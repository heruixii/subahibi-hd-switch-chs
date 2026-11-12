# 《素晴日》高清新版 NS 移植：第135轮真实生产调度函数和 Switch 桥接链接

2026-10-23。实际工作区：`D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns`。

**发行仍然 `BLOCKED_NOT_SAFE_TO_INSTALL`，开发隔离QA通过不意味着可安装的NS游戏。** 保持原PC高清CG、OGG原始音频、25fps影片、字库、原BP/ARC归档和用户存档只读，不降低到800×600，不用静态假效果代替原版演出。

## 1. 直接执行未经修改的GPL2生产 `Vm_RunThread` 函数体（P876/P626）

前轮 P870 已用同一次原版IPL重放将**8个真实原BP子线程**运行6轮、共1748条真原C99指令：第5轮在`mtnmngr._bp`的真实Thread_t上等待而跳过指令，第6轮在显式隔离测试时钟到期后恢复执行。原主线程执行计数仍为**225988，PC=0x20E4D**。

本轮不再只使用该受控调试调度循环，而是从GPL2上游 `src/vm/sched.c` **精确提取未经更改的生产函数体** `static int Vm_RunThread(Thread_t* t)`，直接在同一原GPL2隔离宿主C99编译执行（外部调试钩子在本测试中关闭，且任何被意外触发的钩子立即终止测试）。

- 选择真实原子线程ID6：`mtnmngr._bp`，第6轮结束时原代码 `IP=637`、栈 `SP=30`、原`Thread_t`对象未重置；源码下一opcode确为原BP `00 Opcode_PushI8`。
- 安装**真实 GPL2 `WaitTimer_New` + `Thread_SetWait`**（7ms开发测试fixture），首先调用**原生产 `Vm_RunThread`**：返回`1`，线程仍等待，IP637/SP30/FP原值保持原样，**没有执行或抓取任何真实脚本字节**。
- 随后仅在**隔离测试环境**明确将虚拟时钟推进7ms，再调用同一未经修改的 `Vm_RunThread`：源码自己的 `Thread_PollWait` 解除等待，源码自己的 `Thread_FetchOp` 真正读取原BP `00` 并调用真 `Opcode_PushI8`，`IP=637→639`、`SP=30→31`，执行结果返回`0`（限额结束）。
- 调试器限制该次执行1条指令是为了阻止未接通的其余副作用并校验精确原字节，**不是把真实GPL2生产 `Vm_RunThread` 中的指令/等待逻辑替换成模拟函数**。这次验收只覆盖函数本身在真实Thread_t的等待/取指路径，**并未**执行完整 `Vm_RunPass`、`Vm_FrameServices`，不能冒充原剧情持续播放或NS实机帧服务。

证据：`01_工具脚本\verify_p876_round135_exact_original_GPL2_Vm_RunThread_wait.py`，`06_测试记录\P626_第135轮_原GPL2生产Vm_RunThread源码实执行等待跳过及原00取指.json`，隔离实际源码、编译日志和运行日志位于`03_脚本工作区\P876_*`。

## 2. 首次将150份真实原GPL2 AArch64引擎机器码和5个Switch原生桥接目标实际合并链接（P875/P625）

此前已经**真正**交叉编译了150份未经修改的原GPL2 C99源码为真实AArch64 ELF64 ET_REL，150成员GNU静态库是**7,360,930字节**、`ld.lld -m aarch64elf -r` 部分链接机器码ELF是**6,593,376字节**，其中258个未解析符号有真实清单。前轮梳理出147个OS接口、27个窗口消息以及其他C库/游戏引擎外部依赖，不得用Windows/POSIX/Wasm实现冒充Nintendo实现。

**P875** 为避免把旧的205源预链接整体混入150源引擎造成重复符号，**仅选5个已经独立编译并经过原生ABI核验的Switch SDL2/libnx机器码目标**与150源码合并ELF执行真正LLVM LLD -r：

