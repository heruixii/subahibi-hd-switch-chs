# 《素晴日》新版PC高清移植Nintendo Switch｜第144轮真实引擎主入口整合记录

记录日期：2026-10-23。工作根目录：`D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns`。

## 基线与本轮重点

继承第143轮权威`P661`：原版真实主线程IPL **225988／PC=0x20E4D**；**173份未经修改OpenBGI GPL-2.0-only原C99源码模块**＋**24份独立Switch SDL2/libnx/OFL字体高清GPU/PCM/SD桥接模块**，真实ARM64局部链接ELF64为**38,516,512字节**、剩余**159项实在的未解析全局名字**。127份原PC高清CG/OGG/25fps影片/字体/BP总共39,772,982字节仍逐SHA完全一致，原PC媒体和玩家Save不允许修改、图片不降采样。

本轮不是单纯追求链接缺口个数下降，而是把之前只编译到独立小样的**真正上游原GPL2程序入口**和SDK的**真实GNU C++运行库**接回当前高清字体和SDL2声音/窗口运行链。严格保留真实OS缺口、SDK额外依赖和缺少实体Switch启动验证的发行限制。

## 一、原样编译原GPL2的真正程序引擎、main和游戏资源哈希（P912/P662）

三份完全不修改原始字节的上游源码：

1. `src/sys/engine.c`：原引擎 `Engine_Main`、`Engine_Init`、`Engine_Shutdown`、`Boot_ParseCmdLine`，以及`gEngineUp`、`gLauncherMode`、`gDiscMarker`、原退出程序参数等状态；这里包含真实原顺序的启动/窗口/声音/脚本初始化，但**当前尚未把它在Switch实体执行**。
2. `src/sys/main.c`：真正的**POSIX风格`main(argc,argv)`程序入口**，接收引擎参数，调用`OS_SetArgv0/OS_Init`再进入原`Engine_Main`，最后退出并调用`OS_Shutdown`。不是一个只打印“游戏已启动”的占位入口。设备侧特定Applet/CRT装载条件尚未满足。
3. `src/sys/install/hvl.c`：原`HvHash_File`、`HvHash_UpdateBuf`、`Hvl_Load`等。`HvHash_UpdateBuf`是真实旧引擎游戏数据8字节哈希，不是用户下载资源的现代SHA-256替代品。此处仅编译源字节，没有真的复制、安装或改写任何游戏文件。

工程的`01_工具脚本/verify_p912_round144_three_true_original_GPL2_main_engine_hvl_with_native_Cpp_sdk.py`严格检查原三个源码SHA-256未改变，逐一真实C99→AArch64 ELF64 Machine183并检测没有重复强符号。为避免直接运行尚缺操作系统服务的整个商业引擎，宿主测试仅将**真实原源码中一字不改的启动参数解析和HVL分块哈希函数区间**抽取到隔离生成源码编译，未改动完整ARM64上游编译文件：

- **9条原始启动参数解析测试真实PASS**：默认`ipl._bp`、`.`和指定`romfs:`目录、带空格私有SD路径、原`Do not use mutex.`及`Execute as a launcher.`标志、未知选项不误认、引号中的路径不丢失。
- **4条原始HVL字节哈希测试真实PASS**：独立计算原8字节哈希参照、原分块续算与一次计算一致、零字节初始状态、非零真实负载。测试只对内存数组算哈希，不修改PC媒体或存档。

额外纳入真正Nintendo SDK AArch64 `libstdc++.a`、`libsupc++.a`、`libm.a`及`libgcc.a`归档，真实LLVM `ld.lld -m aarch64elf -r`对这三份原GPL2模块＋既有173份GPL2/24份Switch原生模块和GNU C++库执行物理链接。**旧159项缺口中27项获得实际机器码**（含原`main`、六项原引擎全局变量、`HvHash_File/UpdateBuf`与GNU C++的17个旧ABI）；但新引擎和库自身**诚实引入18项新的设备/运行库依赖**（含`OS_InstanceMutexCreate/Release`、`OS_IpcSendToRunning`、`OS_ImeStatus`及`_ITM_*`等）。最终此阶段**159→150项**。并不假称编出了Switch最终NSO/NRO。

P662物理验证文件：`06_测试记录/P662_第144轮_真正原GPL2_3份引擎入口main文件HVL哈希和原GNUcppSDK_ARM64链接.json`；机器码与完整150项缺口：`03_脚本工作区/P912_第144轮_真正原GPL2主入口engine_C99与GNUcpp库链接探索/P912_original176_GPL2_24_Switch_real_engine_boot_hash_CppSDK_AARCH64_partial.o`。真正原GPL2源码累计**176份**。

