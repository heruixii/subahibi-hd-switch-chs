# 《素晴日》新版 Nintendo Switch 高清移植｜第137轮

日期2026-10-23，工程：`D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns`。

**第137轮目标：在已能实际通过原 GPL2 生产 `Vm_RunPass` 的基础上，进一步链接真正的Switch SDK图形和C运行库，并补齐原 `Vm_FrameServices` 直接调用的原引擎机器码。** 仅限开发阶段隔离验证；**尚不能安装，更不代表真正的NS高清GPU/OGG电影音画播放完成**。发行状态：`BLOCKED_NOT_SAFE_TO_INSTALL`。

## 一、在原引擎＋9桥接基础上真链接EGL、GLESv2、CRT

前轮 P881/P631 已真实生成 `22,682,080 B` 原 `150` 份未经修改GPL2 C99 AArch64 ELFs + `9`份Switch SDL2/libnx/只读SD适配＋实际SDK `libSDL2.a`、`libnx.a` 的 LLVM LLD 部分链接，真实剩余**374种**全局符号。它不是NRO/NSP。

P883/P633 在保持前述二进制SHA一致且全部原媒体只读的前提下，增加并实际交给LLVM `ld.lld -m aarch64elf -r` 的Switch SDK静态归档如下：

1. 图形接口 `libEGL.a`、`libGLESv2.a`、`libglapi.a`；Nouveau图形驱动 `libdrm_nouveau.a`。
2. 压缩库 `libz.a`。
3. C运行库 `libc.a`、`libm.a`、`libpthread.a`、`libsysbase.a`、`libnosys.a`。
4. GCC ARM64内核库 `libgcc.a`。

这**11份真实SDK静态库**全部保留原SHA，实际LLVM部分链接返回成功，生成**37,138,344字节**真实Machine183 AArch64 ELF64 ET_REL开发机器码。与加入这些库前的374未解符号相比较，**162个旧符号被实际解析，新引入59个图形/驱动/C++等传递依赖**，当前这个链接阶段真实剩余**271项**。EGL和pthread原未解析函数现在全部有定义；仍有124项`OS_*`和27项`Wm_*`窗口消息接口尚无合适的Switch实现。

P633和其真实日志、SHA、271完整符号清单：`01_工具脚本/verify_p883_round137_true_Switch_sdk_EGL_GLES_CRT_pthread_ARM64_link.py`，`03_脚本工作区/P883_第137轮_真正Switch_EGL_GLES_CRT完整SDK静态链接探索/`。

## 二、原GPL2生产`Vm_FrameServices`仍须真实平台服务，不可空实现

此前P878/P628已在八个真实原版私有BP `Thread_t` 上执行了未经修改的原GPL2生产 `Vm_RunPass`，真正完成独占线程的阻塞、隔离测试定时器到期后从原IP637按原`00 Opcode_PushI8`续执行至IP639；但测试虚拟时钟**不是游戏/任天堂真实时钟**，尚未运行完整`VmMain`。

P884/P634直接读取、逐字校验原GPL2上游 `src/vm/sched.c` 的真正 `Vm_FrameServices` 函数，检查其原始帧服务顺序，包含：

- 原粒子和雨滴更新：`Ptcl_UpdateAll`、`Ptcl_AutoTick`、`Rain_UpdateAll`、`Rain_FrameTick`。
- 原按钮/面板/选取更新：`Panel_GetPollMode`、`Panel_PollAll`/`Panel_PumpAll`、`Target_UpdateAll`。
- 光标、光标精灵和旋钮更新：`Cursor_Update`、`CursorSprite_Update`、`Knob_Update`。
- 输入、显示、影片、调试覆盖：`Input_Poll`、`PresentFrame`、`Movie_Tick`、`Dbg_OverlayPresent`。
- 消息泵与帧间空闲：`PumpMessages`、`Display_FrameIdle`（及原退出异常处理）。

以本轮真SDK EGL/GLES/CRT ARM64部分链接机器码全局符号表逐项反查，原 `Vm_FrameServices` 函数本身确实已经有AArch64定义，其**17个直接被调用的函数中16个在当时有真实GPL2机器码实现**，缺的仅`Dbg_OverlayPresent`。这是函数定义层面的链接核查，**还不能证明实际GPU画面、影片音画、Joy-Con、触屏已实机正常运行**，因为底层`OS_*`/`Wm_*`等仍缺接口。

## 三、继续交叉编译11份原版GPL2调试/窗口覆盖源码→161份

P885/P635读取**未修改**的原 `src/dbg/dbg.c`、`dbgdraw.c`、`dbg_listing.c`、`dbg_pane.c`及原七个调试视图 `bitmaps/log/memory/objects/programs/sound/threads.c`，按相同AArch64 C99目标独立编译，全部生成真实ARM64 ELF64 ET_REL，逐源SHA复核且没有与前150原源码或9桥接发生重复全局定义。再和上述真实SDK 37.14MB ELF进行LLVM真实部分链接：

| 数据 | 真实结果 |
|---|---:|
| 累计未经修改的GPL2 C99原源码ARM64机器码模块 | **161份** |
| 已独立ARM64编译的Switch SDL2/libnx/SD桥接 | **9份** |
| 本轮新增原GPL2调试/覆盖源码 | **11份** |
| 含SDL2/libnx和新增EGL/GLES/CRT等所有静态SDK的LLD部分链接文件 | **37,386,472字节** |
| 对比150原模块SDK基线，真正解析旧缺失符号 | **15项** |
| 新增原调试源码的传递外部依赖 | **8项** |
| 最新161模块范围（含SDK）的实际未解析符号 | **264项** |
| 当前仍缺原`OS_*`操作系统接口 | **128项** |
| `Vm_FrameServices`原17直接调用已有AArch64源机器码定义 | **17/17** |

