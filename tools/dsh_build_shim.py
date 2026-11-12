"""Shim: let mingw gcc/ld write outputs even though the project path is non-ANSI.

The toolchain cannot create files under any path containing CJK characters
(verified: `gcc t.c -o D:\\tmp\\中文\\p.exe` -> ld.exe: cannot open output file).
Reading such paths works fine, so only WRITES need redirecting:

  *  intercept subprocess.run / Popen
  *  for every argument that follows -o (or spells -o<path>), rewrite the
     destination to an ASCII staging file under D:\\tmp\\objstage\\
  *  after the process exits successfully, copy the staged file back to the
     original (Chinese) destination with Python, which handles Unicode paths.

Usage:
    import dsh_build_shim        # installs the patch
    import <target module>; <target module>.main()
"""
import os
import shutil
import subprocess
import sys
import tempfile

STAGE = r'D:\tmp\objstage'
os.makedirs(STAGE, exist_ok=True)

_orig_run = subprocess.run
_orig_popen = subprocess.Popen
_counter = [0]


def _is_ascii(p):
    try:
        p.encode('ascii')
        return True
    except Exception:
        return False


def _stage_path(orig):
    _counter[0] += 1
    ext = os.path.splitext(orig)[1] or '.bin'
    return os.path.join(STAGE, 'o%05d%s' % (_counter[0], ext))


def _rewrite(cmd):
    """Return (new_cmd, [(staged, original), ...])."""
    if not isinstance(cmd, (list, tuple)):
        return cmd, []
    out = list(cmd)
    moves = []
    i = 0
    while i < len(out):
        a = out[i]
        if not isinstance(a, str):
            i += 1
            continue
        if a == '-o' and i + 1 < len(out) and isinstance(out[i + 1], str):
            dest = out[i + 1]
            if not _is_ascii(dest):
                sp = _stage_path(dest)
                out[i + 1] = sp
                moves.append((sp, dest))
            i += 2
            continue
        if a.startswith('-o') and len(a) > 2 and not a.startswith('--'):
            dest = a[2:]
            if not _is_ascii(dest):
                sp = _stage_path(dest)
                out[i] = '-o' + sp
                moves.append((sp, dest))
        i += 1
    return out, moves


def _copy_back(moves):
    for sp, dest in moves:
        if os.path.exists(sp):
            os.makedirs(os.path.dirname(dest) or '.', exist_ok=True)
            try:
                if os.path.exists(dest):
                    os.remove(dest)
            except Exception:
                pass
            shutil.move(sp, dest)


def _run(cmd, *a, **kw):
    new, moves = _rewrite(cmd)
    r = _orig_run(new, *a, **kw)
    if moves and getattr(r, 'returncode', 1) == 0:
        _copy_back(moves)
    return r


class _Popen(_orig_popen):
    def __init__(self, cmd, *a, **kw):
        new, moves = _rewrite(cmd)
        self._dsh_moves = moves
        super().__init__(new, *a, **kw)

    def wait(self, *a, **kw):
        rc = super().wait(*a, **kw)
        if rc == 0:
            _copy_back(self._dsh_moves)
        return rc


subprocess.run = _run
subprocess.Popen = _Popen
subprocess.call = lambda cmd, *a, **kw: _run(cmd, *a, **kw).returncode
subprocess.check_call = lambda cmd, *a, **kw: _run(cmd, *a, **kw).returncode
subprocess.check_output = lambda cmd, *a, **kw: _run(cmd, *a, **kw).stdout

if __name__ == '__main__':
    r = subprocess.run([r'C:\msys64\mingw64\bin\gcc.exe', r'D:\tmp\t.c',
                        '-o', r'D:\tmp\中文\shimtest.exe'], capture_output=True)
    print('rc', r.returncode)
    print('exists', os.path.exists(r'D:\tmp\中文\shimtest.exe'))
