#!/usr/bin/env python3
"""Convert a repo markdown doc into Discord-paste-ready message chunks.

Discord differences handled:
  - no table support      -> markdown tables become aligned ``` code blocks
  - headings stop at ###  -> #### becomes bold
  - 2000 char/message     -> split on structural boundaries, never inside a fence
"""
import sys, re

LIMIT = 1900          # leave headroom under Discord's 2000


def table_to_block(lines):
    rows = []
    for ln in lines:
        if re.fullmatch(r'\s*\|[\s|:-]+\|\s*', ln):   # separator row
            continue
        rows.append([c.strip() for c in ln.strip().strip('|').split('|')])
    if not rows:
        return []
    # strip markdown emphasis/code marks that only add noise in a code block
    clean = [[re.sub(r'(\*\*|`|\*)', '', c) for c in r] for r in rows]
    width = max(len(r) for r in clean)
    clean = [r + [''] * (width - len(r)) for r in clean]
    col = [max(len(r[i]) for r in clean) for i in range(width)]

    # Discord code blocks do not wrap; a wide table forces horizontal scrolling on
    # mobile. Past ~68 columns, render the rows as a list instead.
    if sum(col) + 2 * (width - 1) > 68:
        head, body = rows[0], rows[1:]
        out = []
        for r in body:
            r = r + [''] * (width - len(r))
            first = re.sub(r'(\*\*|`)', '', r[0]).strip()
            rest = ' · '.join(f"{head[j].strip('* `')}: {r[j].strip()}"
                              for j in range(1, width) if r[j].strip())
            out.append(f"- **{first}** — {rest}" if rest else f"- **{first}**")
        return out

    out = ['```']
    for i, r in enumerate(clean):
        out.append('  '.join(c.ljust(col[j]) for j, c in enumerate(r)).rstrip())
        if i == 0:
            out.append('  '.join('-' * col[j] for j in range(width)))
    out.append('```')
    return out


def convert(src):
    lines = src.split('\n')
    out, i, in_fence = [], 0, False
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('```'):
            in_fence = not in_fence
            out.append(ln); i += 1; continue
        if not in_fence and ln.lstrip().startswith('|') and ln.rstrip().endswith('|'):
            block = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                block.append(lines[i]); i += 1
            out.extend(table_to_block(block)); continue
        if ln.startswith('#### '):
            ln = '**' + ln[5:].strip() + '**'
        out.append(ln); i += 1
    return unwrap('\n'.join(out))


def unwrap(text):
    """Join hard-wrapped prose/list/quote lines so Discord reflows them; drop --- rules."""
    res, fence = [], False
    for ln in text.split('\n'):
        if ln.startswith('```'):
            fence = not fence; res.append(ln); continue
        if fence:
            res.append(ln); continue
        if re.fullmatch(r'\s*-{3,}\s*', ln):        # horizontal rule: not a thing in Discord
            continue
        starts_new = (
            not ln.strip()
            or ln.startswith('#')
            or re.match(r'\s*([-*+]|\d+\.)\s', ln)
            or ln.startswith('>')
            or ln.startswith('|')
        )
        if res and not starts_new and res[-1].strip() and not res[-1].startswith('```') \
                and not res[-1].startswith('#'):
            res[-1] = res[-1].rstrip() + ' ' + ln.strip()
        else:
            res.append(ln)
    # collapse runs of blank lines
    final = []
    for ln in res:
        if not ln.strip() and final and not final[-1].strip():
            continue
        final.append(ln)
    return '\n'.join(final)


def blocks_of(text):
    """Paragraphs and complete fenced blocks. Oversized fences are re-fenced in pieces."""
    out, cur, fence = [], [], False
    for ln in text.split('\n'):
        if ln.startswith('```'):
            fence = not fence
            cur.append(ln)
            if not fence:
                out.append('\n'.join(cur)); cur = []
            continue
        cur.append(ln)
        if not fence and ln.strip() == '':
            out.append('\n'.join(cur)); cur = []
    if cur:
        out.append('\n'.join(cur))

    out = [b for b in out if b.strip()]
    final = []
    for b in out:
        if len(b) <= LIMIT:
            final.append(b); continue
        body = b.split('\n')
        if body[0].startswith('```'):           # split the fence into several fences
            inner, piece, n = body[1:-1], [], 0
            for ln in inner:
                if n + len(ln) + 1 > LIMIT - 16 and piece:
                    final.append('```\n' + '\n'.join(piece) + '\n```')
                    piece, n = [], 0
                piece.append(ln); n += len(ln) + 1
            if piece:
                final.append('```\n' + '\n'.join(piece) + '\n```')
        else:                                    # plain prose: split on lines
            piece, n = [], 0
            for ln in body:
                if n + len(ln) + 1 > LIMIT and piece:
                    final.append('\n'.join(piece)); piece, n = [], 0
                piece.append(ln); n += len(ln) + 1
            if piece:
                final.append('\n'.join(piece))
    return final


def chunk(text):
    raw = blocks_of(text)
    merged = []
    for b in raw:
        if merged and merged[-1].strip().startswith('#') and len(merged[-1].strip().split('\n')) == 1 \
                and len(merged[-1]) + len(b) + 2 <= LIMIT:
            merged[-1] = merged[-1].strip('\n') + '\n' + b
        else:
            merged.append(b)
    msgs, buf = [], ''
    for b in merged:
        if buf and len(buf) + len(b) + 2 > LIMIT:
            msgs.append(buf.strip('\n')); buf = ''
        buf += ('\n\n' if buf else '') + b.strip('\n')
    if buf.strip():
        msgs.append(buf.strip('\n'))
    return [m for m in msgs if m.strip()]


if __name__ == '__main__':
    text = convert(open(sys.argv[1], encoding='utf-8').read())
    msgs = chunk(text)
    parts = []
    for n, m in enumerate(msgs, 1):
        parts.append(f"━━━━━━━━━━ MESSAGE {n}/{len(msgs)}  ({len(m)} chars) ━━━━━━━━━━\n\n{m}")
    open(sys.argv[2], 'w', encoding='utf-8').write('\n\n'.join(parts) + '\n')
    print(f"{len(msgs)} messages, max {max(len(m) for m in msgs)} chars")
