# -*- coding: utf-8 -*-
"""assemble clean_pairs.tsv = current overlay + placeholders for adult-scene keys."""
import io, json

SRC = r'D:\tmp\repo_edit\translation\overlay_manual5.tsv'
BUCKETS = r'D:\tmp\clean_buckets.json'
OUT = r'D:\tmp\clean_pairs.tsv'
PLACEHOLDER = '（此处内容已省略）'

rows = []
seen = set()
for ln in io.open(SRC, encoding='utf-8'):
    ln = ln.rstrip('\n')
    if not ln or ln.startswith('#'):
        continue
    if '\t' not in ln:
        continue
    k, v = ln.split('\t', 1)
    rows.append((k, v))
    seen.add(k)

buckets = json.load(io.open(BUCKETS, encoding='utf-8'))
added = skipped = 0
for k in buckets['adult']:
    if k in seen:
        continue
    try:
        kb = k.encode('cp932')
    except UnicodeEncodeError:
        skipped += 1
        continue
    if len(kb) > 500:
        skipped += 1
        continue
    rows.append((k, PLACEHOLDER))
    seen.add(k)
    added += 1

io.open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(k + '\t' + v for k, v in rows) + '\n')
print('base', len(rows) - added, 'placeholders', added, 'skipped', skipped, 'total', len(rows))
