# -*- coding: utf-8 -*-
"""Build a weight-ordered review list: overlay entries sorted by corpus frequency."""
import io, re, sys, pathlib, collections
sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path(r'D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns')
SCENES = ROOT / '03_脚本工作区' / 'HD全部130场景_可读反汇编'
pat = re.compile(r'push_string\("((?:[^"\\]|\\.)*)"\);')

cnt = collections.Counter()
for path in sorted(SCENES.rglob('*.bsd')):
    lines = path.read_text('utf8', 'replace').splitlines()
    for i, line in enumerate(lines):
        if 'msg_::f_140()' in line:
            v = [pat.search(lines[z]).group(1) for z in range(max(0, i - 15), i) if pat.search(lines[z])]
            if v:
                cnt[v[-1]] += 1

pairs = {}
for l in io.open(r'D:\tmp\overlay_manual5.tsv', encoding='utf-8'):
    l = l.rstrip('\n')
    if '\t' not in l:
        continue
    k, v = l.split('\t', 1)
    pairs[k] = v

rows = sorted(((cnt.get(k, 0), k, v) for k, v in pairs.items()), key=lambda t: -t[0])
with io.open(r'D:\tmp\overlay_weighted.tsv', 'w', encoding='utf-8', newline='\n') as f:
    for w, k, v in rows:
        f.write('%d\t%s\t%s\n' % (w, k, v))
tot = sum(w for w, _, _ in rows)
print('entries', len(rows), 'covered_by_overlay_messages', tot)
cum = 0
for idx, (w, k, v) in enumerate(rows):
    cum += w
    if idx in (99, 199, 499, 999, 1999, 3999):
        print('top %5d entries -> %5.1f%% of overlay messages' % (idx + 1, 100.0 * cum / tot))
zero = sum(1 for w, _, _ in rows if w == 0)
print('zero_weight_entries', zero)
