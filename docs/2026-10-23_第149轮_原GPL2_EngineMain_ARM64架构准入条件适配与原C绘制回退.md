# 《素晴日》新版PC高清移植 Nintendo Switch｜第149轮 GPL2 ARM64启动架构适配

工程根目录：`D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns`。日期：2026-10-23。

## 一、真实技术阻塞与安全原则

承接第148轮权威`P674`：**176份原样GPL-2.0-only OpenBGI C99模块＋34个独立Switch libnx/SDL2/GPU/PCM/OFL中文字形/安全SD入口平台目标**，物理AArch64 ELF64 ET_REL机器码**39,469,312字节、剩132项真实未解析全局外部名**。原剧情线程真实IPL 225988/PC `0x20E4D`。原PC 127份1280×960 CG/原OGG/原25fps电影/字体/BP共39,772,982B和玩家Save不改；不能用800×600旧CG“通过”测试。

上轮新Nintendo `main`已经通过真实SD源目录和`ipl._bp`文件检查后，调用保留机器指令未修改的原GPL2主入口`orig`；但上游原`src/sys/engine.c`的`Engine_Main`仍在非WASM机器上强制`Cpu_Detect`/`Cpu_HasCmov`/`Cpu_HasMmx`成功。原`src/sys/cpu.c`依赖**x86 CPUID指令位15（CMOV）和23（MMX）**，Switch属于**AArch64**，正确的原生OS接口`OS_Cpuid`应报告x86 CPUID不可用。若把Intel指令位硬设为真，将出现伪造硬件能力、可能误导Gfx启用x86 SSE/MMX的风险，不能这么做。

## 二、P928／P675：只调整原GPL2引擎一处架构条件，完整源码/机器重链接

**完全保留上游GPL2 `07_工具链环境/P419_OpenBGI_最新GPL2_隔离只读参考_未执行未链接游戏/source/src/sys/engine.c`只读原文件。** 在P928新目录中另复制一份**明确注明GPL-2.0-only的架构适配版**：

`03_脚本工作区/P928_第149轮_ARM64真实非x86启动条件_原GPL2只读架构改版/p928_GPL2_engine_Nintendo_AArch64_cpu_branch_adapted.c`

对照两份源码，**仅原`Engine_Main`的那一行编译条件更改**：从原来的`#if !defined(BGI_WASM)`改为`#if !defined(BGI_WASM) && !defined(BGI_NINTENDO_AARCH64)`；修改前后的`Cpu_Detect`、CMOV/MMX判断及失败弹框**一字不改**，因此Win32/POSIX原x86仍然执行原有的CPU要求，原WASM条件保持原逻辑；仅显式宏`BGI_NINTENDO_AARCH64`下不调用不存在的x86专属启动许可条件。ARM64的`OS_Cpuid`仍保持真实`return 0`，绝不伪装Intel指令支持，`Cpu_HasSse/Sse2()`因此继续返回不可用。

真实原GPL2 `src/gfx/mgr/gfxmgr.c` 的`Gfx_Create`仍依据`Blit_SetSse(Cpu_HasSse())`和`Blit_SetSse2(Cpu_HasSse2())`来选择通用C位图算法而非x86 SIMD。`src/gfx/blit_scale.c`的`Blit_InitMmxTables()`仅生成权重数组，不会在Nintendo ARM64上执行x86 MMX指令。这只是**源码路径/机器符号审查**，并非证明了真Switch屏幕的1280×960逐帧图像或原CG性能。

从修改后的`Engine_Main`提取**确切CPU条件源片段**，宿主以两种编译设置分别生成可执行程序并运行：ARM分支5项（x86 CPUID不可用时允许继续、根本不询问或伪报x86检测/弹窗，静态AMD/Intel条件不影响ARM）；原x86分支5项（没有CPUID/CMOV/MMX三种失败条件仍被拒绝，特性真正齐全才允许通过，失败按原逻辑弹错误框），共**10项宿主断言全部PASS**。真实`zig cc -target aarch64-freestanding-none -DBGI_NINTENDO_AARCH64`交叉编译得到新的**59,368B AARCH64 ELF64 Machine183 `Engine_Main`目标**，逐符号检查已不再引用原`Cpu_Detect/Cpu_HasCmov/Cpu_HasMmx`作为启动条件，但保留音频/游戏选择/真实SDK依赖。

本轮重链接不是对已包含旧`Engine_Main`的39MB ELF简单叠加重复定义，也不是隐藏原游戏指令：从**P910真正173份原GPL2＋24份Switch平台**且尚未包含引擎入口的GPL2机器码重新开始，加上**2份未改GPL2源码`main.c`、`hvl.c`及1份明确为新架构适配的GPL2 `engine.c`**，原GPL2的`main`目标仅在ELF符号表把`main`重命名为同长度的`orig`（机器指令和重定位完全不改），再真正加入全部已有的10个Switch平台增量目标，形成**175份未修改原GPL2源码＋1份GPL2架构适配引擎源码＋34份独立Switch原生接口模块**。以官方libstdc++/libsupc++/libm/libgcc、SDL2、libnx和newlib静态库实际LLD局部链接。原始`main`/新安全入口`main`/新ARM64 `Engine_Main`和完整GPL2 VmMain符号真正同在一个物理AArch64 ELF64 ET_REL里；前后**132项未解全局名集合完全相同**，任何尚未实现的电影、NIR、OS IPC或文件操作都没有伪造成功。