调试覆盖函数`Dbg_OverlayPresent`的确获得真实原GPL2机器码实现，但还引入了调试窗 `OS_DebugWindow*` 与原显示其他依赖。**264是加入所有静态SDK与原调试器源码的当前局部链接缺失总数，不等同Switch全部最终API数量。** 没有通过空函数抹掉真正缺口。

真机器码：`03_脚本工作区/P885_第137轮_原GPL2未修改调试模块ARM64真链接可消帧服务断点/GPL2_original_161_C99_9Switch_all_sdk_plus_dbg_full_lld_partial.o`。自动脚本：`01_工具脚本/verify_p885_round137_161_original_GPL2_dbg_FrameServices_SDK_ARM64.py`，测试JSON `06_测试记录/P635_*`。

## 四、完整开发门禁及安全边界

本轮权威验收 `01_工具脚本/verify_p886_round137_final_161GPL2_nintendo_EGL_CRT_FrameServices_HD127_1163.py`，实际从前轮P880完整质量链重新验证：

- **127/127**份原PC高清素材SHA256完全一致，共**39,772,982字节**；原1280×960 CG、原OGG、25fps影片、字体和BP不降采样、不重编码，用户Save及商业游戏归档未修改。
- **1163项历史开发质量检查**重新执行，全部PASS。
- 161份原GPL2 C99 AArch64机器码、9份原生Switch桥接目标、真实Switch SDK EGL/GLES/CRT静态归档核对SHA、真部分链接成功。
- 生产 `Vm_FrameServices` 所有**17项**直接原GPL2子系统调用均有原生机器码定义；**未测试它在NS GPU/音频/影片/输入/存档硬件上的实际功能**。
- 最新真正局部链接**264项未解析符号**需继续处理。**尚无可安装、经过真实Switch测试的NRO/NSP完整游戏。**

第137轮最终质量记录：`06_测试记录/P636_第137轮最终_161原GPL2模块9Switch桥接真EGL_GLES_CRT链接_127HD_1163.json`。该门禁PASS是开发验证PASS，不意味着发包许可；发行仍`BLOCKED_NOT_SAFE_TO_INSTALL`。

## 五、下一轮准确续接

原剧情主线程真实IPL **225,988，`PC=0x20E4D`**，8个原BP安全调度现场见P628。**最新链接入口以P635/P636为准**：161份原GPL2源码＋9原生Switch桥接＋SDL2/libnx/EGL/GLES/CRT等真实SDK归档；AArch64 ELF64部分链接文件37,386,472字节，剩余264项真实外部符号（其中`OS_*`128项）。下一阶段优先实现最小正确的Switch独立窗口/图形/输入/音频/文件平台后端，使生产`Vm_FrameServices`能在真帧循环中接受正当SDL2/libnx事件，而不是只做源码符号链接；然后验证完整NRO/NSP生成和Switch全高清音画同步、手柄、存档。不得跳过未知原BP指令或冒充实机进度。

## 六、第137轮续推进：第十份真实Switch高清SDL2视窗映射目标（P887/P637和P888/P638）

本轮又进一步使用**此前真实独立编译、且具备ARM64 ELF64 Machine183格式**的SDL2高清几何和呈现桥接对象 `p440_true_original_HD_renderer_geom_AARCH64_ET_REL.o`，其中包含真正的 `P441_BeginBlackLetterboxedFrame`、`P441_ComputeHDViewport`、`P441_DrawOriginalRGBA1280Texture`、`P441_MapWindowPointerToOriginal`、`P441_PresentFrame`机器码导出。这些函数名称表示设计用途，不能直接认定Switch屏幕上已经出现图片。

P887再次调用真正 LLVM `ld.lld -m aarch64elf -r`，在原**161份GPL2真实源码＋9份Switch桥接＋EGL/GLES/SDL2/libnx/CRT SDK静态库**基础上加入此第10份桥接，并使用真实SDK的`libSDL2.a`满足相关接口。原引擎和SDL2导出均无强符号重复；`P441_MapWindowPointerToOriginal`从原未解项实际获得定义，且未引入额外外部依赖，故最新局部组合未解析**264→263项**。

当前准确物理构件大小是 **37,394,528字节**、真正AArch64 ELF64 ET_REL；路径：`03_脚本工作区/P887_第137轮_原高清SDL2映射加入161源码10桥接实链接/real_GPL2_161_original_C99_10_Switch_SD_SDL2_EGL_SDK_geometry_lld.o`，有真实SHA及完整263项未解符号清单。测试脚本：`01_工具脚本/verify_p887_round137_161GPL2_10Switch_SDL2_HD_geometry_LLD.py`，记录 `06_测试记录/P637_*`。

**权威最新阶段收口为P888/P638**：真实再执行P887部分链接，精确验证机器码SHA与263项符号，同时交叉核对本轮**已实际完整重新执行**的P636 127/127项原PC-HD SHA和1163项历史开发质量PASS（P888不重复假称又跑了一次百秒历史链）。文件：`06_测试记录/P638_第137轮最终补充_161原GPL2_10Switch真SDK高清视窗链接_127HD_SHA_1163.json`，状态`PASS_P888_..._DEV_ONLY`。下一轮因此以**P637/P638：161原GPL2 C99＋10个原生Switch桥接＋真实SDK、263项未解、37,394,528字节ARM64 ELF**为准；不再沿用上文P635的9桥接/264作为“最新”。真实Switch GPU、原OGG与电影、手柄触摸、Save和可安装NRO/NSP尚未成功完整验收，**发行仍`BLOCKED_NOT_SAFE_TO_INSTALL`**。
