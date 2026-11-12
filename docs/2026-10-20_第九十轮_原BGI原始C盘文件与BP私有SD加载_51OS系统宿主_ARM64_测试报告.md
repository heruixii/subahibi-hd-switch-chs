# 第九十轮｜原BGI原始C盘剧情/BP加载真正对接主人NS私人SD

日期2026-10-20；项目主目录为 D:/switch游戏/素晴日/素晴日整合/1.游戏合集/移植新版素晴日ns。

## 原生工程已完成

从205个真GPL2 OpenBGI C99/ASM 引擎源模块与上轮35个Switch SDL2/libnx平台宿主ABI继续推进，未添加来源不明的引擎VM虚构实现，也未覆盖PC或Switch原始游戏母版。

P473/P474：真正原BGI Windows C: 盘私有只读路径转换，将 C:盘的 sysprg/scrsys._bp、data01101/1-1_0710_dream 等原编译故事/BP文件名映射到 sdmc:/switch/subahibi_pc_native_hd_qa/story/ 树。原始音频的完整 sdmc 字面路径保持不变。相对文件名按照隔离的虚拟C盘当前目录解析。测试拒绝 ../、./、UNC、其他驱动器、过长串、混合分隔符、Switch安装TitleID/Save；文件系统不会接受源修改、创建或删除。原主人SD必须满足没有符号链接或恶意挂载等前置条件，尚未经过Switch硬件检验。

P475：原BGI的5个只读文件接口替换为上述带虚拟C盘的SDL_RWops实现，另增加确实被VM调用的5个游戏/执行文件目录接口。205原引擎真ARM64合并后共40个接口，SHA256 be18bb6c603d8aa5fd87ba835fb94541c5930b7f4f96e340a5487e9b8dfee368。OS未解144。

P476/P477：增加真正原BGI FileAttrs、ReadNativeFile、NativeOpen三接口，原生配置games.json字节+结束NUL测试PASS，只有已验证的私人目录获得目录属性，读取文件必经原只读路径防护，native文件仅允许rb；兼容配置最大16MiB。新增3个真原引用符号，累计43接口，OS未解141。

P478/P479：依SDL2正式规范的可重入recursive mutex实现LockCreate/Destroy/Enter/Leave，并使用ARM64 GCC seq-cst原子加减实现AtomicInc/AtomicDec。递归3次与原子值主机模拟测试通过，6个接口有真实代码，但仅4个原来缺符号，故OS未解141→137（不伪称6个缺口都消除）。

P480/P481：真BGI ThreadStart/ThreadJoin生命周期转换到SDL_CreateThread / SDL_WaitThread，保留原void工作函数、原参数、普通或高优先级；失败/等待/资源释放测试PASS。增加2个原来未解OS符号。205个真实引擎模块 + 51个BGI宿主API的AArch64 ELF64 ET_REL大小 9359728 字节，SHA256 f4f7f0b74074d4e0caf6ed159ce540edfd3dc798e758cdf7d03a3e20ecc9742d，原BGI OS未解剩余135，未生成可安装完整游戏NRO。

## 源材质完整保持新版质量

原高清1280×960 RGBA/Alpha、原压缩OGG、52汉化私有旧中文字幕、五部原高清25fps/48kHz影片不改写不缩图。既有1280×960 SDL2持久离屏GPU画布、精准双声道44100/48000Hz PCM回调、控制器真实实例ID、手柄摇杆及4:3显示比例均保留。Windows虚拟C盘不会映射玩家存档或原任天堂安装目录。

## 原始启动文件差距不是理论，而是从磁盘查实

原始IPL启动BP文件在原始P2归档中找到：04_HD转换样本/P2_扩展归档/system/ipl._bp；原字节长度 3344，SHA256 4c86a967974ba8a1aecae3af2b9750762c70ad9e61a3025b6f1b92ad1c28512f。但是先前82个主人私有SD测试文件里不含原IPL文件和games.json配置。现有82个目录仅供隔离质量测试，并不是商业游戏的完整源资产；完整system.arc及原1.647 BGI/BP脚本兼容尚未证明。此轮仅记录来源和差异，没有频繁重新打包或复制到公开包。

## 质量与发行范围

P482原BGI路径/Native配置/递归锁/线程共5项自写源码 + 真ARM64编译 + 82份主人私有资源SHA核对 + 原非剧情NRO不变的快速门禁通过，用时5.68秒。P483在正式中央脚本内新增加质量条件，254项逐项前置预检PASS，完整历史媒体扫描不在本次执行，不能称中央全量已经重跑。

仍需要：原BGI1.647真实BP/VM动态执行与完整存读档隔离、真实全部游戏源和IPL打包布局、至少135个必要OS宿主函数及其真实系统依赖、标准C/C++/EGL/GLES运行时的真正NS可执行文件最后链接、真实Switch GPU/DAC/声音时钟/手柄实机试验。所有用户母版、旧NRO和Save未被替换。严格发行状态 BLOCKED_NOT_SAFE_TO_INSTALL。GPL-2.0-only衍生二进制分发需遵守GPL源码与版权条款，不公开释放用户商业素材。

## 第90轮追加：原始205模块＋51宿主接口实链接到隔离SDK图形、手柄与音频库

使用经SHA保护的P481原生ELF64 AARCH64机器对象，继续与隔离的Switch libSDL2.a、libnx.a、libEGL.a、libGLESv2.a仅在Zig -r可重定位方式链接；**没有执行任何第三方二进制，未生成NS游戏NRO**。真实结果P484链接成功，AARCH64 ET_REL大小39645840字节，SHA256 5eec2947972006279cd72de03c00c12a1fadc61bb95dba3f6bf01f4dda203d3d。其中SDL_CreateMutex与SDL_CreateThread从SDK SDL2库中真实消除了未解符号，但原BGI OS_*仍缺135，合并SDL2/libnx/EGL/GLES后整个程序仍缺416个外部及运行时/CRT/GL符号；仅成功部分静态链接不等于可以运行或完整剧情引擎已适配。

本轮原质量门禁已补全上述SDK链接和线程证明，P485共261条中央新增条件独立预检PASS。耗时的历史多媒体全部门禁未重新执行。全部既有PC高清资源、OGG、原影片、汉化原文、用户私有SD及Switch旧NRO和Save无写入。
