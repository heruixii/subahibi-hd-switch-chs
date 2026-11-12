# 第八十六轮续：真正205个BGI引擎C99模块进入NS ARM64

2026-10-20。本轮真正链接C99虚拟机、图形声音脚本支持模块为ARM64可重定位代码，不是模拟替代游戏运行。保留正版PC母版和所有NS旧补丁/Save。

## P429：新增完整83份GPL2引擎核心代码ARM64

在此前原VM 16个AArch64模块基础上，编译OpenBGI同一提交40b144a03e15f159cadc957387e6f94bce8de65f中src/wait、src/scn、src/bpc、src/core、src/sys（排除main）、src/sysobj共83份真C99源码，83份编译通过，失败0。含脚本译码、文件/线程等待、内存、资源与原引擎系统服务。保留上游源SHA与GPL-2.0-only许可证，不改原源代码；仅补POSIX_C_SOURCE宏确保现代strnlen原型在交叉编译中可见。

16份VM先前687个未定义符号，有308个真实被新C99模块实现，同时新服务需要336个更底层外部函数，净剩715个，所有链接仍是ELF64 ET_REL而非实际Switch运行。

## P430：新增106份原图形、音频、汇编、调试C99模块

再编译开源仓库src/gfx、src/snd、src/asm、src/dbg、src/os/os_common共106份原C99源码，106份成功，失败0。具体源码种类计数为{'gfx': 75, 'snd': 12, 'asm': 7, 'dbg': 11, 'os_common': 1}。源SHA及对象真EM_AARCH64=183逐份核对。

真正已在ARM64机器语言编译并链接的完整VM+服务模块计数=16+83+106=205。第83模块阶段缺失的715中，又有509被真正解决；新增33项更底层接口，最终尚有239项符号。其中约182项OS_函数，其余为标准C库和其它系统服务。完整单个可重定位ARM64 ET_REL共9160032字节，SHA256=e634127272df6db219b36efabef90c25ed437ae14e8745f7ef3e2b3b078c8bd7，不是NRO。

## P431/P432：真正的Switch SDL2宿主平台代码开始接通

对照上游原bgi/os.h ABI，自写独立C99模块。已实现3个完全可对应的调用：
OS_TicksMs调用SDL_GetTicks，uint32 32位回绕；OS_SleepMs调用SDL_Delay，原样转发毫秒数；OS_CpuCount调用SDL_GetCPUCount并保证至少返回1。

同一C99源码用Host模拟SDL2验证回绕、睡眠数值及非法CPU数量；再使用隔离Switch SDL2真实头文件编译AArch64；进一步与原完整205模块真ARM64 ET_REL链接。新合并机器码9162968字节，SHA256=82ed745086e4c8a1390c0adabd0be27f1493b9bb02bb8d19277dc1ba3176a95b。原3个OS_未定义符号真正有了实现，但SDL库3个入口还需在完整libnx SDL2运行时链接；所以净总数仍239。NS系统时钟精度、GPU和DAC没有物理设备记录，绝不宣称实机通过。

## 质量、授权与下一阶段

第86轮中央P214此前对旧与新增虚拟机16源模块完成432个Python脚本及4324阶段文件总质量门禁，状态仍BLOCKED_NOT_SAFE_TO_INSTALL。新增P429/P430/P432各自完整源SHA、真ARM64机器类型和OS ABI主机测试已PASS。本段继续把新三阶段加进中央门禁。

GPL-2.0-only的OpenBGI完整源与license保存在工程独立P419目录；交付任何其衍生二进制必须考虑GPL源码及许可证义务。本作PC HD版权素材、原OGG配音/音乐、原1280x960 PNG/Alpha、五部1280x960 25fps 48kHz影片以及旧汉化译文不因此获得公开分发许可，绝不上传到公共GitHub。P412早期手动52原声中文字幕QA NRO、原PC剧本与NS既有旧Save完全未修改。

后续应先实现182项OS_*里的真正Switch SDL2控制器/事件/文件系统/文字/音频输出；Windows驱动器、MCI、窗口管理、存档及线程接口不能随意空实现。再实证原PC BGI 1.647 profile及fixmul执行语义，之后实现剧情分支、中文字幕、音轨、高清演出和影片以及实机GPU/DAC/TitleID/Save保护测试。安装状态：BLOCKED_NOT_SAFE_TO_INSTALL。


