# -*- coding: utf-8 -*-
"""Full dictionary-stack coverage + classification of the uncovered messages."""
import io, json, pathlib, re, struct, zipfile, os

ROOT = pathlib.Path(r'D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns')
SCENES = ROOT / '03_脚本工作区' / 'HD全部130场景_可读反汇编'
ZIP = r'D:\tmp\dl\Subahibi_HD_CHS_v1.0.0_full.zip'
WORK = r'D:\tmp\dict'
os.makedirs(WORK, exist_ok=True)

with zipfile.ZipFile(ZIP) as z:
    for n in z.namelist():
        if n.startswith('switch/subahibi_pc_native_hd_qa/chs/'):
            out = os.path.join(WORK, os.path.basename(n))
            if not os.path.exists(out):
                with z.open(n) as f, open(out, 'wb') as g:
                    g.write(f.read())

pat = re.compile(r'push_string\("((?:[^"\\]|\\.)*)"\);')

def load_bin(path):
    d = pathlib.Path(path).read_bytes()
    assert d[:8].startswith(b'SBCHS'), path
    ver, count = struct.unpack_from('<II', d, 8)
    at = 16
    m = {}
    for _ in range(count):
        n, k = struct.unpack_from('<HH', d, at); at += 4
        key = d[at:at + n].decode('cp932', 'replace'); at += n
        val = d[at:at + k].decode('gbk', 'replace'); at += k
        m[key] = val
    return m

stack = {}
for fn in ('dialogue_cp932_gbk.bin', 'opening_narration_private_cp932_gbk_26.bin',
           'unvoiced_unique_voice_anchor_cp932_gbk_759.bin'):
    p = os.path.join(WORK, fn)
    if os.path.exists(p):
        m = load_bin(p)
        stack[fn] = len(m)
        for k, v in m.items():
            stack.setdefault('_map', {})[k] = v

# overlay: take the authoritative TSV (binary header carries extra fields)
ov = {}
for ln in io.open(r'D:\tmp\repo_edit\translation\overlay_manual5.tsv', encoding='utf-8'):
    ln = ln.rstrip('\n')
    if '\t' in ln:
        k, v = ln.split('\t', 1)
        ov[k] = v
stack['overlay_tsv'] = len(ov)

mapping = stack.pop('_map'); mapping.update(ov)
print('dictionary sizes:', stack)
print('merged keys:', len(mapping))

msgs = []
for path in sorted(SCENES.rglob('*.bsd')):
    lines = path.read_text('utf8', 'replace').splitlines()
    for i, line in enumerate(lines):
        if 'msg_::f_140()' in line:
            v = [pat.search(lines[z]).group(1) for z in range(max(0, i - 15), i) if pat.search(lines[z])]
            if v:
                msgs.append(v[-1])

covered = sum(1 for m in msgs if m in mapping)
uncov = sorted({m for m in msgs if m not in mapping})
print('occurrences:', len(msgs))
print('covered occurrences:', covered, '(%.2f%%)' % (100.0 * covered / len(msgs)))
print('uncovered unique:', len(uncov))

def gbk_ok(s):
    try:
        s.encode('gbk'); return True
    except Exception:
        return False

buckets = {'too_long': [], 'unencodable': [], 'short': [], 'adult': []}
for m in uncov:
    if len(m) > 500:
        buckets['too_long'].append(m)
    elif not gbk_ok(m):
        buckets['unencodable'].append(m)
    elif len(m) <= 12 and not any(c in m for c in '。！？!?、…'):
        buckets['short'].append(m)
    else:
        buckets['adult'].append(m)

print('buckets:', {k: len(v) for k, v in buckets.items()})
io.open(r'D:\tmp\clean_buckets.json', 'w', encoding='utf-8').write(
    json.dumps({k: v for k, v in buckets.items()}, ensure_ascii=False))
io.open(r'D:\tmp\stats_stack.json', 'w', encoding='utf-8').write(
    json.dumps({'occurrences': len(msgs), 'covered': covered,
                'uncovered_unique': len(uncov),
                'buckets': {k: len(v) for k, v in buckets.items()}}, ensure_ascii=False, indent=2))
print('written')
