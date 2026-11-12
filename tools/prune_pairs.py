# -*- coding: utf-8 -*-
"""Prune over-long fields from manual_pairs.tsv.

The on-disk TSV stores newlines as the two ASCII characters \\n, so the real
overlay field length is len(text) + count(newline). Validate that escaped form.
"""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

P = r'D:\tmp\manual_pairs.tsv'
LIMIT = 512
rows = []
for l in io.open(P, encoding='utf-8'):
    l = l.rstrip('\n')
    if '\t' not in l:
        continue
    k, v = l.split('\t', 1)
    rows.append((k, v))

def esc_len(s, enc):
    # s already holds literal backslash-n sequences; count them as written
    try:
        return len(s.encode(enc))
    except Exception:
        return 10 ** 9

keep, dropped = [], []
for k, v in rows:
    kl = esc_len(k, 'cp932')
    vl = esc_len(v, 'gbk')
    if kl > LIMIT or vl > LIMIT:
        dropped.append((k, v, kl, vl))
        continue
    keep.append((k, v))

print('kept', len(keep), 'dropped', len(dropped))
for k, v, kl, vl in dropped:
    print('DROP jp_bytes', kl, 'cn_bytes', vl, '|', k[:60].encode('ascii', 'backslashreplace').decode())

if '--write' in sys.argv:
    with io.open(P, 'w', encoding='utf-8', newline='\n') as f:
        for k, v in keep:
            f.write(k + '\t' + v + '\n')
    print('rewrote', P)
