#!/usr/bin/env python3
"""
LOM Web Capture Filter
Filters an extracted web capture directory to keep only game-relevant files.

Strips out images, fonts, audio, video, CSS, and third-party tracking/auth
domains, keeping only JS, JSON, and binary data files needed for RE work.

Usage:
    python3 filter_capture.py /path/to/extracted/capture
    python3 filter_capture.py /path/to/extracted/capture --output data/capture
    python3 filter_capture.py /path/to/extracted/capture --dry-run
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone


# File extensions to DROP (media, fonts, styles)
DROP_EXTENSIONS = {
    # Images
    '.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.ico', '.bmp',
    # Audio
    '.mp3', '.ogg', '.wav', '.aac', '.m4a', '.flac',
    # Video
    '.mp4', '.webm', '.avi', '.mov',
    # Fonts
    '.woff', '.woff2', '.ttf', '.eot', '.otf',
    # Styles
    '.css',
    # Source maps
    '.map',
}

# File extensions to KEEP
KEEP_EXTENSIONS = {
    '.js', '.json', '.bin', '.dat', '.cfg', '.proto', '.txt', '.html',
}

# Domain prefixes to DROP entirely (third-party auth, analytics, tracking)
DROP_DOMAINS = [
    'accounts.google.com',
    'appleid.cdn-apple.com',
    'connect.facebook.net',
    'captcha-cdn.joynetgame.com',
    'www.googletagmanager.com',
    's.axon.ai',
    'c.albss.com',
    'apiapm.ssgamescenter.com',
    'mkts.joynetgame.com',
    'y.joynetgame.com',
]

# Domain prefixes to DROP (pattern match)
DROP_DOMAIN_PATTERNS = [
    'slogin',
]


def should_drop_domain(filepath):
    """Check if the file is under a domain we want to drop."""
    parts = filepath.replace('\\', '/').split('/')
    if not parts:
        return False

    top_dir = parts[0]

    for domain in DROP_DOMAINS:
        if top_dir == domain or top_dir.startswith(domain):
            return True

    for pattern in DROP_DOMAIN_PATTERNS:
        if top_dir.startswith(pattern):
            return True

    return False


def should_keep_file(rel_path, file_size):
    """Decide whether to keep a file based on extension, size, and path."""
    _, ext = os.path.splitext(rel_path.lower())

    # Always drop media/font/style extensions
    if ext in DROP_EXTENSIONS:
        return False, f"dropped extension {ext}"

    # Always keep binary data files
    if ext == '.bin':
        return True, "binary data"

    # Keep JS files (game logic)
    if ext == '.js':
        return True, "javascript"

    # Keep JSON files if they have meaningful content (>100 bytes)
    if ext == '.json':
        if file_size < 100:
            return False, "tiny json (<100 bytes)"
        return True, "json data"

    # Keep other data formats
    if ext in KEEP_EXTENSIONS:
        return True, f"data file ({ext})"

    # For unknown extensions, keep if reasonably sized
    if ext == '' or ext not in DROP_EXTENSIONS:
        if file_size > 100:
            return True, f"unknown type ({ext or 'no ext'})"
        return False, f"tiny unknown file"

    return False, "unrecognized"


def format_size(size_bytes):
    """Format byte count as human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def main():
    parser = argparse.ArgumentParser(
        description="Filter extracted web capture to keep only game-relevant files."
    )
    parser.add_argument(
        "input_dir",
        help="Path to the extracted web capture directory"
    )
    parser.add_argument(
        "--output", "-o",
        default="data/capture",
        help="Output directory for filtered files (default: data/capture)"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would be kept/dropped without copying"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show every file decision"
    )
    args = parser.parse_args()

    input_dir = os.path.abspath(args.input_dir)
    output_dir = os.path.abspath(args.output)

    if not os.path.isdir(input_dir):
        print(f"ERROR: Input directory not found: {input_dir}")
        sys.exit(1)

    print("=" * 60)
    print("LOM Web Capture Filter")
    print("=" * 60)
    print(f"Input:  {input_dir}")
    print(f"Output: {output_dir}")
    if args.dry_run:
        print("Mode:   DRY RUN (no files will be copied)")
    print()

    # Walk input directory
    kept_files = []
    dropped_files = []
    kept_size = 0
    dropped_size = 0
    large_files = []

    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, input_dir)
            file_size = os.path.getsize(filepath)

            # Check domain filter first
            if should_drop_domain(rel_path):
                dropped_files.append((rel_path, file_size, "dropped domain"))
                dropped_size += file_size
                if args.verbose:
                    print(f"  DROP [domain]  {rel_path} ({format_size(file_size)})")
                continue

            # Check file filter
            keep, reason = should_keep_file(rel_path, file_size)

            if keep:
                kept_files.append((rel_path, file_size, reason))
                kept_size += file_size
                if args.verbose:
                    print(f"  KEEP [{reason}]  {rel_path} ({format_size(file_size)})")
                if file_size > 5 * 1024 * 1024:
                    large_files.append((rel_path, file_size))
            else:
                dropped_files.append((rel_path, file_size, reason))
                dropped_size += file_size
                if args.verbose:
                    print(f"  DROP [{reason}]  {rel_path} ({format_size(file_size)})")

    # Summary
    print(f"\nResults:")
    print(f"  Files kept:    {len(kept_files):>6} ({format_size(kept_size)})")
    print(f"  Files dropped: {len(dropped_files):>6} ({format_size(dropped_size)})")
    print(f"  Total scanned: {len(kept_files) + len(dropped_files):>6} ({format_size(kept_size + dropped_size)})")

    if large_files:
        print(f"\nLarge files (>5MB) that will be kept:")
        for path, size in sorted(large_files, key=lambda x: -x[1]):
            print(f"  {format_size(size):>10}  {path}")

    # Breakdown by extension
    ext_stats = {}
    for path, size, reason in kept_files:
        _, ext = os.path.splitext(path.lower())
        ext = ext or '(none)'
        if ext not in ext_stats:
            ext_stats[ext] = {'count': 0, 'size': 0}
        ext_stats[ext]['count'] += 1
        ext_stats[ext]['size'] += size

    print(f"\nKept files by type:")
    for ext, stats in sorted(ext_stats.items(), key=lambda x: -x[1]['size']):
        print(f"  {ext:>8}: {stats['count']:>4} files, {format_size(stats['size'])}")

    if args.dry_run:
        print("\nDry run complete. No files were copied.")
        return

    # Copy files
    print(f"\nCopying {len(kept_files)} files to {output_dir}...")
    os.makedirs(output_dir, exist_ok=True)

    for i, (rel_path, file_size, reason) in enumerate(kept_files, 1):
        src = os.path.join(input_dir, rel_path)
        dst = os.path.join(output_dir, rel_path)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

        if i % 50 == 0 or i == len(kept_files):
            print(f"  Copied {i}/{len(kept_files)} files...")

    # Generate manifest
    manifest = {
        "sourceDir": input_dir,
        "filteredAt": datetime.now(timezone.utc).isoformat(),
        "totalScanned": len(kept_files) + len(dropped_files),
        "totalKept": len(kept_files),
        "totalDropped": len(dropped_files),
        "keptSize": kept_size,
        "droppedSize": dropped_size,
        "entries": [
            {
                "path": path,
                "size": size,
                "type": reason,
            }
            for path, size, reason in sorted(kept_files, key=lambda x: x[0])
        ]
    }

    manifest_path = os.path.join(output_dir, "_manifest.json")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    print(f"\nManifest saved: {manifest_path}")
    print(f"Output size: {format_size(kept_size)}")
    print("Done!")


if __name__ == '__main__':
    main()