| 已存在的Switch目标 | 本轮实际匹配并解析的原GPL2接口 |
|---|---|
| SDL2基础时钟/睡眠 | `OS_TicksMs`, `OS_SleepMs` |
| SDL2手柄、键盘与事件泵 | `OS_KeyState`, `OS_KeyboardState`, `OS_PostQuit`, `OS_PumpMessages`, `OS_SetEventHandlers` |
| SDL2光标 | `OS_CursorShow` |
| libnx真实SVC进程内存 | `OS_MemoryStatus`, `OS_MemoryStatusEx` |
| SDL_RWops 私有SD文件**只读**读取 | `OS_FileOpenRead`, `OS_FileRead`, `OS_FileSeek`, `OS_FileSize`, `OS_FileClose` |

结果：**150个原引擎源单元 +5个不同Switch原生目标**成功真实LLD部分链接，且没有重复定义任何原GPL2全局符号。总共15个原GPL2 OS调用得到定义，桥接又引入21个新的SDL2/libnx相关外部依赖。因而与150纯原GPL2模块集合同口径比较，真实缺失符号 **258→264**；这是依赖引入后的精确会计而不是编译倒退。合并的**AArch64 ELF64 ET_REL为6,696,720字节**。只检查到目标文件和局部链接，**SDL2动态/静态运行库、libnx系统入口、真实图形驱动、OGG/影片、HID/Save的全量最终链接、Switch硬件运行均未完成**。

实际产物：`03_脚本工作区\P875_第135轮_150原GPL2与现有5真Switch_SDL2_libnx桥接首次LLVM实部分链接\original150_GPL2_plus_5_true_Switch_SDL2_libnx_AARCH64_LLD_partial_ET_REL.o`。P625 JSON记录全部5份对象的源路径、SHA、原 `inc/bgi/os.h` ABI符号、分组resolved/added以及合并目标SHA、剩余264项外部符号的完整文件。脚本：`01_工具脚本/verify_p875_round135_150_original_GPL2_plus_5_switch_SDL2_libnx_AARCH64_true_LLD.py`。

## 3. 质量闸门和后续准确续接

第135轮完整自动验收使用 `01_工具脚本/verify_p877_round135_final_original_production_VM_true_Switch_LLD_127HD_1163.py`，重跑前轮全部历史开发门禁及本轮 P875/P876。权威结果记录为 `06_测试记录/P627_第135轮最终_原GPL2生产Vm_RunThread实执行_150引擎和5Switch桥接真链接_127HD_SHA_1163.json`：

- 127/127份原 PC-HD PNG/OGG/25fps电影/字体/BP相关源媒体SHA256一致，总计**39,772,982字节**；GB4位图128和Mode5精灵33仍1280×960，不做重采样或假静态代替。
- 1,163项历史开发断言重新运行PASS；原用户Save、PC源归档不被改动。
- 真实源八BP六轮1748条及第六子线程原GPL2生产`Vm_RunThread`等待/真正读取opcode及SP/IP递进有独立原始运行日志。
- 150份原GPL2 ARM64 ELF64源目标/静态归档实际重建；5份现有Switch桥接ARM64对象经过真LLD无重复符号部分链接、校验新合并ELF SHA和264项真实未解析符号。
- 当前**只有开发质量结果**，不可声称Switch高清画面、声音、动画、电影、手柄和存档已经实机验证，**未生成可安全安装的完整版NRO/NSP**。

**下一轮优先级：** 从原主线程 IPL225988 / PC0x20E4D、P620的八BP第六轮运行态与P626直接运行的生产函数证据继续，进一步把原 GPL2 `Vm_RunPass` 真正用在八Thread_t完整列表的源码消息/等待/调度路径上；然后按P625的264个**包含新SDL2/libnx依赖**的真实外部符号清单完成实际目标平台SDK/运行库连接、图形/OGG/25fps视频/HID/Save实机验收。保留原1280×960高清，拒绝低清替代、数据破坏与未实测发行。
