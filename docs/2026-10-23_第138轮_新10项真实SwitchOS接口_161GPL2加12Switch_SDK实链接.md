# 《素晴日》新版 Switch 高清移植：第138轮

日期：2026-10-23；工程根目录：`D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns`。

此轮目标：从上一轮 `P638` 的**161份原GPL2 C99 ARM64模块＋10份已有Switch适配对象＋SDL2/libnx/EGL/GLES/CRT真实SDK归档**继续，不再单纯增加“编译次数”，而是实际编写、机器码链接和可执行测试**两个新增的Nintendo平台后端源码文件**，填补原 `inc/bgi/os.h` 的真实函数定义。原PC高清CG、OGG、电影、字体、BP及玩家Save始终保留原字节；不把新版CG缩成800×600。

## 一、在Switch ARM64和宿主上实际测试5项CPU/SDL2时钟/显示ABI（P889/P639）

**新增加的真实平台源码**：`03_脚本工作区/P889_第138轮_SwitchSDL2真实性能时钟显示及ARM64非x86CPU后端/p889_switch_sdl2_cpu_clock_display.c`；未修改任何上游 GPL2 源码。

| 原 GPL2 API | Switch SDL2/libnx实现和行为 |
|---|---|
| `OS_Cpuid` | ARM64不支持x86 CPUID，按原 `os.h` 不支持的返回约定报告不可用，输出寄存器清零；不虚报x86性能 |
| `OS_ReadTsc` | 不冒充x86 `RDTSC`，按原注释返回0；实际计时另用SDL2 |
| `OS_PerfCounterNs` | 真正调用目标平台 `SDL_GetPerformanceCounter/Frequency`，用128位中间数转换为纳秒；零频率、空指针及纳秒溢出均安全失败，不使用测试虚拟时钟替代游戏时钟 |
| `OS_DisplayAdapter` | 使用真正SDL2运行时视频驱动名字；SDL2尚未初始化时返回未知，版本数组归零，不捏造 GPU/驱动版本 |
| `OS_MouseButtonsSwapped` | Nintendo Switch不存在Win32全局左右键交换设置，按原含义返回不交换；真正Touch/Joy-Con映射另在HID处理 |

真实 `zig cc -target aarch64-freestanding-none` 生成 **7,848B** 的ARM64 ELF64 Machine183对象，与前161份GPL2+10Switch SDK链接时真正补上5项原缺失接口。纳秒的128位整数除法引入 `__udivti3`，随后再使用**真实ARM64 `libgcc.a`** 完成此依赖，不留伪造实现。

另将**完全同一份新增C99源**在Windows宿主实编译成可执行EXE，模拟的仅是SDL2平台时钟/驱动返回值，不是原游戏脚本。主机断言覆盖不可用x86指令、SDL时钟频率1000Hz与1GHz、频率0、64位溢出、NULL、SDL未初始化、实际视频驱动名/缓冲截断等边界，运行成功；这个测试**不等于已在Switch硬件上验证真实帧时钟**。机器码SHA和宿主日志见`P639`。

## 二、屏幕/窗口/鼠标焦点与真实SDL坐标转换（P890/P640）

新增源：`03_脚本工作区/P890_第138轮_SwitchSDL2原OS屏幕和视口焦点坐标适配/p890_sdl2_mouse_focus_screen.c`。原版OS.h额外获得5种可移植的真实SDL2支持：

- `OS_WindowActive`：按真实SDL2键盘焦点报告窗口激活状态；无焦点绝不虚报。
- `OS_CursorGetPos`：使用SDL2实际全局鼠标坐标。
- `OS_CursorSetPos`：优先请求SDL2真实全局warp；平台不支持时对已获得的真实SDL鼠标/键盘焦点窗口采用真正的本地warp；窗口不存在则不注入虚构消息。
- `OS_ScreenToClient`、`OS_ClientToScreen`：从实际SDL窗口坐标得到屏幕/客户区变换，未知窗口不编造偏移，极限整数进行安全钳位。

