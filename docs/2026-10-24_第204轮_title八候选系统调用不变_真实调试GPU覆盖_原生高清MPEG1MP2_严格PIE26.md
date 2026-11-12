# 素晴日 PC HD → Nintendo Switch 第204轮

记录日：2026-10-24。坚持原1280×960高清CG、25fps MPEG-1视频、MP2原音、OGG音轨、原双语字体及用户存档安全。所有操作限于移植项目专属工作区；原PC游戏、原Switch包、原主人存档、原工具链SDK均未被修改。

## P776：title系统BP的0x56未知指令审计

原私有标题BP的SHA256为35b8e215ea5d8933cd4db25cb48ed66d06b0d03f9c0133c2aadfe3b546b12ac2，未知基本操作码位于0x0a05。原P277证明有八个结构有效的候选操作数宽度：0、1、2、3、4、5、7、8。分别完全解析这八种假设，原VM系统80/81操作码序列完全一致，均包含14次80 40动态模块加载，并没有直接出现安装器注册或外部Windows进程操作码。P776通过。

这一事实并没有解决0x56真正的参数宽度和运行语义，也没有完成整个标题脚本的控制流证明，不能擅自选一种宽度写回或让VM跳过指令。

## P777/P778：原GPL2调试器切换真正主GPU覆盖层

从原GPL2 src/dbg/dbg.c生成完整独立源码衍生，强制使用原有的主游戏画面覆盖层功能，不尝试创建Win32第二个顶层调试窗口。保留原DbgDraw绘制、输入、暂停恢复及调度，并依赖原OS_WindowGetDc、OS_BlitToWindow、OS_WindowReleaseDc和每帧Dbg_OverlayPresent绘制到主画布。

从实际GPL2源码中原样抽取Open、Close、Present及Dbg_OverlayPresent四个完整函数；宿主C99执行20项检查通过，含1280×960、关闭主画面恢复、DC配平、GPU缺失及绘图分配失败。然后重建148原GPL2核心＋2安全衍生、10原GPL2调试源码＋1覆盖层衍生、64份原生Switch平台适配、16份验签Mesa源码。P778通过。

真实Horizon switch.ld严格PIE缺符33→29，消除了OS_DebugWindowOpen、Close、Alive、Present四项，0重复定义、0非法只读重定位。确切计数是64个平台适配＋1份GPL2调试器衍生，而不是65份平台适配。

## P779：只保留真实原生MPEG-1/MP2，不假装能运行PC ffmpeg

原GPL2 gfx/movie.c本来先调用原生OS_MovieOpen/Start/Stop/IsRunning/SetVolume，失败时才调用src/sys/moviefx.c去启动PC ffprobe/ffmpeg进程。Switch不能运行宿主机上的ffmpeg可执行程序，本项目已有真实原生MPEG-1、MP2和SDL2画面/音频实现，因此单独衍生整个原GPL2影片调度源，保留原原生播放器、画面缩放、音量、结束事件及画面恢复，只在Switch独立源码配置中去掉不可实现的外部进程回退；不支持的格式明确返回失败，不虚构播放成功。

从150个原GPL2独立AArch64机器码对象中保留146个不变；只替换真实安全SaveWrite、Child及Native Movie三个源对象，排除仅负责PC ffmpeg子进程的moviefx对象。原视频和CG均未转码、未退回800×600。

实际GPL2电影源与严格宿主HOS API模拟一起编译运行，26项原API断言通过，包括1280×960原尺寸、GPU目标矩形、MP2音量、失败返回、结束时重绘、无音频设备ScriptError。P779全源码独立复建通过。严格Nintendo PIE缺符29→26，消除OS_PipeProcStart/Read/Stop三项，0重复定义、0非法只读重定位、0新缺符。宿主验证并非真实Switch完整电影播放验收。

## P780最终门禁与具体文件

原130份主人编译剧情与原55份私有IPL/系统BP再次逐份SHA验证。结果：146原GPL2机器码＋3安全/原生视频衍生、10原GPL2调试源码＋1调试覆盖层衍生、64原生Switch适配、16验签Mesa20rc3 NIR模块。原CG、原MPEG/MP2/OGG、中文字体和玩家存档没有改动。

完整测试报告：06_测试记录中的P776、P777、P778、P779、P780 JSON。可重复测试和复建脚本：01_工具脚本中的verify_p1115、verify_p1118、verify_p1119、verify_p1123、verify_p1124脚本。

本轮最新真实机器码位于03_脚本工作区/P1120_第204轮_原GPL2视频源真实HOS_MPEG1_MP2_播放器_独立切除桌面_ffmpeg_ffprobe外进程_不降HD/P1121_ORIGINAL_GPL2_64OS_NATIVE_MPEG1_MP2_GPU_16SIGNED_MESA_AARCH64.o。仅为AArch64 ELF64 ET_REL开发文件，不是可安装游戏。

剩余26个严格缺符及其保守原VM来源分类分别保存在P780 JSON及02_清单与差异下的P204最终26缺符CSV。主要是PC安装/卸载、注册表、快捷方式、Win32子进程、桌面拖放、文件属性和桌面壁纸。原BP的完整间接控制流和标题0x56仍未证明，严禁以空接口、虚构成功、忽略未定义等方式骗过链接器。

当前正式状态：BLOCKED_NOT_SAFE_TO_INSTALL。尚无可安装NRO/NSP，也还未完成原剧情、视频音频同步、CJK文字、八子窗口及存档安全的完整Switch真机验收。
