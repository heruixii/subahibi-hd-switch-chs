# 《素晴日》新版 Nintendo Switch 移植：第136轮

日期：2026-10-23。项目目录：`D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns`。

第136轮主要由 **P878（原生产调度器源码实际执行）、P879（原引擎与9份Switch桥接的真实ARM64部分链接）**组成，完整开发质量检查由P880/P630负责。发行状态仍为 **`BLOCKED_NOT_SAFE_TO_INSTALL`**：未生成完整、安全可安装且实机验证的Nintendo Switch NRO/NSP。

## 一、GPL2源 `Vm_RunPass` 真正走八原BP列表，而非替代调度循环

继承前轮真实原主线程 **IPL225988、PC=0x20E4D**，八个真实原GPL2编译BP线程的六次受控调度已实际执行 **1748条子线程源码C99指令**；其中原动画管理主线程通过 `80:44` 派生了第八个 `anmmngrs._bp`。上一轮又将原GPL2 `src/vm/sched.c` 的**完整、未经更改的生产 `Vm_RunThread` 函数体**作为原C99函数真实编译执行，验证真实第六子线程（`mtnmngr._bp`）原IP637/SP30在等待时不取指，到期后原opcode `00 PushI8`真执行、IP639/SP31。

**P878/P628：** 从原 GPL2上游 `src/vm/sched.c` 再逐字提取**生产 `Vm_RunPass` 函数体**；同时保留同一源码的 `Vm_RunThread` 和源 `Thread_FindById`。`Vm_RunPass` 使用实际 GPL2 `Thread_Next` 遍历八个存活的 `Thread_t` 链表节点，按原独占线程标志 `gExclusiveOn/gExclusiveThread` 限制本次安全试验中其他七个原 BP 的指令取用：

1. 由隔离fixture在原`mtnmngr._bp`（原真实Thread_t ID6，原IP637/SP30）安装**原 GPL2 `WaitTimer_New`+`Thread_SetWait`**，计时7ms。
2. 第一次调用**源生产 `Vm_RunPass()`**：按链表访问八个节点；七个非独占原线程未抓取BP指令；原ID6使用真实 `Thread_PollWait` 判断仍在等待，**0条原BP字节码抓取**，八个线程IP/SP/FP都不改变。
3. 对**隔离测试的虚拟时钟**明确推进7ms。这不是游戏原时钟、NS OS时钟或实际剧情演出。
4. 再次调用**相同的源生产 `Vm_RunPass()`**：第六线程真实 `Thread_PollWait` 返回完成，源码自己的`Thread_FetchOp`和`Opcode_PushI8`执行原编译BP `00`，IP **637→639**、SP **30→31**，其余七个原BP的IP、SP、FP完全不变。

原版 `Vm_RunPass`、`Vm_RunThread`、`Thread_FindById` 的C99函数体没有修改；所测试是正常结束与独占等待这条调度路径，**线程终止/切换/重启/退出的 `3/4/5/6` 返回分支仍没有覆盖**，测试隔离宿主对此类未接通的终止分支采用失败即中止防护。**未运行完整 `VmMain` 或`Vm_FrameServices`；不代表已经接通真实GPU/音画/输入/存档。**

可执行原C99编译/运行证据：`01_工具脚本\verify_p878_round136_exact_original_GPL2_Vm_RunPass_eight_child_exclusive.py`，`06_测试记录\P628_第136轮_原GPL2生产Vm_RunPass真实8BP独占等待阻塞恢复与原指令执行.json`，宿主运行文件/日志在`03_脚本工作区\P878_*`。

## 二、150份真正原GPL2引擎机器码＋9份真正Switch ARM64桥接实际合并链接

上一轮P875/P625已经实际将**150份未经修改的GPL2 C99 ARM64 ELF64 ET_REL 原机码目标**与5份不同的Switch SDL2/libnx适配目标真正LLVM `ld.lld -m aarch64elf -r` 无重复全局定义地部分链接，生成 **6,696,720字节**AArch64部分链接ELF。五桥接定义了15种原 `OS_*` ABI符号，引入21种SDL2/libnx外部符号，当前该局部组合有264种未解析符号。

