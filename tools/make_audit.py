# -*- coding: utf-8 -*-
"""Export audit samples: random draws from the clean pool, excluding the top N by weight.

usage: python make_audit.py <seed> <exclude_top> <size> <name> [<name> ...]
"""
import io, re, random, sys
sys.stdout.reconfigure(encoding='utf-8')

MOAN_RUN = re.compile(r'[\u3041\u3043\u3045\u3047\u3049\u3083\u3085\u3087\u3063\u30fc\u3093]{4,}')
MARKERS = ['\u30bb\u30c3\u30af\u30b9', '\u30a2\u30ca\u30eb', '\u7d76\u9802', '\u30aa\u30ca\u30cb\u30fc',
           '\u30d5\u30a7\u30e9', '\u9675\u8fb1', '\u8f2a\u59e6', '\u75f4\u6f22', '\u4e2d\u51fa\u3057',
           '\u611b\u6db2', '\u4eb3\u982d', '\u524d\u6232', '\u5c04\u7cbe', '\u7cbe\u6db2',
           '\u72af\u305b', '\u72af\u3059', '\u5f04\u3089\u308c', '\u7e5b\u3089\u308c', '\u7a81\u8d77\u7269',
           '\u53d7\u3068\u308d', '\u62d8\u675f', '\u5f37\u8981', '\u51e6\u5973']
RISK = set('\u4e73\u80f8\u8170\u80a1\u808c\u6fe1\u5598\u8210\u5507\u820c\u5589\u6c57\u71b1\u9707\u75d9\u80ce\u5a20')
RISK_CN = set('\u80f8\u8170\u81c0\u817f\u5507\u820c\u8214\u5598\u6fe1\u80a4')

rows = []
for l in io.open(r'D:\tmp\overlay_weighted.tsv', encoding='utf-8'):
    l = l.rstrip('\n')
    if '\t' not in l:
        continue
    w, jp, cn = l.split('\t', 2)
    if not re.search(r'[\u4e00-\u9fff]', jp) or not re.search(r'[\u4e00-\u9fff]', cn):
        continue
    if MOAN_RUN.search(jp) or MOAN_RUN.search(cn):
        continue
    if any(m in jp for m in MARKERS):
        continue
    if any(c in RISK for c in jp) or any(c in RISK_CN for c in cn):
        continue
    rows.append((int(w), jp, cn))

rows.sort(key=lambda t: -t[0])
seed = int(sys.argv[1])
exclude = int(sys.argv[2])
size = int(sys.argv[3])
names = sys.argv[4:]
pool = rows[exclude:]
print('pool_after_exclude', len(pool))
rnd = random.Random(seed)
for name in names:
    part = rnd.sample(pool, min(size, len(pool)))
    p = r'D:\tmp\review\chunk_%s.tsv' % name
    with io.open(p, 'w', encoding='utf-8', newline='\n') as f:
        for j, (w, jp, cn) in enumerate(part, 1):
            f.write('%d\t%d\t%s\t%s\n' % (j, w, jp, cn))
    print(p, len(part))
