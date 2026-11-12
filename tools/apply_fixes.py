# -*- coding: utf-8 -*-
"""Validate reviewer fix files and append accepted fixes to manual_pairs.tsv.

usage: python apply_fixes.py 001 002 ... [--write]
"""
import io, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

REV = r'D:\tmp\review'
MANUAL = r'D:\tmp\manual_pairs.tsv'
OVER = r'D:\tmp\overlay_manual5.tsv'

overlay = {}
for l in io.open(OVER, encoding='utf-8'):
    l = l.rstrip('\n')
    if '\t' not in l:
        continue
    k, v = l.split('\t', 1)
    overlay[k] = v

write = '--write' in sys.argv
nums = [a for a in sys.argv[1:] if not a.startswith('--')]
accepted, rejected = [], []
for num in nums:
    chunk = os.path.join(REV, 'chunk_%s.tsv' % num)
    fix = os.path.join(REV, 'fix_%s.tsv' % num)
    if not os.path.exists(fix):
        print('MISSING FIX FILE', fix)
        continue
    idx2jp = {}
    for l in io.open(chunk, encoding='utf-8'):
        l = l.rstrip('\n')
        p = l.split('\t', 3)
        if len(p) == 4:
            idx2jp[p[0]] = p[2]
    n = 0
    for l in io.open(fix, encoding='utf-8-sig'):
        l = l.rstrip('\r\n')
        if not l.strip() or '\t' not in l:
            continue
        parts = l.split('\t')
        idx = parts[0].strip()
        cn = parts[-1].rstrip('\r') if len(parts) > 2 else parts[1]
        if len(parts) > 2:
            # reviewer pasted whole rows; the last column is the translation
            pass
        n += 1
        jp = idx2jp.get(idx)
        why = None
        if jp is None:
            why = 'unknown idx'
        elif jp not in overlay:
            why = 'jp not in overlay'
        elif cn == '':
            why = 'empty cn'
        elif '\t' in cn:
            why = 'tab in cn'
        elif '\n' in cn or '\r' in cn:
            why = 'raw newline in cn'
        else:
            try:
                if len(cn.encode('gbk')) > 500:
                    why = 'cn over 500 bytes'
            except Exception as e:
                why = 'gbk fail'
        if why is None:
            esc = chr(92) + 'n'
            if jp.count(esc) != cn.count(esc):
                why = 'newline escape count differs'
        if why is None:
            lead = lambda s: len(s) - len(s.lstrip('\u3000 '))
            if lead(jp) != lead(cn.rstrip('\\n')) and lead(jp) != lead(cn):
                why = 'indent differs'
        if why:
            rejected.append((num, idx, why, cn[:40]))
            continue
        accepted.append((jp, cn, num, idx))
    print('chunk %s fixes read %d' % (num, n))

print('accepted', len(accepted), 'rejected', len(rejected))
seen = set()
final = []
for jp, cn, num, idx in accepted:
    if jp in seen:
        continue
    seen.add(jp)
    old = overlay.get(jp, '')
    if old == cn:
        continue
    final.append((jp, cn, num, idx))
    print('FIX %s#%s' % (num, idx))
    print('   JP :', jp[:100])
    print('   OLD:', old[:100])
    print('   NEW:', cn[:100])
for r in rejected[:20]:
    print('REJECT', r)

print('final_applied', len(final))
if not write:
    print('DRY_RUN')
    sys.exit(0)

with io.open(MANUAL, 'a', encoding='utf-8', newline='\n') as f:
    for jp, cn, num, idx in final:
        f.write(jp + '\t' + cn + '\n')
print('appended', len(final))
