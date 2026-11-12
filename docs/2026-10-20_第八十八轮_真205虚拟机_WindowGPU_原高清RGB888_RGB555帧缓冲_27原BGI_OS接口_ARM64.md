# 第八十八轮｜真实OpenBGI虚拟机窗口、渲染与原帧缓冲进入ARM64

日期2026-10-20。原PC素晴日HD新版移植NS任务，工作根目录：
D:/switch游戏/素晴日/素晴日整合/1.游戏合集/移植新版素晴日ns

## 1. 工作重心与版权/数据隔离

本轮没有改写或重新压缩原高清1280×960 PNG/Alpha、原OGG、五段原高清25fps/48kHz影片和既有旧ONS翻译资源，也没有修改任何用户Switch存档、已安装TitleID或旧私测QA NRO。全部真ARM64引擎代码仍为**可重定位ELF目标模块**，不是已链接的Switch可运行NRO，更不是整个原1.647故事/BP VM已执行。

冻结的开源GPL-2.0-only OpenBGI真实C99引擎205模块继续复用：16份VM、83份核心/等候/脚本模块与106份音画/ASM等模块。GPL源和license只留在独立07_工具链环境/P419_*目录，不自动提交公开仓库或包含本作商业CG和汉化翻译。未来公开分发GPL衍生二进制需要遵守许可证源码义务；商业游戏的原素材没有由此获得重发布许可。

## 2. P445/P447：原BGI Window API -> 真Switch SDL2 Window/Renderer

已新增真正的C99 SDL2窗口/renderer资源管理源：
03_脚本工作区/P445_Switch_SDL2_Window_Renderer_Lifecycle_原高清GPU_主机真ARM64/p445_Switch_BGI_SDL2_window_renderer_frontend.c

九个原BGI OS Window API逐个以真实SDL2功能实现：OS_WindowCreate、OS_WindowDestroy、OS_WindowAlive、OS_WindowShow、OS_WindowActive、OS_WindowClose、OS_ScreenSize、OS_WindowMove、OS_WindowGetRect。其中7个本来就是205模块的真未解析OS引用，已被新增AARCH64机器码满足；另外2个确实新增可调用符号，但在当前底层引擎没有直接调用，故不能虚构为消除了9个原缺口。P447实际未解OS总数由169降低到162。

按照上游原inc/bgi/os.h约定，创建窗口隐式触发created回调，销毁在真正清理GPU之前触发destroyed回调；OS_WindowClose不强制中断VM或Save，而是在下一次BGI输入消息泵发出close_request供脚本决定。SDL video和controller子系统按创建和销毁生命周期管理；窗口新建、SDL renderer初始化或第一个GPU清屏失败时都实测回收资源，不留下半初始化设备；重复创建与重复销毁负例通过。

窗口尺寸是**SDL输出区域**，不能因为旧OpenBGI文档默认800×600，就将PC高清CG变为800×600。本源继续调用P441原高清GPU 4:3视口（掌机1280×720显示960×720原纹理居中，左右黑160；HDMI1920×1080显示1440×1080，左右黑240），拒绝旧800×600诊断CG当原生1280×960纹理。P438输入桥的虚拟键盘、真实控制器实例ID、摇杆滞回、手柄热插拔及鼠标1280×960逆坐标映射由窗口生命周期显式连接。当前未完成正式BGI的CP932游戏标题转换，故SDL窗口使用固定UTF8私测标题；不将日语CP932源字节错误发送到SDL。

P447真实Window API连同原205模块和13项旧输入/SD/时钟ABI合并AARCH64 Machine183 ET_REL，大小 9278496 字节，SHA256：
2d8f7a467249c307ccee4045b4b27d54fd9bc118902c030047c318c04d95a394

## 3. P450/P451：真正的BGI图像数据帧缓冲接入SDL2 GPU

新增文件：
03_脚本工作区/P445_Switch_SDL2_Window_Renderer_Lifecycle_原高清GPU_主机真ARM64/p450_real_BGI_OsSurface_to_Switch_SDL2_Texture_CG_Blit.c