## P435：真实ARM64机器码239项ABI依赖按任务分组

从ARM64最终对象readelf真实符号表提取239个未解析链接接口，其中在OS三个时钟/CPU符号实现之后OS_*共179个，其他60个（含三SDL链接接口）。分为私人SD文件/目录、Switch事件层、1280×960原图视频与日中字体、OGG声卡、线程与时钟、Windows特定非NS系统、标准C库等。元数据清单位于06_测试记录/P224_第八十六轮_GPL2真实205模块全部239待实现外部ABI及Switch适配优先级清单.json。这些是待实现的真实函数名，而非未来工作猜测；无需做大批空stub伪装完成。

## P436/P437：五个真正的NS私人SD文件只读ABI已编译

自写相同OpenBGI os.h的OS_FileOpenRead、OS_FileClose、OS_FileRead、OS_FileSeek、OS_FileSize五个ABI转换，后端采用Switch SDL2 SDL_RWFromFile/RWread/RWseek/RWsize/RWclose。严格仅允许路径前缀sdmc:/switch/subahibi_pc_native_hd_qa/，拒绝其外SD目录、相对路径、..向上穿越、重复分隔符或反斜杠，完全不实现写入、覆盖/新建/删除游戏或存档。主机独立内存字节样本完成从文件开头/随机seek/EOF/大小/close和非法路径拒绝。再用真实隔离Switch SDL2头文件将原C99源交叉编译为EM_AARCH64=183机器对象，并与既有205模块和3个SDL时钟ABI做实际ELF64 ET_REL链接。

现在Switch专用源码已提供8个BGI OS ABI接口：时钟、毫秒睡眠、CPU数量、只读文件打开/关闭/读取/定位/长度；先前OS_*未解析数179再减少5为174。SSL/SDL文件runtime等符号仍要由原libnx和SDL2系统真实链接，最终总未定义数仍239，不代表NS功能可玩、SD真机读取已实证或可以安装。

最终完整可重定位ARM64 ET_REL大小9177368字节，SHA256 2e0c78cee7d2b4feccb3d4146a0972d40ceec7744983c58c40d2d42434666cfa。见P225实测证据，源代码见03_脚本工作区/P436_私人SD只读BGI文件ABI_真SwitchSDL2_禁止写入_真ARM64。此P437独立验收不影响较早的中央历史门禁范围；后续应将其加入下阶段发行前门禁。


## P223中央最终完整质量门禁

在131个阶段新增源码与SDK真机器码断言于P433预检通过后，正式运行 refresh_current_port_quality_gate.py 将旧的全部保护和本轮P429/P430/P432作为MANDATORY一并校验。得到最后一行：
CURRENT_PROJECT_QUALITY_GATE BLOCKED_NOT_SAFE_TO_INSTALL PRIVATE_BUNDLE_FILES 4324 UNVERIFIED_EFFECTS 69 NO_DIRECT_RENDERER 20 PYTOOLS 438

独立全量日志SHA256：9729727d399fca950a5f0ba665c55fc11b16ab4c0f8d50102b285987ec79c621，文件在06_测试记录/P223_第八十六轮_真正205模块ARM64原BGI_VM及SDL2宿主131条件最终全中央门禁.log。原P412正式保存的旧非剧情NRO仍字节无变化，SHA256 757299abec004b2cee75350a8860516fb200851359ad00a9a742bead58204b39；本阶段真GPL VM+8SDL平台接口独立ARM64 ET_REL SHA256 2e0c78cee7d2b4feccb3d4146a0972d40ceec7744983c58c40d2d42434666cfa。最新源PRIVATE SD五API P437独立再次读取测试结果PASS，不会写入或误删原媒体/存档，不会将OpenBGI许可证覆盖原商业游戏版权。
本轮真正VM205模块全部原生C99/AARCH64架构交叉编译，只是原生中间对象，不含真Switch前端、SD物理设备运行、真实故事与CG动画、完整影片/OGG硬件音频和存读档实际测试。保持 BLOCKED_NOT_SAFE_TO_INSTALL。
