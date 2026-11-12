# -*- coding: utf-8 -*-
"""P1492: append ASET (icon + control.nacp) to the current arrow-cursor NRO.

Layout follows the official switchbrew elf2nro source vendored in this project:
  AssetHeader = "ASET" + u32 version + 3 x AssetSection{u64 offset;u64 size}
  offsets are relative to the asset area start (4-aligned end of the NRO data)
"""
import io
import json
import os
import struct

PROJ = r'D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns'
SRC = os.path.join(PROJ, r'05_NS测试构建\P1460_第290轮_REBUILD_BASELINE\Subahibi_PC1647_P1460_REBUILD_BASELINE.nro')
ICON = os.path.join(PROJ, r'03_脚本工作区\P1482_图标与名称元数据\icon.jpg')
NACP = os.path.join(PROJ, r'03_脚本工作区\P1482_图标与名称元数据\control.nacp')
OUT = os.path.join(PROJ, r'05_NS测试构建\P1492_带图标与名称的当前NRO\Subahibi_arrow_cursor_icon.nro')

data = bytearray(open(SRC, 'rb').read())
icon = open(ICON, 'rb').read()
nacp = open(NACP, 'rb').read()
assert icon[:2] == b'\xff\xd8', 'icon must be JPEG'
assert len(nacp) == 0x4000, 'nacp must be 0x4000'
assert b'ASET' not in data, 'source already has ASET'

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

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'wb').write(bytes(out))

raw = open(OUT, 'rb').read()
i = raw.find(b'ASET')
io_, isz = struct.unpack_from('<QQ', raw, i + 8)
no_, nsz = struct.unpack_from('<QQ', raw, i + 24)
print('out bytes      ', len(raw))
print('ASET at        ', hex(i))
print('icon  rel/size ', io_, isz, 'jpeg', raw[i + io_:i + io_ + 2] == b'\xff\xd8')
print('nacp  rel/size ', no_, nsz, 'name', raw[i + no_:i + no_ + 18].decode('utf-8', 'replace'))
print('prefix unchanged', raw[:len(open(SRC, 'rb').read())] == open(SRC, 'rb').read())
json.dump({'out': OUT, 'bytes': len(raw)}, io.open(os.path.join(os.path.dirname(OUT), 'report.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('OK')
