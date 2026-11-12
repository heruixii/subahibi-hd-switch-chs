"""Run a build module with the mingw output-path shim installed."""
import importlib
import sys

sys.path.insert(0, r'D:\tmp')
sys.path.insert(0, r'D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns\01_工具脚本')

import dsh_build_shim  # noqa: F401  (installs subprocess patch)

modname = sys.argv[1]
m = importlib.import_module(modname)
m.main()
