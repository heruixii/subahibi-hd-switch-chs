# 第九十二轮：真实OpenBGI LoadFile加载全部55个原始编译BP源

日期：2026-10-20。目录：D:/switch游戏/素晴日/素晴日整合/1.游戏合集/移植新版素晴日ns。

## 实际移植进展

原GPL2 OpenBGI的core/loadfile.c默认先尝试读取松散文件，再访问归档。游戏原ipl._bp可以直接按loose文件路径读取；sysprg.arc内的脚本原源已有54个解包后的._bp文件，但当年打包的sysprg.arc和system.arc没找到。原始真IPL内的产品标识为SubarashikihibiHD，引用sysprg.arc、environ._bp、bitmap._bp与prtclctrl._bp。

P498：原真实GPL2 loader.c独立只读派生，对字面sysprg.arc中的严格ASCII安全basenamed ._bp文件在原根目录loose读取失败后尝试sysprg/同名文件。修改了真引擎六项文件载入、分段读取、解码范围、尺寸和存在判断：LoadFile、LoadFileRange、LoadFileRangeDecoded、GetFileSize_、GetFileSizeFast、FileExists。反例拒绝错误归档、存档、目录穿越、其他盘符、混合斜线和不安全文件名。保留正常loose文件读取优先级、原DSC/CompressedBG解码和原ARC管理器；不合成假sysprg.arc或修改原VM指令含义。

P499：在PC主机上真正编译原OpenBGI GPL2 LoadFile函数并接入只读文件mock，逐字节读取真正原ipl._bp 3344字节、environ._bp 2128、bitmap._bp 10912、prtclctrl._bp 5680；0次合成ARC访问，全数原字节匹配。这里验证的是实际LoadFile C99函数路径，非真实游戏剧情VM运行。

P501：私人只读启动源布局独立整理全部54份原sysprg ._bp共316560字节，再加ipl._bp 3344字节，共55份源文件、319904字节，全部源SHA256逐文件比对通过。目录为05_NS测试构建/P501_私人原IPL加54全系统BP解包源_未安装未组NRO/OWNER_ONLY_DO_NOT_PUBLISH/story/。这些是用户自己提供的商业原始素材，单独本地存放、.gitignore防发布。未覆盖旧82文件私人SD QA及旧NRO或任天堂游戏存档。

P502：使用同一份真实原OpenBGI LoadFile C99目标文件，对上述55份真正编译BP逐一读取，返回长度及文件全部字节与原始源完全相同，55/55 PASS。这个测试没有合成系统归档，且没有进入剧情。

P500：由16个原VM C99对象 + 81个原核心对象 + ARM64适配engine.c + ARM64适配原loadfile.c + 106个原图形音频ASM对象，真实还原原205个GPL2源引擎模块。外加独立安全path resolver和此前51个真正BGI OS宿主接口，接入原Main入口、SDL Init/Shutdown、原44.1/48kHz声音拉取、手柄、持久高清GPU及用户源只读文件桥。唯一两个GPL2派生源码为engine.c(去除x86硬件CPUID/MMX误阻断并禁止自动写games.json)与loadfile.c(原BP解包回退)；其余203份源码保留原字节SHA。

新原ARM64 Machine183 ELF64 ET_REL文件长 9373968 字节，SHA256 891c8a73ab7971cfddfc41492a67b21a10e125c3b9565659a75ed8a718654a05。与原Switch SDL2/libnx/EGL/GLESv2 SDK静态档案AARCH64进行可重定位链接，结果 39659936 字节，SHA256 6c1083f90c24f2506fc90eac5e432e892d55769befa8e53e3e84d5bd3eb06279。仍缺真正BGI宿主OS函数 135 项，静态链接全体外部符号 415 项；它不是可执行NRO。

## 重要安全与引擎差距

原BGI 1.647的游戏识别、BP操作码0x56等及sys_::f_120效果完整运行语义仍未经证明，不能把OpenBGI邻近1.640或1.653 profile冒充适配成功。直接操作ArcMgr_Read/ArcMgr_Exists等其它归档API并未一律纳入本轮回退，也未测试全部用户商业媒体和压缩纹理流。

新增55份BP私有启动源与老82份原高清/OGG/中文私人SD测试树目前是两个隔离目录；在真正NS上读取这些源文件需要组合经过SHA和路径验证的私人布局，不应直接把它们当作可运行安装包。任天堂硬件GPU、DAC、Save、全幕脚本分支、高清原影片播放均未测试。

原高清1280×960 PNG/Alpha、OGG原压缩数据、五段高清25fps/48kHz影片、旧中文版原翻译和任天堂TitleID/Save不改写、不降画质、不降采样。商业媒体不允许直接公开GitHub发布；GPL2引擎派生代码有源码与许可证义务。

P503开发快速完整现阶段源门禁PASS 7.71秒，含真LoadFile对全部55份源BP重新编译并逐字节读取、路径负例、真ARM64联接、旧82原媒体和旧NRO逐SHA不变。P504中央共 329 条新增作者条件预检PASS；全项目耗时历史媒体总闸门并未在本轮重跑。

后续优先：原1.647准确profile/真实VM BP opcode、剩余直调ArcMgr分支、原SD私人55BP+原高清媒体严格SHA布局、135 OS缺口与415外部依赖直至NS可执行启动、最后实机剧情/声画/Save验证。禁止为了制造进度重复制作非剧情NRO。安全状态BLOCKED_NOT_SAFE_TO_INSTALL。