## 二、将真SDL2 OS_Init/Shutdown绑定回原程序入口（P913/P663）

复用以前已有、经过真实源码单独验证的`P486_*/p488_Switch_SDL2_Engine_OS_Init_Shutdown_bootstrap.c`，将其**重新交叉编译成第25个不同的Switch原生AArch64目标**：

- `OS_Init`在实际SDL2调用`SDL_Init(SDL_INIT_TIMER | SDL_INIT_EVENTS)`，初始化失败返回0，不伪报成功；重复调用正确控制资源所有权。
- `OS_Shutdown`实际调用SDL2 `SDL_Quit`进行清理，在此前初始化失败、重复退出时不重复错误释放。
- `OS_SetArgv0`保留此主机的原控制台约定，不根据用户进程参数臆造游戏数据目录。此前原`OS_BinaryDir`/目录映射模块仍为它提供路径。

对**同一份新增对象的真实C99源码**在宿主重新编译出可执行测试，覆盖SDL2计时器＋事件创建、故障拒绝、重复初始化、正确释放和重新初始化，执行PASS（仅SDL回调在宿主fixture模拟）。随后重新LLVM部分链接到最新**176原GPL2 C99＋25Switch平台对象＋真实SDL2/libnx/GNU C++ SDK**，前版未解的**`OS_Init`、`OS_SetArgv0`、`OS_Shutdown`三项确实变为机器码定义**，没有引入新的未解依赖，**150→147项**。

脚本`01_工具脚本/verify_p913_round144_true_SDL2_EngineInit_shutdown_native_176GPL2_25Switch.py`，实证JSON`06_测试记录/P663_第144轮_176原GPL2加25Switch真SDL2系统启动回收OS_Init三符号_ARM64.json`。本轮最新ARM64中间ELF：`03_脚本工作区/P913_第144轮_真实SDL2引擎启动初始化并接原GPL2主入口/P913_real_original176_GPL2_25Switch_EngineMain_SDL2_CppSDK_ARM64.o`，**39,402,328字节**，ELF64 ET_REL Machine183。当前尚缺系统进程单实例互斥、远程进程IPC、安装对话/字体扩展、NIR、部分完整GPU软件后端和SDK编译启动时地址布局等；**真实程序入口链接绝不意味着Switch机器里游戏已进入标题画面**。

## 三、第144轮完整历史质量门禁与后续工作

最终完整测试：`01_工具脚本/verify_p914_round144_final_true_176_originalGPL2_25Switch_boot_cpp_hvl_HD127_1163.py`。**已实际运行131.41秒、最终状态`PASS_P914_ROUND144_TRUE_ORIGINAL_176_GPL2_25_SWITCH_SDL2_EngineMain_Cpp_HVL_RASTER_HD127_QA1163_DEV_ONLY`**。再次**实际重新执行**第143轮原PC **127份高清媒体逐SHA一致及1163项历史开发断言全部PASS**（而不是只引用旧JSON），把P912上游原main/engine/HVL真实源码与P913真SDL2启动模块再次完整编译/宿主测试/ARM64 SDK LLVM链接；核验最新ELF实体**39,402,328字节**、SHA256以及**147项真实未解名字**，尤其`OS_InstanceMutex*`、`OS_IpcSendToRunning`、`_rmdir_r/_unlink_r`均未被“成功编译”掩盖。权威质量记录：`06_测试记录/P664_第144轮最终_176原GPL2加25Switch真正EngineMain和GNUcpp启动_127HD_SHA_1163.json`。

**第145轮准确续接**：沿用原IPL **225988、PC=0x20E4D**，本轮开发构件**176份原GPL2真C99机器码＋25份互异Switch原生适配＋真实SDL2/libnx/GNU C++/CRT静态SDK，剩147项局部未解析**。优先真正安全实现OS_Init后面原`Engine_Main`需要的单实例/文件路径/输入/消息、中文菜单字体在实体Switch上屏与全分辨率画布绘制、原OGG/25fps电影音画同步、Joy-Con/触屏/Save；若系统OS接口没有相同可用语义，必须保留失败而不能伪称功能。所有原游戏CG/OGG/影片/脚本/用户存档依旧只读。

**未经实体Switch持续运行验收、没有制作可安全安装的完整NRO/NSP，`release_install_status=BLOCKED_NOT_SAFE_TO_INSTALL`。** 原OpenBGI GPL-2.0-only源码、`stb_truetype`与Noto字体OFL须分别遵循各自开源协议，商业媒体另按权利人的授权处理。
