# -*- coding: utf-8 -*-
"""Integrity check: every manual_pairs entry (last value wins) must appear with the
same value in the merged overlay."""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

def load_last(p):
    d = {}
    for l in io.open(p, encoding='utf-8'):
        l = l.rstrip('\r\n')
        if '\t' not in l:
            continue
        k, v = l.split('\t', 1)
        d[k] = v
    return d

manual = load_last(r'D:\tmp\manual_pairs.tsv')
over = load_last(r'D:\tmp\overlay_manual5.tsv')
print('manual_pairs', len(manual), 'overlay', len(over))
miss = [k for k in manual if k not in over]
diff = [k for k in manual if k in over and over[k] != manual[k]]
print('missing_from_overlay', len(miss))
print('value_mismatch', len(diff))
for k in miss[:8]:
    print('  MISS', repr(k[:46]))
for k in diff[:8]:
    print('  DIFF', repr(k[:46]))
    print('    manual:', repr(manual[k][:50]))
    print('    overlay:', repr(over[k][:50]))
