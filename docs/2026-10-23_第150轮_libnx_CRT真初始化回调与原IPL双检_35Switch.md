# 《素晴日》PC高清新版移植Nintendo Switch｜第150轮实证

2026-10-23，项目根：`D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns`。

## 一、承接第149轮状态

以第149轮`P676`权威为准：**175份未修改GPL-2.0-only OpenBGI C99源码＋1份明确修改过一行ARM64启动架构条件的GPL2 Engine_Main源码＋34份不同Switch平台桥接源码**，已生成真实**39,468,112B AArch64 ELF64 ET_REL**部分链接（SHA `286b2b29b8df6a403cc2243c2d609feab2dd36971c82ed9059749d6cb6588722`），**132项**真实未解析外部全局名。原PC127份1280×960高清CG、原OGG、25fps原影片、字体、BP共39,772,982B SHA全部完整，用户Save未动。原剧情真实执行位置仍是IPL **225988**／PC **0x20E4D**，没有因为平台对象数量增加而真正推进Nintendo端剧情。

本轮重点**不是再修改GPL2引擎或者伪造Windows API**，而是落实真实Nintendo Switch应用CRT启动/退出生命周期，让前轮私有SD、真实`ipl._bp`检测发生在官方libnx的启动回调期间，同时新Nintendo `main`在进入真正原GPL2 `orig`前**重复物理核查**，阻止已拔出SD或IPL消失后继续启动。

## 二、P930/P677：真实libnx CRT回调与新版原GPL2入口

新增2份真正Switch ARM64 C99源（GPL-2.0-only改造源码保留许可声明）：

`03_脚本工作区/P930_第150轮_真libnx应用生命周期与原GPL2启动保护/p930_nintendo_userApp_lifecycle_source_preflight.c`

`03_脚本工作区/P930_第150轮_真libnx应用生命周期与原GPL2启动保护/p930_nintendo_strong_main_after_libnx_userAppInit.c`

第一份物理实现官方libnx启动期引用的`userAppInit()`、`userAppExit()`函数：启动期调用上一轮真实已链接的`P922_EnsureOwnerSourceSdReady`，用真正`fsdevMountSdmc`、`fsdevTranslatePath`与`fsFsGetEntryType`验证业主只读游戏源码目录`sdmc:/switch/subahibi_pc_native_hd_qa/story`是存在的目录，再经真实P473/P474路径映射、`stat()`检查原`ipl._bp`确实是文件。缺失SD、原IPL、目录伪装文件，一律不缓存“可启动”。`userAppExit`只清理**属于本应用的启动状态位**，不能调用`fsExit`或`fsdevUnmountAll`去抢夺libnx应用CRT的自动生命周期，也绝不能删除原CG/OGG、脚本或别的游戏/用户Save，不能擅自删除上一轮原子锁（只有持有锁的`OS_InstanceMutexRelease`负责释放）。**不要把同源码的宿主回调测试冒充实体NS已执行过官方CRT。**

第二份**替换了前轮P926的Switch安全`main`，不会在真实ELF里同时链接两个强`main`**。它先确认libnx的`userAppInit`确实核查过资源，并**再次真正查询SD源目录以及原`OS_FileAttrs("ipl._bp")`**，全部成功后才通过经过ELF符号表重命名但原机器指令绝不修改的`orig(argc=1,safe_argv)`进入上游原GPL2 `OS_Init/Engine_Main`，明确丢弃外部`--extract`和其他不安全文件路径。用户SD拔除或原IPL后来丢失，即使之前启动缓存为真也强制失败；关闭后不会再调用原`orig`。

严格用**同一份C99源**生成Windows宿主测试exe，执行**16项**真实断言覆盖尚未启动CRT、SD缺失、IPL缺失、伪目录、正常IPL启动、非法用户命令行、不可信历史缓存、启动后SD丢失、启动后IPL丢失、用户App退出、再次初始化等行为。**16/16 PASS**，原商业资源和Save零写入。编译真正AArch64 ET_REL机器码，分别实现`userAppInit/Exit`和新版强`main`。

为避免叠加重复的原`main`，从真实P910 **173份未改GPL2＋24份Switch的前置引擎机器码**重新物理链接，加入另外两份原GPL2未改`main.c`和`hvl.c`、上轮明确授权适配的一份GPL2 `engine.c`、9批原生Switch SDK桥接以及本轮2份新接口。使用真实官方GNU C++ `libstdc++/libsupc++/libgcc`、SDL2、libnx和newlib静态库做物理LLVM `ld.lld -r`，最终**175原样GPL2＋1GPL2 ARM64适配＋35份不同Switch平台对象**。原175份上游GPL2源码、商业媒体和玩家Save保持只读。

阶段权威`06_测试记录/P677_第150轮_真libnx_userAppInitExit与原GPL2main前安全验证_35Switch_130缺口.json`状态PASS；实际真AArch64 ELF64 ET_REL Machine183文件：

`03_脚本工作区/P930_第150轮_真libnx应用生命周期与原GPL2启动保护/P930_175Original_1GPL2adapted_35Switch_libnx_lifecycle_native_AARCH64.o`

**39,471,208B**，SHA256 **`481d49359adc1c6229588ef32271cc5ec019cdcf8cffb7fb6b2bcc00636df7a1`**。与上轮ELF真实符号差集严格对比，**正好解决`userAppInit`、`userAppExit`两项官方CRT引用，未添加新的外部依赖，132→130项真实未解外部名**。具体清单`P930_real_arm64_unresolved.txt`，不会把未解处理成成功。

