# 《素晴日》新版Nintendo Switch高清移植：第141轮

日期：2026-10-23。工程根目录：`D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns`。

## 本轮任务与实际成果

本轮不是降低画质换运行速度，也不是对原PC汉化进行润色。从第140轮权威`P651`的**172份原GPL2 C99模块＋18份原生Switch SDL2/libnx/GPU/PCM/SD适配＋198项LLVM局部未解析符号**继续，优先解决新版中文/日文显示所需的原引擎文本编码状态、真实Switch地区语言、窗口标题和剪贴板转换。原游戏的1280×960高清CG、原OGG及25fps影片、原剧情BP和玩家Save均未修改。

### 一、第173份真正的原GPL2 C99模块：原生共用文本编码器（P902/P652）

直接读取未修改的原GPL2源码：

`07_工具链环境/P419_OpenBGI_最新GPL2_隔离只读参考_未执行未链接游戏/source/src/os/os_common.c`

该源码内建原`OS_SetTextEncoding` UTF8/Shift-JIS模式、原`gOsTextUtf8`文本状态、Shift-JIS多字节起始判断、原汉字和假名UTF8解析、原游戏文件通配符等平台共用功能。**不是新写的兼容假实现**。本轮逐源码SHA-256检查、真实C99→AArch64机器码编译成**35,464字节ELF64 ET_REL Machine183**目标，再使用真实LLVM `ld.lld -m aarch64elf -r`与以前的172原GPL2源码、18份已有Switch SDL2 GPU/音频桥接和所有真实SDK静态库融合。与此前源机器码无重复强符号，**真实解析原缺失的`OS_SetTextEncoding`一项**，局部未解析**198→197项**，没有引入额外新外部符号。当前原GPL2源码互异模块累计**173份**。

同一份原C99源码在Windows主机实际编译为可运行EXE（不是测试一份改写的翻译），执行14条可检查的断言：`Shift-JIS 0x82A0→あ U+3042`、半角假名、`0x5C`应为反斜杠、`CP932→UTF8`、中文`中`/`文`两种UTF-8码点及逐字节保留、UTF8/Shift-JIS模式往返、英文文件扩展名通配符等，全部成功。

脚本：`01_工具脚本/verify_p902_round141_real_original_GPL2_os_common_C99_173_arm64_utf8.py`，实证JSON：`06_测试记录/P652_第141轮_第173份原GPL2公共ShiftJIS_UTF8编码源码原样ARM64编译14宿主测试.json`，ARM64机器码/真实链接与宿主EXE都在`03_脚本工作区/P902_第141轮_原GPL2平台文本编码函数与窗口消息接口源码链接/`。

**重要边界：** 这只使引擎内部原Unicode/Shift-JIS模式及其共享解析器有真实机器码；Switch平台`OS_SjisToCodePoint`等码页查询、字形文件查找、字库栅格化及高分辨率字体界面实机绘制仍待开发，不能把UTF8码点解码成功说成全游戏汉字不缺字。

### 二、第19个真实Switch SDL2桥接：系统语言与中文文本UI（P903/P653）

新增并真实交叉编译为独立AArch64机器码的适配源码：

`03_脚本工作区/P903_第141轮_SwitchSDL2真实语言剪贴板主窗标题与原时钟生命周期/p903_switch_sdl2_locale_title_clipboard_timer.c`

新增并已通过实际SDL2静态库链接的**七种原`bgi/os.h`接口**：

| 原GPL2 OS接口 | 真实适配逻辑 |
|---|---|
| `OS_UiLanguage` | 查询真正SDL2 `SDL_GetPreferredLocales`，按Windows LANGID分别映射日语`0x0411`、英语`0x0409`、简体中文`0x0804`、台湾繁中`0x0404`、香港繁中`0x0c04`、韩语`0x0412`；设备语言不可用时返回未知，不硬编码“日文系统” |
| `OS_WindowSetTitle` | 取得前轮真实P454 SDL renderer对应的`SDL_Window`，调用**原GPL2** `OsCommon_MainTitle`组织主标题；依据本轮原`gOsTextUtf8`原引擎模式，经真实SDL2 `SDL_iconv_string`处理UTF8/CP932，再设置SDL窗口标题；转码失败不把乱码交给窗口 |
| `OS_ClipboardSetText` | 实际SDL2剪贴板写入、正确回传平台失败状态；使用原引擎UTF8/CP932模式，不把CP932中文字节误当UTF8输出 |
| `OS_TimerBeginPeriod` / `OS_TimerEndPeriod` | Switch SDL2无WinMM `timeBeginPeriod`及成对计时分辨率句柄，沿用原GPL2 POSIX后端无句柄生命周期约定；真正的帧间`SDL_Delay`时钟已由上轮`P898`实现 |
| `OS_IdleInit` / `OS_IdleShutdown` | 与原GPL2 POSIX平台无需另行创建休眠句柄的语义相同；不虚称Switch支持Win32 WaitableTimer，真正休眠由前轮的SDL实现 |

