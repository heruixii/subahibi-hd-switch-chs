# -*- coding: utf-8 -*-
"""Round 49 coverage: base SBCHS001 + 26 + 759 sidecars + SBCHS004 overlay vs 130 .bsd messages."""
import io, re, struct, hashlib, collections, sys, pathlib

ROOT = pathlib.Path(r'D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns')
SCENES = ROOT / '03_脚本工作区' / 'HD全部130场景_可读反汇编'
BASE = next(p for p in ROOT.glob('03_脚本工作区/**/*.bin') if p.stat().st_size == 3267477)
S26 = next(p for p in ROOT.glob('03_脚本工作区/**/opening_narration_private_cp932_gbk_26.bin') if p.stat().st_size == 2090)
S759 = next(p for p in ROOT.glob('03_脚本工作区/**/P1441_*.bin') if p.stat().st_size == 80307)
S26 = next(ROOT.glob('03_脚本工作区/P1329_*/*/opening_narration_private_cp932_gbk_26.bin'), None) or next(ROOT.glob('03_脚本工作区/P1329_*/opening_narration_private_cp932_gbk_26.bin'))
S759 = next(ROOT.glob('03_脚本工作区/P1441_*/P1441_真实已知逐句无音日中安全对齐仅私人GBK补丁_SBCHS003.bin'))
OVER = pathlib.Path(r'D:\tmp\overlay_manual5.tsv')

pat = re.compile(r'push_string\("((?:[^"\\]|\\.)*)"\);')

def messages():
    out = []
    for path in sorted(SCENES.rglob('*.bsd')):
        lines = path.read_text('utf8', 'replace').splitlines()
        for i, line in enumerate(lines):
            if 'msg_::f_140()' in line:
                v = [pat.search(lines[z]).group(1) for z in range(max(0, i - 15), i) if pat.search(lines[z])]
                if v:
                    out.append(v[-1])
    return out

def load_sidecar(path, magic):
    data = path.read_bytes()
    assert data[:8] == magic, (path, data[:8])
    ver, count = struct.unpack_from('<II', data, 8)
    at = 16
    d = {}
    for _ in range(count):
        n, m = struct.unpack_from('<HH', data, at); at += 4
        k = data[at:at + n].decode('cp932'); at += n
        v = data[at:at + m].decode('gbk'); at += m
        d[k] = v
    assert at == len(data)
    return d

def load_base():
    data = BASE.read_bytes()
    assert data[:8] == b'SBCHS001'
    ver, count = struct.unpack_from('<II', data, 8)
    at = 16
    d = {}
    for _ in range(count):
        n, m = struct.unpack_from('<HH', data, at); at += 4
        k = data[at:at + n].decode('cp932'); at += n
        v = data[at:at + m].decode('gbk'); at += m
        d[k] = v
    assert at == len(data)
    return d, count

base, bcount = load_base()
s26 = load_sidecar(S26, b'SBCHS002')
s759 = load_sidecar(S759, b'SBCHS003')
ov = {}
for l in io.open(OVER, encoding='utf-8'):
    l = l.rstrip('\n')
    if '\t' not in l: continue
    k, v = l.split('\t', 1); ov[k] = v
print('base', bcount, 's26', len(s26), 's759', len(s759), 'overlay', len(ov))

msgs = messages()
print('messages', len(msgs), 'unique', len(set(msgs)))

def covered(m):
    return m in ov or m in s759 or m in s26 or m in base

hit = sum(1 for m in msgs if covered(m))
print('covered %d/%d = %.2f%%' % (hit, len(msgs), 100.0 * hit / len(msgs)))

# per-layer attribution
lay = collections.Counter()
for m in msgs:
    if m in ov: lay['overlay'] += 1
    elif m in s759: lay['759'] += 1
    elif m in s26: lay['26'] += 1
    elif m in base: lay['base'] += 1
    else: lay['none'] += 1
print(dict(lay))

missu = collections.Counter(m for m in msgs if not covered(m))
print('unique uncovered', len(missu), 'messages uncovered', sum(missu.values()))
out = pathlib.Path(r'D:\tmp\uncovered_after_m18.tsv')
with io.open(out, 'w', encoding='utf-8') as f:
    for m, c in missu.most_common():
        f.write('%d\t%s\n' % (c, m))
print('wrote', out)
