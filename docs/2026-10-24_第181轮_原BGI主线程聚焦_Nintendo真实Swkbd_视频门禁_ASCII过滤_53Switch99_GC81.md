# 《素晴日》PC高清中文版→Switch，第181轮：真实BGI聚焦→Nintendo键盘的边界修正

工作区：D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns。

日期：2026-10-24。**状态：BLOCKED_NOT_SAFE_TO_INSTALL。** 本轮没有制作假NRO/NSP，也不宣称实机Applet已经弹出。全部代码写入新P1015隔离目录，旧P1013、原GPL2只读参考、原商业游戏媒体和玩家存档未改。

## 第180轮审计时发现两项真实边界缺口

旧版本真正OS_EditFocus会立即发起阻塞式libnx Swkbd applet，但当SDL视频服务仍未初始化时，原VM输入框处于未可用状态，旧代码仍可能调用swkbdCreate/Show。第181轮只在SDL视频实际启动后、原BGI真实可见且聚焦时启动键盘，缺视频时保持聚焦意图；SDL视频启动后再次OS_EditFocus(1)时可以启动。原主VM线程在不持有SDL_AtomicLock的状态下调用系统Applet，避免在阻塞系统键盘期间拿住CJK输入文字spinlock。

原B0 29的OS_EditRejectAscii要求拒绝可打印ASCII。先前SDL_TEXTINPUT watcher已实现该约束，但系统软键盘通过OS_EditSetText直接更新原BGI文本，因此能绕过这个条件。第181轮通过一个新的SDL_AtomicLock保护的只读标志接口P1015_BGIEditRejectAsciiEnabled，把同一规则施加到Nintendo swkbd整段UTF8回填。出现被禁ASCII时拒绝提交整段，避免一部分字符被静默丢掉；只包含中文时仍可通过真实P546 CP936/CP932编码回环校验。

## 新分支与可重建QA

新GPL2适配源码：

03_脚本工作区/P1015_第181轮_原BGI聚焦系统软键盘时序_ASCII过滤与真正整合QA/p1015_atomic_BGRI_Edit9_hooks_Nintendo_Swkbd_with_video_guard.c

同目录：

- p1015_Nintendo_Swkbd_real_BGIEDIT_CJK_ASCII_filter.c：真实Nintendo libnx swkbdCreate、swkbdConfigMakePresetDefault、swkbdShow、swkbdClose及CJK回填前拒ASCII；
- p997_originalHD_EditMove_nochange.c 和 p997_originalBGI_RGBA_GPU_Refresh_nochange.c：从第177轮原受测SDL IME与P454透明编辑渲染逐字节复制，未改高清画面；
- p1016_host_REAL_OS_EditFocus_SDL_spinlocks_Nintendo_swkbd_BGI_integrated.c：把真实p1015焦点源、真正P546中文GBK/日文CP932字符转换、原P441 4:3高清视口、真实Windows Interlocked原子锁及两个实际Win32线程、受控模拟Horizon Swkbd服务一起链接。它不再只测试未被调用的独立OSK函数，而是调用真正OS_EditFocus完成完整生命周期。

实际宿主测试验证：

- 原SDL视频未初始化时不调用系统键盘；之后获得视频且再聚焦会启动；
- 同一焦点重复OS_EditFocus(1)不反复弹窗，失焦和隐藏后允许新焦点再次启动；
- 原BGI B0 29拒ASCII对系统软键盘同样有效，纯中文原GBK仍允许；
- 取消不改原文、输入过程中被其他事件更新时保留新文本、原CP936/CP932和UTF8边界正确；
- 原SDL watcher/IME Start/Stop由之前真正原BGI源管理；真实Windows两线程并发，主线程始终进行2,500次原BGI文本快照，零撕裂双字节中文；
- 640×480、1280×720、1920×1080三个原1280×960居中4:3输入候选框位置；真实P441源码复用；
- 6次实际模拟成功swkbdCreate/Show对应6次Close；所有SDL_AddEventWatch/DelEventWatch及SDL_AtomicLock/Unlock生命周期最终配平。

重要说明：每次主线程快照会根据真实竞争期间的文字长度进行附加汉字成对断言，所以总断言数随真实线程调度可能不同。第181轮检测脚本要求**至少2600项源级宿主检查**和固定2,500次完整并发快照，不能错误地把某次2,717项当成每次恒定的数目。可重复运行真实宿主源码测试在最后一个已验时间点返回2,606项。

## 真实Nintendo ARM64及SHA终验

继续使用原P982绝对未改的第173轮48Switch物理AARCH64母版及五个独立真实新增AARCH64适配对象（原BGI九文本输入加锁与Swkbd聚焦、真正P441高清IME矩形、原P454透明GPU绘制、仅QA安全FileCopy、真实libnx swkbd与中文字节拒ASCII）。用真实zig cc -target aarch64-freestanding-none C99与ld.lld -m aarch64elf -r完成物理编译：

- **完整53Switch开发对象**，原113个未解真实解决13个编辑接口加QA FileCopy，剩余**99个未解析**、新增0；
- **以真正游戏main为根的GC裁剪对象**仍保留包括P1015标志读取、swkbdCreate/Show/Close、OS_EditFocus、P454/GPU、P441视口、IPL SHA门禁、原真Noto字体、原MPEG1/MP2+OGG、SaveLoad/SaveWrite及QA FileCopy，并有**81个未解**、无新增；
- 原OS_FileSetAttrs仍未实现，不伪造成功；隔离SDK未验签、GPU和本机Applet均未获Switch实体设备验收；两个文件都是真ELF64 ET_REL部分链接，不是安装包。

真实53Switch机器码：

03_脚本工作区/P1015_第181轮_原BGI聚焦系统软键盘时序_ASCII过滤与真正整合QA/P1017_173orig2der1arch53Switch_swkbdFocusVideo_ASCIIguard_AARCH64.o

真实main可达候选：

同目录 P1017_53Switch_originalGAME_mainGC_swkbdFocusVideo_ASCIIguard_AARCH64.o

完整实际重编、真实Win32双线程宿主、源码/ELF未解测试：

01_工具脚本/verify_p1017_round181_BGIEDIT_focus_realSwkbd_ASCII_noVideo_53Switch_99_81.py

独立SHA/ELF头/全部强定义OS及设备测试门禁复核：

01_工具脚本/verify_p1018_round181_FINAL_true_BGI_Focus_Nintendo_Swkbd_99_81_release_guard.py

两份真实PASS JSON：

- 06_测试记录/P725_第181轮_原BGI聚焦系统键盘_视频时序_ASCII限制_2717项双线程_53Switch99_GC81.json （文件名沿用最初的一次2,717断言运行；报告内部写入实际运行可变断言数，不是每次固定2717）
- 06_测试记录/P726_第181轮最终_原BGI视频初始化与拒ASCII真实Swkbd双线程及53Switch_ARM64_99_81硬门禁.json

## 剩余未解决

Nintendo实际手持/Horizon系统键盘弹出、确认/取消后的SDL窗口重建、主VM阻塞Applets时音乐连续性、Joy-Con编辑焦点、真实中文系统IME候选及完整商业素晴字体特制字槽无法仅靠SDL宿主测试确认。当前最新原CG保持原1280×960高清数据，影片原MPEG1/MP2 25fps和OGG音质不重新压缩，原用户PC Save和正式Nintendo TitleID Save均未触碰。第179轮所有81个main可达候选未解析仍需处理并做最终整机验证。

**发布门禁：BLOCKED_NOT_SAFE_TO_INSTALL。**