单独开发脚本`01_工具脚本/verify_p928_round149_architecture_safe_original_GPL2_EngineMain_full_native.py`，证据`06_测试记录/P675_第149轮_175原GPL2与1份真实架构适配Engine_Main及34Switch_10宿主ARM64.json`。最新增量物理ELF：

`03_脚本工作区/P928_第149轮_ARM64真实非x86启动条件_原GPL2只读架构改版/P928_175_unmodified_plus_1_GPL2_AArch64_adapted_engine_34_Switch_relinked.o`

真实**39,468,112字节**，SHA256=`286b2b29b8df6a403cc2243c2d609feab2dd36971c82ed9059749d6cb6588722`。所有上游GPL2只读原件、原PC高清母版、脚本和玩家Save都保持原SHA未改。注意源代码许可：这**1份是修改过的GPL-2.0-only C99**，不能再把整个集合称作“176份全部未改的GPL2源码”，发布时需要保留GPL2许可声明及对应修改说明。

## 三、完整历史回归、已知不足与下轮续接

第149轮最终统一质量门禁脚本：

`01_工具脚本/verify_p929_round149_final_archsafe_engine_fullHD127_1163_GPL2.py`

此脚本会先**真实重新执行**上轮P927完整原PC媒体**127份逐SHA256**、原有**1,163项历史开发断言**、前轮安全SD＋IPL强Switch主入口宿主测试与全部34平台对象，再重新编译本轮明确修改的一行GPL2 C99架构适配源码和**ARM/x86两组共10条**CPU分支宿主测试，最后重新链接SDK ARM64、逐符号核对132项未解、校验原GPL2母版引擎与修改版的SHA及全部源平台机器文件SHA。

权威最终记录：`06_测试记录/P676_第149轮最终_175原GPL2加1架构适配EngineMain及34Switch_127高清SHA_1163质量.json`。**只有P676真实生成且PASS才能宣称第149轮全量完成。** 仍未验收的包括：用户Switch实体机HOS Applet和SDL视频/音频实际初始化、原新版CG GPU帧渲染/CJK字幕、OGG和25fps影片声画、Joy-Con/触屏和完全隔离的Save；未解析函数至少132项，尚无完成实机验收的安装包NRO/NSP，发行门禁保持`BLOCKED_NOT_SAFE_TO_INSTALL`。下轮建议从P676继续优先处理真实`Engine_Main`后续依赖并独立调试SDL2 GPU/NIR与原OGG电影/Save，而非继续反复追求无意义的对象总数。

## 四、最新第149轮全链P929/P676已正式通过

上述最终脚本已**实际运行147.4秒并生成权威`P676`，结果`PASS_P929_ROUND149_REAL_175_UNMODIFIED_PLUS_1_GPL2_AARCH64_CPU_ARCH_ENGINE_34_SWITCH_127HD_1163_DEV_ONLY`**。从原PC 127份新版高清CG、原音质OGG、25fps电影、字体/BP合计39,772,982B物理母版文件的逐SHA256保持不变，到原历史**1,163项开发质量断言全部重跑PASS**，再到前轮P674完整34个Nintendo接口实链接和本轮确切CPU启动源码**ARM5＋原x86五条宿主断言共10条**实际通过。

最新最终物理LLVM链接目标`03_脚本工作区/P928_第149轮_ARM64真实非x86启动条件_原GPL2只读架构改版/P928_175_unmodified_plus_1_GPL2_AArch64_adapted_engine_34_Switch_relinked.o`为**39,468,112B真ARM64 ELF64 ET_REL Machine183**，SHA256=`286b2b29b8df6a403cc2243c2d609feab2dd36971c82ed9059749d6cb6588722`；**仍有132项真实未解全局外部符号**，原GPL2上游源码SHA、原游戏母版资源和玩家Save零改动。新ARM64 `Engine_Main`不再要求不可能存在的x86 CMOV/MMX指令，真正`OS_Cpuid`仍不伪造x86能力；其余软硬件无法完成验证的内容依旧未称为可玩。

**下轮唯一续接权威**`06_测试记录/P676_第149轮最终_175原GPL2加1架构适配EngineMain及34Switch_127高清SHA_1163质量.json`：原故事执行状态仍IPL**225988**、PC **0x20E4D**；175份原GPL2源码＋1份明确修改的GPL2 ARM64 `Engine_Main`＋34份Nintendo桥接；132项未解。继续发版阻止状态`BLOCKED_NOT_SAFE_TO_INSTALL`，设备HOS/NRO、原OGG/电影、HD画面和存档必须以后独立真实验收。