同一份C99源在Windows上通过**12项**可执行SDL焦点、坐标往返、全局Warp回退和防溢出主机断言；另作为真实AArch64 ELF64机器码成功编译，真正链接SDL2.a至最新引擎后解析已有的 **3项**未解析OS函数（另外2个API在本阶段真实已有导出但之前尚未被引用）。未引入新的外部依赖。P640记录源/ELF/SDL2 SDK的SHA和实际链接清单。

**两组新增平台桥接源码合计10项原OS API，实际解决8种过去未解析的原引擎符号**；合计可执行测试断言数需要以C99 fixture源代码中真实 `must()` 调用个数为准（第一组14，第二组12，合计26），不要把平台SDL2回调fixture当成任天堂实机图形/输入已验证。

## 三、最新真实链接状态与剩余后端任务

P889/P890再次执行真正`zig ld.lld -m aarch64elf -r`并核查全局符号、真实ELF机器码及链接SHA，获得：

| 当前最新开发构件 | 结果 |
|---|---:|
| 互异未经修改的原GPL2 C99 AArch64引擎模块 | **161份** |
| 独立原生Switch SDL2/libnx/SD/高清屏幕桥接模块 | **12份** |
| 真正的Switch平台SDK静态归档 | SDL2、libnx、EGL、GLES2、Nouveau、libc、libm、pthread、zlib、libgcc等 |
| 新增OS.h接口真实导出 | **10项** |
| 相对第137轮真实未解析原符号减少 | **8项** |
| 当前真实ARM64 ELF64 ET_REL部分链接大小 | **37,421,816B** |
| 目前局部链接中尚未解析的真实外部符号 | **255项** |

最新物理构件：`03_脚本工作区/P890_第138轮_SwitchSDL2原OS屏幕和视口焦点坐标适配/real_GPL2_161_original_12_Switch_sdk_SDL2_EGL_mouse_focus_AARCH64_ET_REL.o`。**它是LLVM部分链接机器码，不是可启动游戏NRO，也不是NSP安装包。**

P891/P641读取此真实ELF64外部符号清单并复核255种未解项来源：`OS_*` **120种**（真正要实现Nintendo窗口、文件、输入/字体等后端）、`Wm_*` 原Wave Master声音/混音 **28种**、Nouveau GPU设备接口18种、NIR着色编译接口9种、C++运行时16种及其他64种（其中包括程序链接脚本/入口与原安装器/调试器接口）。当前GPU、OGG及电影播放器仍需真正音画时序和Switch硬件验证；链接层面有函数定义不代表执行已正确。

## 四、完整开发质量回归及下一轮

最终全量脚本：`01_工具脚本/verify_p892_round138_final_161GPL2_12Switch_127HD_1163_real_SDL2_OS_ABI.py`，实际重新执行原GPL2/PC-HD全历史质量链和本轮两个新增真实Switch后端编译、可执行主机断言与物理LLD链接，并审计255项剩余符号。权威最终JSON：`06_测试记录/P642_第138轮最终_161原GPL2_12Switch真实OS时钟鼠标26测试SDK_ARM64_127HD_SHA_1163.json`；新增两份真正运行的C99宿主测试含**26项 `must()` 断言**（14＋12）。

- 原PC-HD **127份**SHA256逐项匹配（原PNG、OGG、25fps影片、字体与BP，共39,772,982B），1280×960源CG绝不降级。
- 重新执行历史**1,163项**开发质量条件；原媒体与玩家存档只读。
- 原上游真正生产 `Vm_RunPass/Vm_RunThread` 上一轮八BP同态真实执行证据继续保留；新接入的SDL2时钟/窗口坐标**只有宿主隔离测试及真实ARM64机器码链接**，还未自然进入任天堂GPU连续帧循环。
- 未发布未经硬件验收的可安装NRO/NSP；**发行继续 `BLOCKED_NOT_SAFE_TO_INSTALL`**。

**下轮续接：** 原主线程IPL **225,988／PC0x20E4D**，P628原版生产调度的八个Thread_t、P642最新161原GPL2＋12Switch真SDK LLD构件与P641细分的255项真实缺口。优先实现正确的Switch声音混音/OGG同步和窗口/GPU真实帧服务，再接完HID/触屏/存档；切勿用假的函数体或把宿主模拟测试报告成NS实机运行。