本轮用**同一份新增C99源码＋不修改的原GPL2 os_common.c**编译宿主可执行EXE，执行17条不同主机SDL回调断言：包括日语/中文简繁/香港/英文语言映射、无地区时不虚报，主SDL窗口不存在时不设置标题，UTF8中文`中文`标题完整保持，不可用SDL转码拒绝乱码，SDL剪贴板写入失败不假报成功、NULL安全处理以及生命周期初始化调用。SDL回调在宿主测试中仍是fixture；**测试没证明实体Switch的SDL `CP932`转码支持所有汉字、设备Unicode字形完整或界面布局不重叠**。

该模块与**173份原GPL2 C99＋之前18个Switch桥接＋真正SDL2/libnx/EGL/GLES/PCM/CRT/Nouveau SDK静态库**再次执行真实LLVM AArch64部分链接，**把此前197项缺口里的七项全部补上，197→190项，0项新增缺失符号**。源码原SHA不变，静态链接不是完整可启动游戏。

脚本：`01_工具脚本/verify_p903_round141_switch_SDL2_locale_title_Chinese_clipboard_7OS_native.py`，验证JSON：`06_测试记录/P653_第141轮_SwitchSDL2真实中文标题剪贴板首选语言7原OS函数ARM64和17主机断言.json`。

最新真实原生ELF：`03_脚本工作区/P903_第141轮_SwitchSDL2真实语言剪贴板主窗标题与原时钟生命周期/original173_GPL2_19_Switch_SDL2_locale_text_os_sdk_AARCH64_partial.o`，**37,799,320字节**，AArch64 Machine183 ELF64 ET_REL，SHA256核验及**190项真实未解外部全局名清单**在P653记录。同轮的两种宿主可执行检查合计**31条实际断言**（14+17）。

### 三、最终开发门禁与准确续接

本轮最终全量脚本：`01_工具脚本/verify_p904_round141_final_173_original_GPL2_19_Switch_UTF8_127HD_1163.py`。它从前轮真实原GPL2/WaveMaster与Switch GPU/PCM链完整重建，**实际重新执行原PC-HD的127份逐SHA256源检查（总计39,772,982字节）和1,163项历史开发质量断言**，随后再构建第18个真实SDL2全屏接口、第173个未改GPL2公共编码模块和第19个真实Switch语言文本接口；逐个验证AArch64机器文件哈希和全部190项未解符号。最终权威JSON路径：`06_测试记录/P654_第141轮最终_173原GPL2加19Switch中文编码系统语言_127HD_SHA_1163.json`。

**本轮没有推进新的剧情原IPL，准确原剧情主线程续接仍为IPL 225988、PC 0x20E4D。** 后续从P654最新真实173原GPL2源码＋19Switch桥接＋完整SDK真实LLVM机器构件、190项局部未解符号入手，优先做好Switch OS字体字形/CP932查表、文件隔离、真实GPU窗口渲染/完整25fps影片与原OGG音画同步、Joy-Con触屏输入和存档。GL/Nouveau/NIR/C++等剩余未解须做真实SDK依赖分解；**190是该组局部ELF实际未解析的名字数，不是完成一个真正NRO只需190个函数。**

原CG/OGG/电影/玩家Save保持母版SHA不变。真实NS硬件连贯游玩、高画质实机GPU、音频、25fps电影、存档的验证仍未完成；尚未生成可安全安装的完整游戏NRO/NSP，发行状态继续**`BLOCKED_NOT_SAFE_TO_INSTALL`**。项目链接OpenBGI GPL2源码时仍须遵循GPL-2.0-only的发布义务。
