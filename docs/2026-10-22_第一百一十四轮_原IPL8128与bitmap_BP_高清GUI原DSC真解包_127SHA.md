# 第114轮：真实IPL→environ→bitmap模块，8128条原指令与原版1280×332 GUI真实解码

日期：2026-10-22

工程目录：D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns

## 真实原IPL执行进展

本轮已保存P412–P425及最后P424中央审计记录，所有成功项均是原版权BP和原OpenBGI GPL2 C99源码的隔离Windows宿主实测，均为私人非发行阶段；原游戏、实际玩家存档和原高清母版未修改。

1. P661/P412：原A0:08 BGM主音量，经原Opcode_Snd_BgmMasterVolume、CheckVolume、CheckBgmChannel和Bgm_SetMasterVolume真实执行，6025条，WaveMaster后台仅记录音量参数，未播放音乐。
2. P662/P413：原A0:09音效槽总音量，6803条，累计15次Call和13次Ret，记录12次BGM及32次音效增益写入；原OGG及音频硬件输出未验证。
3. P663/P414、P664/P415：原80:1B键组映射设置5次和80:62全屏切换键绑定1次，原输入表结构实际更新，执行至6925条并返回IPL，累计15次Call和15次Ret。
4. P665/P416：用原GPL2 Thread_LoadModule正确登记主IPL为第一模块，再加载environ；调用原Opcode_Sys_UnloadProgram和Thread_UnloadLastModule，真实卸载environ，保留主IPL唯一模块、3328字节原代码全等。达到6939条。
5. P666/P417：原80:64 ShowMainWindow、Input_ClearStates及80:46 GetThreadId已执行，宿主仅安全记录窗口显示请求；推进至7929条。
6. P667/P418：真实整批原GPL2整数/位运算函数，尤其原Not已执行2次，推进至8028条。
7. P668/P419：原90:0C全局消息窗口可见性和Alpha、90:4C背景显示参数、90:00提交重绘执行；后台背景绘制使用严格无画面的指令记录适配，不是Switch真正GPU合成。推进至8036条。
8. P669/P420：逐一用原主人SHA校对54份sysprg系统BP文件，启用严格单目录/文件名白名单，再由原GPL2 Opcode_Sys_LoadProgram和Thread_LoadModule真实加载bitmap._bp。推进至8117条，已加载environ与bitmap两次，当前主IPL与bitmap两模块共14224字节。
9. P670/P421：原bitmap._bp使用90:07设同步图片加载窗口100ms，推进至8128条。**特殊版本证明**：原PC BGI1.647操作码表90:07真正处理器为x86地址0x481850，在0x402210将值存至0x572220并清零0x572224；虽然上游GPL2操作码版本标记为1.69.472以后，原PC实际支持，故采用原机证据。
10. 下一条原真实VM指令为bitmap._bp中的**PC 0xE7F，90:10（BmpLoad）**。原bitmap槽1025，归档sysgrp.arc，条目SGMsgWnd990000。尚未在同一个原VM执行器里运行90:10的加载、合成和GPU上传全套逻辑，禁止称标题或游戏画面已可运行。

## 已真实打开的原版PC高清GUI

- P671/P422：真实原GPL2 ArcRead_OpenFile/ArcRead_Find在用户PC原文件sysgrp.arc（34,737,544字节，SHA256 8be431fb6506b1c35d2c57b889982e90173a55d28830b1862a1bfbd94e547016）读出BURIKO ARC20索引共327项；SGMsgWnd990000位于源文件偏移12033548，保存的DSC压缩数据118715字节。
- P672/P423：实际编译并执行原GPL2 ArcRead_Load、DscBuildTree、DscDecodeStream、BGI_DscDecode以及BGI_HashNext，将该条目在内存里解出1699856字节；原图片尺寸**1280×332、32bpp、format0**，全部解码数据FNV1a32为**3383c851**。图片未被保存、降分辨率或替换。
- P674/P425：将上述原生解码数据继续送入原GPL2 RawImage_Unpack与BmpOp_PutRaw，抵达原BmpMgr_PutPixels的隔离参数/像素哈希宿主边界，原图片槽1025，**PM_ARGB32、1280×332、1699840像素数据字节**，像素FNV1a32为**0404afa1**。此处使用严格无GPU的BitmapMgr宿主事件记录，尚不是NS实际GLES/SDL画面。

以上过程只读原PC归档，并无导出/改写原图片像素文件，亦未制作任何含商业图像的可公开安装包。

## 集中质量闸门P673/P424

**PASS（范围受限，非发行）：**再运行上述实际原GUI DSC和原BmpOp_PutRaw源码C99测试；鲜读私人完整127份原始HD PNG、OGG、25fps电影、Noto字体及BP文件SHA256，共39,772,982字节全等；已编译的205 GPL2 VM＋85 NS宿主接口的AARCH64 SDK ET_REL旧目标文件（40,378,224字节）再次核对SHA256 ad9459c2b87811b51c110cd3a9d3d707b9e544021273333583cd4efc6975b9d7；中央1163条作者静态质量条件重新执行PASS。额外确认了原PC sysgrp.arc完整SHA未变。

**独立构建问题尚在：**本轮尝试全套历史Zig 0.15.2 P576 ARM64 SDK重编译，反复出现编译器error: Unexpected。之前已经存在的AARCH64 ET_REL对象SHA仍通过，并不能据此声称本轮Zig全量重构建通过。后续优先隔离Zig缓存或切换受信任工具链重新编译。仍剩101个未实现NS OS接口、384个链接外部符号；没有可玩的游戏NRO/NSP，尚未实际在NS运行游戏标题、原音质/影片、手柄输入或游戏存档。

## 下一段连续目标

1. 从真实bitmap BP的0xE7F的90:10出发，在原VMLoop中打通原BmpOp_LoadFile→原ARC20/DSC→原BmpOp_PutRaw、BmpMgr真实缓存与SDL2/GLES 1280×960 RGBA管线；先验证像素全等、8MiB代码区及32MiB图片读取缓存内存上界，严禁CG缩到800×600。
2. 继续加载原54个系统BP白名单中的其它实际脚本，逐步进入真实title._bp标题UI及VmMain，验证剧本/声音/影片/输入和隔离存档。
3. 处理Zig的Unexpected问题并完成NS硬件构建、101 OS及384 external缺口的真实链接和运行回归。在这些阻塞解决前保持安装门禁BLOCKED_NOT_SAFE_TO_INSTALL。