## 三、余下130项的真正可玩阻塞及避坑

通过物理LLVM ARM64机器链接清单而不是按文件数量统计，当前未解**130项**，按名字前缀审计：**61项OpenBGI原`OS_*`跨平台接口、10项NIR/SPIR-V Shader接口、7项GNU C++事务内存ABI相关符号，其余52项包括Windows旧安装器/注册表/快捷方式以及实际ELF最终链接所需的CRT和装载器运行时符号**。这是**ET_REL局部链接的未解符号数，不等于制作完整NRO仅差130行源代码**。要结合最终链接脚本/entry/SDK分清哪些是源码缺实现、哪些可由NRO终链接填充。

对实际原GPL2调用点进行源码跟踪：真正影片接口原`src/gfx/movie.c` `Movie_Play` 调`OS_MovieOpen`，只有返回真实可用的播放器才能继续`OS_MovieStart`，若失败则进入原`src/sys/moviefx.c`的FFmpeg独立进程解码路径。而现有隔离Nintendo SDK里**没有可直接链接的`libavcodec.a`、`libavformat.a`、`libvorbisfile.a`、`libogg.a`或SDL2_mixer**，无法凭空说已经实现原25fps音画解码。原`OS_PlaySoundFile`仍须实际音频设备与原文件格式服务，不能造一份总返回1的假实现。原场景GPU/NIR全套、中文字形/窗口上屏、Joy-Con、存档安全读写也都要实测，不以模拟硬件宣称完成。

`OS_DirCreate/DirRemove/FileCreate/FileWrite/FileDelete/FileCopy`等9项写入API必须严格将写入目标限制到单独**新建的安全测试存档区**且真实验证其FS授权和`fsdevCommitDevice`语义，不得写在原商业游戏`story`下，更不能覆盖用户现有真实Switch存档或任何其他Title目录。原SD测试锁崩溃时可能残留，请核实后仅人工操作该私有锁，绝不广泛清除游戏目录。

## 四、第150轮完整全历史质量门禁、续接

本轮整链实际回归脚本：

`01_工具脚本/verify_p931_round150_final_libnx_CRT_userApp_InitExit_HDSHA127_QA1163.py`

须先真实重跑**127份原PC 1280×960高清CG/OGG/25fps影片/字形/BP逐SHA256完全一致及1163项历史开发质量测试**，再重编完整P929架构适配与P930 C99 CRT和安全原`main`，执行本轮16项宿主测试，核验实体Machine183 ELF SHA和130个未解外部名并按来源分类。权威最终记录：

`06_测试记录/P678_第150轮最终_175原GPL2加1架构适配35Switch真libnx应用生命周期_127HD_SHA_1163.json`

**本轮最终完成只以P678实际PASS为准**。即便P678 PASS，正式NRO/NSP和用户Switch实体机还没有得到完整安全验证，不能发版或安装覆盖现有游戏。`release_install_status=BLOCKED_NOT_SAFE_TO_INSTALL`。下轮从原剧情IPL **225988**／PC **0x20E4D**、175原样GPL2＋1 GPL2 ARM64架构适配＋35份平台桥接／**130个真实未解全局符号**继续，优先真实音画/SDK与独立Save而非批量替代旧Windows安装器函数。

## 五、P931/P678整链质量回归正式完成

最终`P678`**真正运行159.15秒，结果`PASS_P931_ROUND150_ACTUAL_175_ORIGINAL_1_ARCH_GPL2_35_SWITCH_LIBNX_CRT_APP_SDIPL_127HD_1163_DEV_ONLY`**：原PC高清资源**127份**、母版**39,772,982字节**逐SHA256一致；历史**1,163项**开发断言在本次调用链实际全部重新执行PASS；第149轮ARM/x86十项CPU条件测试重新执行；本轮**16项同源码libnx userAppInit/userAppExit+强Nintendo main前置IPL/SD检验测试全部PASS**。真正从原P910基线重新链接了**175份GPL2原源码＋1份独立GPL2 ARM架构适配＋35份不同Nintendo C99机器码**，旧x86 CPU门槛正确跳过而没有伪报CPU，原GPL2主函数和真实文件验证源码仍保留。

本轮最终AArch64 ELF64 Machine183 ET_REL物理目标 **39,471,208字节**，SHA256 **`481d49359adc1c6229588ef32271cc5ec019cdcf8cffb7fb6b2bcc00636df7a1`**。真实**130项**未解外部名与ELF逐项一致，归类**61个原`OS_`跨平台API、10个NIR/SPIR-V函数、7个GNU事务内存运行库符号和52个安装器/CRT/ELF引导等其余名字**。这仅是局部链接真符号，不是NRO最终链接差距的精确工作量。

权威最终记录：`06_测试记录/P678_第150轮最终_175原GPL2加1架构适配35Switch真libnx应用生命周期_127HD_SHA_1163.json`。**第151轮从P678、原IPL225988/PC0x20E4D、175原GPL2＋1GPL2架构适配＋35Switch、130项未解开始；原高清画质和声画不降级。** 真Switch SDK/HOS Applet/SD自动启动后主线程、CG及中文字幕实机GPU、OGG/25fps电影解码与同步、Joy-Con和隔离Save尚未验收，仍`BLOCKED_NOT_SAFE_TO_INSTALL`，不允许将部分ET_REL冒充可安全安装的NRO/NSP。
