#!/usr/bin/env python3
"""
fetch_live_assets.py — Mirror the live Legend of Mushroom web client.

Walks the Cocos Creator 3.x bootstrap chain served at https://lom.joynetgame.com/
and downloads the game scripts, config tables and bundle assets into a dated
capture directory laid out exactly like the site (so decode_config_data.py and
the other repo tools work on it unchanged).

Discovery chain (all hashes are resolved live, never hard-coded):

  index.html
    -> src/polyfills.bundle.<h>.js, src/system.bundle.<h>.js, src/import-map.<h>.json
    -> index.<h>.js -> application.<h>.js -> settingsPath 'src/settings.<h>.json'
  src/settings.<h>.json
    -> assets.bundleVers  { bundle-name: version-hash }
    -> assets.remoteBundles / assets.server
    -> scripting / engine paths (cocos-js/cc.<h>.js via import-map)
  assets/<bundle>/config.<ver>.json      (Cocos bundle manifest)
    -> uuids[], versions.import[], versions.native[], packs{}, paths{}
    -> import/<xx>/<uuid>.<hash>.json    (serialized assets, packs)
    -> native/<xx>/<uuid>.<hash>.<ext>   (raw bin / images / audio / fonts)

Bundles of interest for reverse engineering:
  script               -> assets/script/index.<h>.js   (18 MB game code == game_script.js)
  bundle-firstload-res -> config/datas .bin (all 900+ config tables) + config/proto JSON
  main                 -> GameLoadingView bootstrap
  bundle-LoadingView   -> loading UI + hot-update .manifest files (full native-app asset index)
  internal, resources  -> engine defaults
  bundle-res           -> ~28k art/audio/prefab assets, ~1.5 GB (opt-in with --all)

Usage:
  python3 fetch_live_assets.py                       # core bundles -> uploads/live_YYYYMMDD/
  python3 fetch_live_assets.py --list                # print bundleVers + asset paths, no download
  python3 fetch_live_assets.py --bundles script,bundle-firstload-res
  python3 fetch_live_assets.py --all                 # everything incl. bundle-res (large)
  python3 fetch_live_assets.py --sdk                 # also grab third-party SDK scripts from index.html
  python3 fetch_live_assets.py --out uploads/live_20260904 --workers 16

After a capture:
  python3 decode_config_data.py uploads/live_YYYYMMDD --output data/tables
  cp uploads/live_YYYYMMDD/lom.joynetgame.com/assets/script/index.*.js game_script.js

Requires: requests (pip install requests). Python 3.8+.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from urllib.parse import urljoin, urlparse

try:
    import requests
except ImportError:  # pragma: no cover
    print("pip install requests", file=sys.stderr)
    sys.exit(1)

SITE = "https://lom.joynetgame.com/"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
)

CORE_BUNDLES = [
    "script",
    "bundle-firstload-res",
    "main",
    "bundle-LoadingView",
    "internal",
    "resources",
]

# Native extensions to probe when the import JSON does not tell us (rare).
NATIVE_EXT_GUESSES = [
    ".bin", ".png", ".jpg", ".webp", ".json", ".mp3", ".ogg", ".ttf",
    ".manifest", ".atlas", ".plist", ".fnt", ".txt", ".astc", ".pvr", ".skel",
]

# ---------------------------------------------------------------------------
# Cocos compressed-UUID decoding (engine: cocos/core/utils/decode-uuid.ts)
# ---------------------------------------------------------------------------
_B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
_B64_VAL = {c: i for i, c in enumerate(_B64)}
_HEX = "0123456789abcdef"


def decode_uuid(base64_uuid):
    """22-char compressed uuid -> dashed 36-char uuid. Other strings pass through."""
    sub = ""
    if "@" in base64_uuid:
        base64_uuid, sub = base64_uuid.split("@", 1)
        sub = "@" + sub
    if len(base64_uuid) != 22:
        return base64_uuid + sub
    out = [base64_uuid[0], base64_uuid[1]]
    i = 2
    while i < 22:
        lhs = _B64_VAL[base64_uuid[i]]
        rhs = _B64_VAL[base64_uuid[i + 1]]
        out.append(_HEX[lhs >> 2])
        out.append(_HEX[((lhs & 3) << 2) | (rhs >> 4)])
        out.append(_HEX[rhs & 0xF])
        i += 2
    h = "".join(out)
    return f"{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}" + sub


# ---------------------------------------------------------------------------
# Bundle manifest -> relative file list
# ---------------------------------------------------------------------------
def _pairs(seq):
    """versions arrays are flat [uuidIndex, hash, uuidIndex, hash, ...]."""
    return {seq[i]: seq[i + 1] for i in range(0, len(seq), 2)}


def bundle_files(config):
    """Return (import_files, native_files) as lists of dicts describing each asset file.

    import_files: {uuid, rel}  -> assets/<bundle>/import/xx/<uuid>.<hash>.json
    native_files: {uuid, dir, stem, hash, ext(None)} -> ext resolved later
    """
    uuids = config.get("uuids", [])
    import_base = config.get("importBase", "import")
    native_base = config.get("nativeBase", "native")
    imp_ver = _pairs(config.get("versions", {}).get("import", []))
    nat_ver = _pairs(config.get("versions", {}).get("native", []))
    packs = config.get("packs", {})
    ext_map = {}
    for ext, idxs in config.get("extensionMap", {}).items():
        for idx in idxs:
            ext_map[idx] = ext

    packed = set()
    for members in packs.values():
        packed.update(int(m) for m in members)

    imports, natives = [], []
    for idx, cuuid in enumerate(uuids):
        uuid = decode_uuid(cuuid)
        # Every uuid with an import version has its own import json unless it lives in a pack
        if idx in imp_ver and idx not in packed:
            h = imp_ver[idx]
            imports.append({
                "idx": idx, "uuid": uuid,
                "rel": f"{import_base}/{uuid[:2]}/{uuid}.{h}.json",
            })
        if idx in nat_ver:
            natives.append({
                "idx": idx, "uuid": uuid, "dir": f"{native_base}/{uuid[:2]}",
                "stem": uuid, "hash": nat_ver[idx], "ext": ext_map.get(idx),
            })
    # Pack ids are their own 9-hex names, also indexed in versions.import via uuids[]
    for pack_id in packs:
        if pack_id in uuids:
            continue  # already emitted above
        # Some builds list packs only in packs{}, resolve their hash by name
        for idx, cuuid in enumerate(uuids):
            if cuuid == pack_id and idx in imp_ver:
                imports.append({
                    "idx": idx, "uuid": pack_id,
                    "rel": f"{import_base}/{pack_id[:2]}/{pack_id}.{imp_ver[idx]}.json",
                })
    return imports, natives


# cc.ImageAsset serializes its extension as an index into this list ("fmt").
IMAGE_EXTNAMES = [".png", ".jpg", ".jpeg", ".bmp", ".webp", ".pvr", ".pkm", ".astc"]


def ext_from_doc(doc):
    """Extract the native extension from one serialized asset document.

    Handles '_native': '.bin' style fields (BufferAsset, fonts, manifests) and the
    packed cc.ImageAsset form {'fmt': '1', 'w': .., 'h': ..}.
    """
    def walk(o):
        if isinstance(o, dict):
            v = o.get("_native")
            if isinstance(v, str) and v.startswith("."):
                return v
            f = o.get("fmt")
            if isinstance(f, (str, int)) and "w" in o and "h" in o:
                try:
                    return IMAGE_EXTNAMES[int(f)]
                except (ValueError, IndexError):
                    return None
            for x in o.values():
                r = walk(x)
                if r:
                    return r
        elif isinstance(o, list):
            for x in o:
                r = walk(x)
                if r:
                    return r
        return None

    r = walk(doc)
    if r:
        return r
    m = re.search(r'"(\.[a-z0-9]{2,8})"', json.dumps(doc))
    return m.group(1) if m else None


def native_ext_map(config, import_docs):
    """uuid -> native extension, derived from downloaded import JSON documents.

    import_docs: {uuid-or-packid: parsed json}. Packs of the form
    {"type": "cc.ImageAsset", "data": [doc, doc, ...]} list one doc per member in
    the same order as config['packs'][packid].
    """
    uuids = config.get("uuids", [])
    out = {}
    for pack_id, members in config.get("packs", {}).items():
        doc = import_docs.get(pack_id)
        subs = None
        if isinstance(doc, dict) and isinstance(doc.get("data"), list):
            subs = doc["data"]                      # {"type": "cc.ImageAsset", "data": [...]}
        elif isinstance(doc, list) and len(doc) > 5 and isinstance(doc[5], list):
            subs = doc[5]                           # compact v1: [ver, uuids, strs, classes, masks, docs]
        if subs:
            for member, sub in zip(members, subs):
                ext = ext_from_doc(sub)
                if ext:
                    out[decode_uuid(uuids[int(member)])] = ext
    for key, doc in import_docs.items():
        if key not in out and not (isinstance(doc, dict) and "data" in doc):
            ext = ext_from_doc(doc)
            if ext:
                out[key] = ext
    return out


# ---------------------------------------------------------------------------
# Downloader
# ---------------------------------------------------------------------------
class Mirror:
    def __init__(self, out_dir, workers=8, verbose=False):
        self.out_dir = out_dir
        self.workers = workers
        self.verbose = verbose
        self.s = requests.Session()
        self.s.headers["User-Agent"] = UA
        self.s.headers["Referer"] = SITE
        self.manifest = {}  # rel path -> {url, size, sha256}
        self.failed = []

    def local_path(self, url):
        p = urlparse(url)
        rel = p.path.lstrip("/") or "index.html"
        return os.path.join(self.out_dir, p.netloc, rel)

    def fetch(self, url, retries=4, binary=True):
        last = None
        for attempt in range(retries):
            try:
                r = self.s.get(url, timeout=120)
                if r.status_code == 200:
                    return r.content if binary else r.text
                if r.status_code == 404:
                    return None
                last = f"HTTP {r.status_code}"
            except requests.RequestException as e:
                last = str(e)
            time.sleep(2 ** attempt)
        raise RuntimeError(f"{url}: {last}")

    def head_exists(self, url):
        try:
            r = self.s.head(url, timeout=30, allow_redirects=True)
            if r.status_code in (200, 404):
                return r.status_code == 200
            r = self.s.get(url, timeout=30, stream=True, headers={"Range": "bytes=0-0"})
            ok = r.status_code in (200, 206)
            r.close()
            return ok
        except requests.RequestException:
            return False

    def save(self, url, force=False):
        """Download url to mirror path. Returns bytes (cached read if already present)."""
        path = self.local_path(url)
        if os.path.exists(path) and not force:
            with open(path, "rb") as f:
                data = f.read()
            self._record(url, path, data)
            return data
        data = self.fetch(url)
        if data is None:
            self.failed.append(url)
            return None
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
        self._record(url, path, data)
        if self.verbose:
            print(f"  {len(data):>10}  {url}")
        return data

    def _record(self, url, path, data):
        rel = os.path.relpath(path, self.out_dir)
        self.manifest[rel] = {
            "url": url, "size": len(data), "sha256": hashlib.sha256(data).hexdigest(),
        }

    def save_many(self, urls, label):
        urls = [u for u in urls if u]
        if not urls:
            return
        done = 0
        with ThreadPoolExecutor(self.workers) as ex:
            futs = {ex.submit(self.save, u): u for u in urls}
            for fut in as_completed(futs):
                done += 1
                try:
                    fut.result()
                except Exception as e:  # noqa
                    self.failed.append(futs[fut])
                    print(f"  FAIL {futs[fut]}: {e}", file=sys.stderr)
                if done % 200 == 0 or done == len(urls):
                    print(f"  [{label}] {done}/{len(urls)}")


# ---------------------------------------------------------------------------
# Bootstrap discovery
# ---------------------------------------------------------------------------
def discover_bootstrap(m):
    print(f"GET {SITE}")
    html = m.fetch(SITE, binary=False)
    if html is None:
        raise SystemExit("index.html returned 404")
    m.save(SITE)  # store as lom.joynetgame.com/index.html

    refs = re.findall(r'(?:src|href)=["\']([^"\']+)["\']', html)
    refs += re.findall(r'System\.import\(["\']([^"\']+)["\']', html)
    refs += ["manifest.json", "pwa-sw.js", "favicon.ico"]

    local, external = [], []
    for r in refs:
        u = urljoin(SITE, r)
        (local if urlparse(u).netloc == urlparse(SITE).netloc else external).append(u)

    info = {"index_refs": sorted(set(local)), "external_refs": sorted(set(external))}

    # index.<h>.js -> application.<h>.js -> settings path
    entry = next((u for u in local if re.search(r"/index\.[0-9a-f]+\.js$", u)), None)
    if not entry:
        raise SystemExit("could not find index.<hash>.js in index.html")
    entry_src = m.save(entry).decode("utf-8", "replace")
    app_rel = re.search(r'["\'](\./)?(application\.[0-9a-f]+\.js)["\']', entry_src)
    app_url = urljoin(SITE, app_rel.group(2)) if app_rel else urljoin(SITE, "application.js")
    app_src = m.save(app_url).decode("utf-8", "replace")
    settings_rel = re.search(r"settingsPath\s*=\s*['\"]([^'\"]+)['\"]", app_src)
    settings_url = urljoin(SITE, settings_rel.group(1) if settings_rel else "src/settings.json")
    settings = json.loads(m.save(settings_url).decode("utf-8"))
    info["settings_url"] = settings_url

    # import-map -> engine cc.js and other mapped modules
    imap_url = next((u for u in local if "import-map" in u), None)
    if imap_url:
        imap = json.loads(m.save(imap_url).decode("utf-8"))
        for target in imap.get("imports", {}).values():
            m.save(urljoin(SITE, target))
        info["import_map"] = imap

    # everything else referenced by index.html on the same host
    m.save_many([u for u in local if u not in (entry, app_url)], "index refs")
    return settings, info


def discover_bundle(m, name, version, server=""):
    base = f"{server}remote/{name}/" if server else urljoin(SITE, f"assets/{name}/")
    cfg_url = f"{base}config.{version + '.' if version else ''}json"
    idx_url = f"{base}index.{version + '.' if version else ''}js"
    cfg_raw = m.save(cfg_url)
    if cfg_raw is None:
        print(f"  !! {name}: config not found at {cfg_url}")
        return None
    m.save(idx_url)
    cfg = json.loads(cfg_raw.decode("utf-8"))
    imports, natives = bundle_files(cfg)
    return {"base": base, "config": cfg, "imports": imports, "natives": natives}


def download_bundle(m, name, b):
    base = b["base"]
    print(f"== bundle {name}: {len(b['imports'])} import, {len(b['natives'])} native")
    m.save_many([base + f["rel"] for f in b["imports"]], f"{name} import")

    # Resolve native extensions: extensionMap > import JSON (packs + singles) > HTTP probe
    docs = {}
    for f in b["imports"]:
        p = m.local_path(base + f["rel"])
        if os.path.exists(p):
            try:
                with open(p, "rb") as fh:
                    docs[f["uuid"]] = json.load(fh)
            except Exception:
                pass
    ext_map = native_ext_map(b["config"], docs)
    urls = []
    for n in b["natives"]:
        ext = n["ext"] or ext_map.get(n["uuid"])
        stem = f"{base}{n['dir']}/{n['stem']}.{n['hash']}"
        if not ext:
            ext = next((e for e in NATIVE_EXT_GUESSES if m.head_exists(stem + e)), None)
        if not ext:
            print(f"  !! no extension resolved for {n['uuid']} in {name}", file=sys.stderr)
            m.failed.append(stem + ".?")
            continue
        n["ext"] = ext
        urls.append(stem + ext)
    m.save_many(urls, f"{name} native")


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=None, help="capture dir (default uploads/live_YYYYMMDD)")
    ap.add_argument("--bundles", default=",".join(CORE_BUNDLES),
                    help="comma list of bundles (default: core set)")
    ap.add_argument("--all", action="store_true", help="download every bundle in bundleVers incl. bundle-res")
    ap.add_argument("--sdk", action="store_true", help="also fetch third-party SDK scripts referenced by index.html")
    ap.add_argument("--list", action="store_true", help="discover and print, do not download bundle assets")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    out = args.out or os.path.join("uploads", "live_" + datetime.now().strftime("%Y%m%d"))
    m = Mirror(out, workers=args.workers, verbose=args.verbose)

    settings, info = discover_bootstrap(m)
    assets = settings.get("assets", {})
    bundle_vers = assets.get("bundleVers", {})
    remote = set(assets.get("remoteBundles", []))
    server = assets.get("server", "") or ""
    print(f"settings: {info['settings_url']}")
    print(f"bundleVers: {json.dumps(bundle_vers)}")
    if remote:
        print(f"remoteBundles: {sorted(remote)} server={server!r}")
    print(f"external refs: {info['external_refs']}")

    wanted = list(bundle_vers) if args.all else [b.strip() for b in args.bundles.split(",") if b.strip()]
    for b in wanted:
        if b not in bundle_vers:
            print(f"  !! bundle {b!r} not in bundleVers (versionless fetch attempted)")

    bundles = {}
    for name in wanted:
        b = discover_bundle(m, name, bundle_vers.get(name, ""), server if name in remote else "")
        if b:
            bundles[name] = b
            paths = b["config"].get("paths", {})
            print(f"  {name}: v={bundle_vers.get(name, '-')} uuids={len(b['config'].get('uuids', []))} "
                  f"paths={len(paths)} import={len(b['imports'])} native={len(b['natives'])}")
            if args.list or args.verbose:
                for idx, (p, *_rest) in sorted(paths.items(), key=lambda kv: kv[1][0]):
                    print(f"      {p}  ->  {decode_uuid(b['config']['uuids'][int(idx)])}")

    if args.sdk:
        m.save_many(info["external_refs"], "sdk")

    if not args.list:
        for name, b in bundles.items():
            download_bundle(m, name, b)

    # capture manifest + summary
    os.makedirs(out, exist_ok=True)
    summary = {
        "captured_at": datetime.now().isoformat(timespec="seconds"),
        "site": SITE,
        "settings_url": info["settings_url"],
        "bundleVers": bundle_vers,
        "remoteBundles": sorted(remote),
        "server": server,
        "external_refs": info["external_refs"],
        "bundles": {n: {"base": b["base"], "config": b["config"]} for n, b in bundles.items()},
        "files": m.manifest,
        "failed": m.failed,
    }
    with open(os.path.join(out, "capture_manifest.json"), "w") as f:
        json.dump(summary, f, indent=1)

    total = sum(v["size"] for v in m.manifest.values())
    print(f"\ncaptured {len(m.manifest)} files, {total / 1e6:.1f} MB -> {out}")
    if m.failed:
        print(f"{len(m.failed)} failures (see capture_manifest.json)")

    script = [k for k in m.manifest if re.search(r"assets/script/index\.[0-9a-f]+\.js$", k)]
    if script:
        print(f"game script: {script[0]}  sha256={m.manifest[script[0]]['sha256'][:16]}")
    if "bundle-firstload-res" in bundles and not args.list:
        print(f"next: python3 decode_config_data.py {out} --output data/tables")


if __name__ == "__main__":
    main()
