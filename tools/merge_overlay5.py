import io, sys
sys.stdout.reconfigure(encoding='utf-8')

def load(p):
    d = {}
    order = []
    for l in io.open(p, encoding='utf-8'):
        l = l.rstrip('\n')
        if '\t' not in l:
            continue
        k, v = l.split('\t', 1)
        if not k or v == '':
            continue
        if k not in d:
            order.append(k)
        d[k] = v
    return d, order

a, ao = load(r'D:\tmp\manual_pairs.tsv')       # newer wins
b, bo = load(r'D:\tmp\overlay_manual4.tsv')    # m18 source

out = []
seen = set()
for k in ao:
    out.append(k + '\t' + a[k]); seen.add(k)
add = 0
for k in bo:
    if k in seen:
        continue
    out.append(k + '\t' + b[k]); seen.add(k); add += 1

print('manual_pairs', len(a), 'm18', len(b), 'union', len(out), 'added_from_m18', add)
conflict = sum(1 for k in b if k in a and a[k] != b[k])
print('conflicting_translations', conflict)

io.open(r'D:\tmp\overlay_manual5.tsv', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('wrote overlay_manual5.tsv')