**P879/P629** 再把4份**此前已真实独立编译**的ARM64 SDK目标物理合并到上述ELF，保持原150份C99引擎目标完全不变：

| 新增原生Switch适配对象 | 真正新增原GPL2调用接口 |
|---|---|
| SDL2互斥锁 | `OS_LockCreate`, `OS_LockDestroy`, `OS_LockEnter`, `OS_LockLeave` |
| SDL2线程 | `OS_ThreadStart`, `OS_ThreadJoin` |
| 私有SD只读根目录映射 | `OS_ExeDir`, `OS_SetCurrentDir`，以及游戏目录辅助导出 |
| 私有SD C盘路径映射基础 | `P473_MapBGIPath`，为真实只读路径适配提供定义 |

真实SDL2/libnx/SD桥接来源：`03_脚本工作区/P473_*` 中p479/p481/p475的四份独立AArch64 `.o`。校验每个目标文件头部为**ELF64 ET_REL、AArch64 Machine183**，验证原`inc/bgi/os.h`的ABI函数名、不允许已合并原引擎或前面桥接有重复强全局定义。随之再次调用**真 `ld.lld -m aarch64elf -r`**，真实产物及符号清单如下：

- 引擎模块（未经修改的GPL2 C99源）：**150份**。
- Switch真实SDK/SDL2/SD只读桥接目标：**9份不同ELF64**（前5＋本轮4）。
- 本轮新解析之前264种未解析中的**8种**；新引入**7种**真实SDL2/其他依赖；同一局部链接口径的剩余外部符号**263种**。
- 新实际部分链接文件 **6,724,384字节**、SHA256和真实剩余符号清单已保存。

产物：`03_脚本工作区\P879_第136轮_原150GPL2与9真Switch_SDL2_libnx桥接增量真实LLVM链接\original150GPL2_9_real_switch_native_SDL2_libnx_arm64_LLD_partial_ELF64_ET_REL.o`。脚本：`01_工具脚本/verify_p879_round136_150GPL2_9_switch_native_objects_SDL2_LLD.py`。权威测试 `06_测试记录/P629_第136轮_原150GPL2加9原生Switch_SDL2_libnx桥接真实AARCH64链接.json`。

注意：263个剩余缺失符号不仅是原引擎接口，也包括新引入的SDL2、libnx及通用运行库符号。上述是**真静态机码部分链接，但不是最终Nintendo NRO/NSP链接、不是SDL2/libnx在实机运行的凭据**。所涉数据路径只能用于用户自己的合法资产和私有SD安全区域，严格不修改PC商业来源素材和存档。

## 三、高清资源品质、开发测试与后续计划

本轮最终脚本 `01_工具脚本/verify_p880_round136_final_production_Vm_RunPass_9Switch_127HD_1163.py` 重新执行前轮完整质量链及P878/P879，对以下项目做真实质量复核：

- PC原**127份**PNG/OGG/电影/字体/BP等高清源资源 SHA256逐项不变、总计**39,772,982字节**；原RGB32 BG4 bitmap128和Mode5 sprite33仍为**1280×960**（没有将新CG压成800×600）。
- 重新运行**1163项历史开发质量断言**，原PC商业素材及用户玩家存档不被修改。
- GPL2原八BP受控六轮源执行1748条＋**原生产`Vm_RunPass`两次安全测试**；真实阻塞不抓取码、到期后原BP `00` 指令正常执行。
- 重新编译核验150份原GPL2 ARM64机器码；实际合并9份独立Switch SDL2/libnx/SD ARM64桥接目标，核验AArch64 ELF+SHA与263个剩余真实外部符号。

第136轮综合开发质量结果：`06_测试记录/P630_第136轮最终_原GPL2生产Vm_RunPass真执行_150加9Switch桥接ARM64链接_127HD_SHA_1163.json`。