直接依据真实GPL2 inc/bgi/os.h 与 src/gfx/mgr/frame.c、src/sys/present.c、src/os/posix/window.c API适配：
- OS_WindowGetDc / OS_WindowReleaseDc：对应SDL_Renderer的受限借用画面/释放；一批绘制合并后才SDL_RenderPresent，不在每个小CG块后立即present。
- OS_BlitToWindow：原 BGICPU OsSurface_t 32-bit XRGB8888/0x00RRGGBB 或16-bit RGB555，使用原pitch/宽高通过SDL_CreateTexture+SDL_UpdateTexture直接上传到GPU，原源像素不重新编码。
- OS_StretchToWindow：将源BMP区域拉伸/裁剪进原逻辑1280×960 4:3窗口坐标映射，剪切后恢复正常clip状态。
- OS_WindowFillBlack：实现原Bgi黑屏填充，新的GPU输出屏幕使用真实SDL_RenderClear+SDL_RenderPresent。

完整原1280×960 framebuffer的dirty rect请求现在会**重新绘制完整1280×960当前源画面**，以防SDL_RenderPresent后backbuffer无保证而只绘小块导致黑洞。这个完整重绘回退正确性优先、效率未优化；对于只有小块叠加图片、前一帧backbuffer没有永久保存的情况，**跨帧像素合成还没有保证**，下一步需要保留离屏目标纹理或完整GPU混合场景图并实机校验。这是本阶段明示的功能缺口，绝不写成“全部动画/对话框正常”。

P450主机模拟使用SDK真实SDL2头文件、无游戏版权图片，仅用6字节/合成小块和静态原尺寸假像素测试：1280×960 32位源上传、RGB555小纹理、原BGI绘图区裁剪/4:3位置、dirty rect full-source保护、同一Dc合成时不重复清屏、释放后才present、错误24位源/不足pitch拒绝、贴图生命周期严格平衡。没有任何外部平台音视频播放器运行。

新5个图像OS ABI确实在205份底层C99里有缺失引用，并全部得到真正ARM64机器定义，未解BGI OS从162下降到157。与前述9个窗口API、13个输入/只读SD/时钟API合计**27个真实实现**。新增SDL2纹理/窗口真实函数仍是未解析的最终链接依赖，总计252个。没有假装用空stub完成真实GPU或游戏剧情。

P451真 AARCH64 Machine183 ELF64 ET_REL合并产物 9298280 字节，SHA256：
3bac54e24004fb6aed1063467ff4d906073207e1f5f3605c285e92c1d4a309b3

## 4. 本轮快速质量与累计状态

P231：9个原Window API + 前13个OS接口与GPL205模块真ARM64；主机窗口与GPU失败处理。
P232：再加5个真正BGI RGB888/RGB555帧缓冲GUI绘制API，主机错误分支+原GPU纹理调用/完整源码SHA。
P233：同时重跑原82私人源+手柄+高清GUI+窗口+帧缓冲5项实测工具，耗时约9.2秒。对旧P412非故事诊断NRO逐SHA复核，原文件内容不变。
P234：把本轮新增真实接口与上一轮原BGI/BP音画安全条件加入中央门禁脚本，已完成179条新条件的独立预检。为遵守“适当加快移植速度”要求，本轮不重复此前极其耗时的历史全媒体质量闸门；P229第87轮全量历史测试末行已PASS（发行仍阻塞），最新P88源码的全量历史门禁尚未重新运行，不能假称通过。

旧P229全项目状态：BLOCKED_NOT_SAFE_TO_INSTALL、PRIVATE_BUNDLE_FILES4324、UNVERIFIED_EFFECTS69、NO_DIRECT_RENDERER20、PYTOOLS442。P230另外一次同时运行的全量历史扫描曾因编译器并发发生链接冲突，不把该失败当成P88已过测试。P231/P232/P233/P234均按当前源码独立通过。

## 5. 下一阶段优先顺序

首要缺口已经从手工中文字音画QA转为**跨帧GPU图层保持与真正NS SDL2静态链接**。后续还需157个BGI OS接口中的必要系统/文件/音频/定时器服务，原BGI1.647商业引擎的实际脚本opcode兼容性及title._bp的fixmul完整栈/舍入语义，真实剧情分支/选择/自动音轨/CG/OP与Save/TitleID隔离，以及实际NS GPU/DAC/hbmenu/控制器验证。五部PC新版高清MPEG视频、音轨及原OGG压缩比特流均应沿用母版，不可降质或重压缩。

**此版本不可安装、不是可玩游戏，不应公开发布含商业原素材或译文包。工程安全闸门仍为BLOCKED_NOT_SAFE_TO_INSTALL。**
