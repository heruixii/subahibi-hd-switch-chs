#!/usr/bin/env python3
"""Build the runtime-extensible private translation overlay (SBCHS004).

Usage:
    python p1470_build_extra_dictionary.py pairs.tsv out.bin

`pairs.tsv` is UTF-8, one `original<TAB>translation` pair per line; `#` starts
a comment line. The original must be encodable as CP932 and the translation as
GBK; entries are sorted by the CP932 byte order because the on-device helper
does a binary search over the raw bytes.

Container (little endian):
    "SBCHS004" | u32 version=1 | u32 count | u32 crc32(body) | body
    body entry: u16 len(original) | u16 len(translation) | original | translation

The helper validates magic/version/count/CRC32 and then still requires an exact
original-string match, so a damaged or wrong file can only fall back to the
original Japanese text.
"""
from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path

MAGIC = b"SBCHS004"
VERSION = 1
MAX_ENTRIES = 200_000
MAX_LEN = 512


def read_pairs(path: Path) -> dict[bytes, bytes]:
    pairs: dict[bytes, bytes] = {}
    conflicts: list[str] = []
    for lineno, raw in enumerate(path.read_text("utf-8-sig").splitlines(), 1):
        line = raw.strip("\r\n")
        if not line or line.lstrip().startswith("#"):
            continue
        if "\t" not in line:
            raise SystemExit(f"line {lineno}: missing tab")
        jp, cn = line.split("\t", 1)
        if not jp or not cn:
            raise SystemExit(f"line {lineno}: empty field")
        try:
            jb = jp.encode("cp932")
            cb = cn.encode("gbk")
        except UnicodeEncodeError as exc:
            raise SystemExit(f"line {lineno}: {exc}") from exc
        if len(jb) > MAX_LEN or len(cb) > MAX_LEN:
            raise SystemExit(f"line {lineno}: field over {MAX_LEN} bytes")
        if b"\x00" in jb or b"\x00" in cb:
            raise SystemExit(f"line {lineno}: embedded NUL")
        if jb in pairs and pairs[jb] != cb:
            conflicts.append(jp)
        pairs[jb] = cb
    if conflicts:
        raise SystemExit(f"{len(conflicts)} conflicting originals, e.g. {conflicts[0]!r}")
    if not pairs:
        raise SystemExit("no pairs")
    if len(pairs) > MAX_ENTRIES:
        raise SystemExit("too many entries")
    return pairs


def build(pairs: dict[bytes, bytes]) -> bytes:
    body = bytearray()
    for jb, cb in sorted(pairs.items()):
        body += struct.pack("<HH", len(jb), len(cb)) + jb + cb
    header = MAGIC + struct.pack("<III", VERSION, len(pairs), zlib.crc32(bytes(body)) & 0xFFFFFFFF)
    return header + bytes(body)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2
    src, dst = Path(argv[1]), Path(argv[2])
    pairs = read_pairs(src)
    blob = build(pairs)
    dst.write_bytes(blob)
    print(f"entries={len(pairs)} bytes={len(blob)} crc32={zlib.crc32(blob[20:]) & 0xFFFFFFFF:08x}")
    print(f"sha256={__import__('hashlib').sha256(blob).hexdigest()}")
    print(f"installed path: sdmc:/switch/subahibi_pc_native_hd_qa/chs/{dst.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
