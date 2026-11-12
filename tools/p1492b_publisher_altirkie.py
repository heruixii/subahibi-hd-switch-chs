# -*- coding: utf-8 -*-
"""Rebuild control.nacp with publisher ALTIRKIE, then re-append ASET to the clean NRO."""
import io, os, struct

PROJ = r'D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns'
NACP = os.path.join(PROJ, r'03_脚本工作区\P1482_图标与名称元数据\control.nacp')
SRC = os.path.join(PROJ, r'05_NS测试构建\P1460_第290轮_REBUILD_BASELINE\Subahibi_PC1647_P1460_REBUILD_BASELINE.nro')
ICON = os.path.join(PROJ, r'03_脚本工作区\P1482_图标与名称元数据\icon.jpg')
OUT = os.path.join(PROJ, r'05_NS测试构建\P1492_带图标与名称的当前NRO\Subahibi_HD_CHS.nro')

NAME = '素晴日 HD 汉化版'
PUB = 'ALTIRKIE'
AUTHOR = 'Subarashiki Hibi CHS port'
TITLE_ID = 0x0100A5C0C0FF8000

buf = bytearray(0x4000)
nb, pb, ab = NAME.encode(), PUB.encode(), AUTHOR.encode()
for i in range(16):
    o = i * 0x200
    buf[o:o + len(nb)] = nb
for i in range(16):
    o = 0x2000 + i * 0x100
    buf[o:o + len(pb)] = pb
struct.pack_into('<Q', buf, 0x3000, TITLE_ID)
buf[0x3008:0x3008 + len(ab)] = ab
open(NACP, 'wb').write(bytes(buf))

data = bytearray(open(SRC, 'rb').read())
icon = open(ICON, 'rb').read()
nacp = open(NACP, 'rb').read()
assert icon[:2] == b'\xff\xd8'
assert len(nacp) == 0x4000
assert b'ASET' not in data

file_off = (len(data) + 3) & ~3
if file_off > len(data):
    data += b'\0' * (file_off - len(data))
hdr_size = 4 + 4 + 16 * 3
icon_off = hdr_size
nacp_off = icon_off + len(icon)
hdr = bytearray()
hdr += b'ASET'
hdr += struct.pack('<I', 0)
hdr += struct.pack('<QQ', icon_off, len(icon))
hdr += struct.pack('<QQ', nacp_off, len(nacp))
hdr += struct.pack('<QQ', 0, 0)
out = bytearray(data)
out[file_off:file_off + hdr_size] = hdr
out[file_off + icon_off:file_off + icon_off + len(icon)] = icon
out[file_off + nacp_off:file_off + nacp_off + len(nacp)] = nacp
open(OUT, 'wb').write(bytes(out))

raw = open(OUT, 'rb').read()
i = raw.find(b'ASET')
no_, nsz = struct.unpack_from('<QQ', raw, i + 24)
name = raw[i + no_:i + no_ + 40].split(b'\x00')[0].decode('utf-8', 'replace')
pub = raw[i + no_ + 0x2000:i + no_ + 0x2000 + 40].split(b'\x00')[0].decode('utf-8', 'replace')
io.open(r'D:\tmp\nacp_result.txt', 'w', encoding='utf-8').write(
    'bytes=%d aset=%s name=%s publisher=%s' % (len(raw), hex(i), name, pub))
print('done', len(raw))
