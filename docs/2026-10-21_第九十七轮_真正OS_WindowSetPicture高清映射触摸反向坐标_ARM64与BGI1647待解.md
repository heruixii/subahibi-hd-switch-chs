# 第九十七轮：原BGI高清OS_WindowSetPicture触摸映射源级验证与ARM64链接

日期：2026-10-21。项目根目录 D:/switch游戏/素晴日/素晴日整合/1.游戏合集/移植新版素晴日ns。
当前仍 BLOCKED_NOT_SAFE_TO_INSTALL；没有真实故事NRO或已运行的游戏。

## 实际移植进展

上轮ShunCode桥接终止，本轮重新连接并直接从此前已落盘的P536/P537代码恢复，没有重做高清资源和演示安装包。真实新增的是原GPL2 OpenBGI VM所引用的 OS_WindowSetPicture(w,h)。其C源码在 03_脚本工作区/P536_真BGI图片大小与原高清指针逆映射联动_既有SDL窗口_ARM64/p536_original_BGIVM_10_window_HDpicture_pointer_SDL2_AARCH64.c。

当原逻辑画布为1280×960时，调用先前已完成的 P445_BorrowRenderer、真正 SDL_GetRendererOutputSize、P441_ComputeHDViewport 和 P438_ConfigureOriginalHDViewport，使现有SDL2画面与触摸坐标映射同步；切换全屏和还原窗口也重新计算。原1280×960 RGBA/Alpha CG，不改文件像素、不降至旧800×600，视频音频母版不重编码。

P537主机真实执行OpenBGI原GPL2 OsCommon_MainTitle、P441_ComputeHDViewport、P441_MapWindowPointerToOriginal，并用SDL/P438的宿主夹具记录是否正确刷新：1280×720输出原4:3画面占用x160..1119，中心(640,360)反算为原(640,480)；1920×1080画面投射横坐标240..1679；黑边坐标不会误命中原画面。NULL/无窗口、负尺寸、旧800×600和SDL输出失败等负例PASS。**说明：本轮测试用了记录P438_ConfigureOriginalHDViewport调用的测试夹具，未直接执行整个P438事件队列；非1280×960画布虽标记不支持，但尚不能声称完全禁用了此前输入模块的坐标回退。**

P538用隔离Zig工具链真正编译AArch64 Machine183 ELF64重定位机器码。P539以原205个GPL2 C99/ASM VM引擎模块和此前72个原BGI宿主接口为基线，链接10个当前需要的窗口/显示/图片函数，其中9个已有P531，本轮新增1个真实OS_WindowSetPicture；无重复计数。BGI OS未解析105->104，总外部388->387。

真ARM64引擎合并中间对象 9842672 字节，SHA256 93286bcbb24bea0cb2d18f85d1b475577fafded44c9d66aa9e69eb3947ed5dbb。
与真正Switch SDL2/libnx/EGL/GLES静态归档可重定位链接后的对象 40143664 字节，SHA256 d8c21f9906b7887295d76d6fbe3858c0fd8c05d1c5a9b38cb6a232cb420ef1ef。
**以上仅ELF64 ET_REL，非可执行ELF或可安装游戏NRO。**

## 质量验证与安全边界

P540 非发行源码快速门禁PASS耗时 15.7秒：重跑前轮真实205/81OS与55BP/ipl真实加载、Noto中文字体主机像素、OS窗口及本轮高清反向映射主机测试；原127份私人HD PNG/OGG/Noto/BP资源再次逐文件读取SHA，旧非游戏QA NRO原字节不变；新AArch64对象与SDK合并后哈希完全一致。原主人NS TitleID/Save、五段高清25fps/48kHz影片和原44.1/48kHz音频全部未修改。

P541 从作者当前中央闸门源码独立提取新增496条条件并逐一PASS，历史耗时全媒体中央最终闸门本轮没有重跑。不可将快速预检或静态链接当作已运行游戏。

当前根本阻断未解除：原IPL产品SubarashikihibiHD的真实 BGI 1.647 profile 并未被上游OpenBGI内置支持；相邻1.640/1.653不应猜测代替。title._bp 的0x56只有编码结构候选，原native VM完整执行语义未证明，sys_::f_120和游戏选择/保存/全部电影未真正运行。仍缺104个BGI系统接口和387个总体静态外部符号，以及Nintendo实机GPU/DAC/触控/Save保护测试。

继续优先研究原1.647真实编译脚本和native执行代码、选择适配，并完成输入禁用和多种逻辑画布所需的实际GPU/指针支持；不能制作假兼容完整游戏包。状态 BLOCKED_NOT_SAFE_TO_INSTALL。