**下一轮优先事项：** 在原主线程IP**225988／PC0x20E4D**和P628的八BP实际状态上，继续验证原生产 `Vm_RunPass` 的**正常多线程执行、线程调度返回码3/4/5/6、消息同步**，真正接入`Vm_FrameServices`及SDL2/libnx图形/音频/手柄/Save。然后从P629的263项真实外部依赖清单逐批加入OS后端和相应库，最终连成可运行NRO/NSP并在NS实机做全尺寸音画、存档与稳定性验收。没经过实机前发行状态仍然`BLOCKED_NOT_SAFE_TO_INSTALL`。

## 四、进一步实际链接Nintendo SDK自带的原生SDL2和libnx静态库（P881/P631、P882/P632）

在第136轮P630完整QA全部通过后继续直接推进，未停止在“桥接目标能部分链接”阶段。隔离SDK本身存在**真正的Switch AArch64 静态库**：`portlibs/switch/lib/libSDL2.a`（**10,039,308字节**）与`libnx/lib/libnx.a`（**26,759,124字节**）。在只读核验两库及既有P879原GPL2+9桥接合并ELF SHA的前提下，P881调用真`zig ld.lld -m aarch64elf -r`，使用`--start-group`将两份真正SDK库加入**原150 GPL2源码机器码＋9份桥接目标**的真实AArch64部分链接。

- LLVM **确实成功完成链接**，输出物理**22,682,080字节**的真正 ELF64 ET_REL Machine 183（AArch64）机器码目标；源码、原玩家Save、SDL2 SDK包与libnx SDK包均未修改。
- 与加入真实SDL2/libnx库之前的P629同口径相比，原来缺失的**27项SDL2/libnx调用**全部由真实SDK归档提供，包括`SDL_CreateMutex`、`SDL_CreateThread`、`SDL_PollEvent`、`SDL_RWFromFile`、`SDL_GetTicks`与`svcGetInfo`等，未残留`SDL_*`名字。
- 实际静态库还引入**138项新的传递依赖**（EGL/OpenGL、C库、math、libnx运行时、POSIX兼容层及链接脚本符号等），因此本次**带SDL2与libnx库的部分链接范围当前还有374项外部未解符号**，并非P629阶段的263项，也不代表Switch操作系统还“差374个功能”。新增传递依赖是 SDK 静态库真实实现被拉入后的正常结果。
- **未达成最终NRO或NSP链接**；特别是SDL2窗口/GPU的EGL运行库、CRT与Switch程序入口仍有待接通，OGG/25fps视频以及Joy-Con/HID、Save均未完成NS实机全程音画验收。

源可复验脚本：`01_工具脚本/verify_p881_round136_real_Switch_libnx_SDL2_static_archives_LLD.py`。产物：`03_脚本工作区/P881_第136轮_150GPL2九桥接与真实SDK_SDL2_libnx归档链接/original150_GPL2_9Switch_plus_true_SDL2_libnx_static_archives_lld.o`及残留374项的真实ELF符号清单。测试结果`06_测试记录/P631_第136轮_原150GPL2加9桥接真Switch_SDL2与libnx静态SDK归档_LLVM实链接.json`。

**补充最终QA P882/P632**没有无谓再次重跑长达百秒的历史完整质量链，而是验证本轮已实际重新执行并PASS的**P630全套127源HD SHA与1163历史开发测试**及P628/P629原真实生产调度/桥接链接，然后**再次实际运行P881静态SDK链接**，核验所有ELF/SDK归档源SHA和真实374项残留符号；状态`PASS_P882_..._DEV_ONLY`。最终补充质量记录为`06_测试记录/P632_第136轮SDK补充最终_生产Vm_RunPass_150GPL2九Switch及真SDL2_libnx归档_127HD_1163.json`。

**准确下一续接点更新：** 原主线程IPL225988/PC0x20E4D、八原BP的原生产`Vm_RunPass`验证见P628；原150模块+9桥接见P629，**加入真正SDL2/libnx SDK静态库后的最新局部链接和374项缺口则以P631/P632为准**。下一轮优先核对隔离SDK已有EGL/GLES/CRT/目标链接脚本和真实最终NRO入口条件，同时推动未覆盖的原线程消息/帧服务与实机端画面、音频、视频、存档。没有Nintendo实机可玩验收不得发布。
