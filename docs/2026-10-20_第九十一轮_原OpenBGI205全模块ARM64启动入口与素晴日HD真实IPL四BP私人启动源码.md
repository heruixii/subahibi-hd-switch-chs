# 第九十一轮：原205引擎从仅有VM对象推进至真实ARM64 main入口 + 私有IPL启动源码层

日期 2026-10-20。根目录 D:/switch游戏/素晴日/素晴日整合/1.游戏合集/移植新版素晴日ns

## 1. 精确从原真实205 C99源码重新构建，而非叠加两个Engine_Main函数

GPL-2.0-only OpenBGI原始源码仍隔离且保持不变、仓库版本 40b144a03e15f159cadc957387e6f94bce8de65f。根据早期P207/P215/P218的原文件与对象逐SHA目录，重链接16个真实VM模块、82个原核心模块、1个ARM64专用引擎入口源、106个原图形/音频/ASM和消息模块，总计205个。除了src/sys/engine.c只读分叉，其他204个源原字节SHA不变。

差异在03_脚本工作区/P486_*中，经p486_proven_upstream_source_delta.json逐SHA复核：
- 在BGI_SWITCH_AARCH64宏下，跳过仅适用于x86的CPUID/CMOV/MMX入场检查。ARM64没有那些x86指令；不伪造CPUID，不修改其它BGI VM/音画逻辑。
- 如果用户的games.json不存在，则默认profiles只存RAM，禁止OpenBGI自动把games.json写回到SD、游戏安装目录或Save。不会绕过原解压/画面/音频等剩余真实依赖。

P487用四段AArch64重新链接源对象，205源＋前轮51个原BGI宿主OS ABI形成新的Machine183 ELF64 ET_REL 9359192字节；SHA256：73971ddea19737edafc0805623d57fb014ff714f14ce97568c0cb28ab50ff3a7。尚缺原OS接口135。仅靠这项修改不等于真实游戏引擎可运行。

## 2. Switch SDL生命周期和真正的process main入口

P488专门实现OS_Init/OS_Shutdown/OS_SetArgv0，SDL_Init(SDL_INIT_TIMER|SDL_INIT_EVENTS)成功才认定引擎基本服务初始化；真正GPU窗口、手柄、音频在各自原BGI OS接口单独初始化；失败返回false，shutdown幂等，无写Save。新主机模拟检测SDL启动失败、重复调用、退出清理、再次初始化均PASS。

使用原隔离GPL2源码src/sys/main.c的真实main函数，而不是主观设计的假入口。P489将main、Engine_Main、OS_Init、OS_Shutdown和51个宿主接口真正合并ARM64，大小9367016字节，SHA256 1b2b2ded3305e652f8a67bb70ad0f2645352bb6c0bb3f62ca0c17cb297e5ea9b。缺原BGI OS接口135，合计待解析外部符号249项。

P490再只作为数据对接隔离的Switch libSDL2.a/libnx.a/libEGL.a/libGLESv2.a真AArch64归档，完成可重定位静态链接的目标文件39653000字节SHA256 71414bf139a119146065ee1bacb8b8a1c13b595a9ea4107d4962fb93f9b0160c。SDL_Init、SDL_Quit已从实际SDL归档补齐，最后仍有415个外部符号未解析，其中135为原BGI OS；**不是Switch最终可执行ELF/NRO，未进行GPU/音频硬件测试**。

## 3. 原版SubarashikihibiHD IPL和实际依赖源证据

原PC真实IPL位于04_HD转换样本/P2_扩展归档/system/ipl._bp，字节3344，SHA256 4c86a967974ba8a1aecae3af2b9750762c70ad9e61a3025b6f1b92ad1c28512f，原脚本内部确实携带SubarashikihibiHD标记。

P491从原编译IPL实际字节定位四个名字：sysprg.arc、environ._bp、bitmap._bp、prtclctrl._bp。三份BP解包源码均位于P2原始归档sysprg下，有逐字节原SHA，但是完整sysprg.arc和system.arc归档没有找到。已有解包BP不等于原VM支持文件夹代替归档，暂不捏造BGI虚拟归档执行成功。

P494仅把原IPL和上面3份原BP文件另存到05_NS测试构建/P494_原IPL_三必需BP私人启动源码层_不生成NRO_未验证剧情/OWNER_ONLY_DO_NOT_PUBLISH/story下，总计22064字节4个文件，与原母版逐SHA完全一致。.gitignore明确屏蔽商业启动BP的公开提交；原有82文件私人QA SD与旧NRO字节不变、从未在本轮组装/安装新的Switch包。这个P494仅是本地私人启动源码**层**，不含完整资源与system.arc。

更重要：P496独立检查OpenBGI GPL2内置games表和真实IPL，原IPL标识SubarashikihibiHD没有默认精确匹配，且当前GPL源码未证实原BGI1.647正确profile。不能靠版本接近强行选择1.640或1.653，否则可能破坏原VM/BP、存读档及字幕位置。需要针对原1.647源码、真实opcode和BP系统功能作独立验证，再选择配置。

## 4. 全部质量与不可发布边界

P492 以最新源码重新执行第90轮原游戏读盘/线程/音频宿主接口质量回归、完整205 C99对象替换重建、真实main链接、IPL原文件SHA依赖。PASS，用时4.71秒。P494原4份私人启动BP字节验证PASS。中央总门禁新增304条作者自建条件经P497前置检查PASS；完整历史中央媒体质量门禁没有在本轮重跑，不能混淆两种验收。

本轮没有编辑或重压缩新版1280×960 PNG/Alpha、原Vorbis OGG、五段1280×960原高清影片25fps/48kHz、已有中文译本、旧非剧情QA NRO、用户原任天堂TitleID/Save。OpenBGI LGPL声明未经证实，按实际GPL-2.0-only源码与衍生二进制义务对待；严禁把玩家商业游戏母版与GPL源码融合后公开为可下载完整游戏。

## 5. 接下来无需重复做历史诊断包的具体任务

优先研究原Buriko的1.647代际profile和原IPL中sysprg.arc的解包文件夹替代载入，禁止无证据猜测；继续必要135 BGI OS函数，完整原音画/影片与原事件选择/分支，实际完整SDL2/libnx/C runtime ELF启动链接，最后在用户自有NS上核实标题菜单、首段连续场景、44.1kHz/48kHz配音、GPU画面、TitleID/Save隔离。真实BP/VM、影片、音轨未实机执行，所以仍是BLOCKED_NOT_SAFE_TO_INSTALL。
