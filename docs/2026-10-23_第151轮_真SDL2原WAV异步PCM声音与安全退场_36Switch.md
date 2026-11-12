# 《素晴日》新版PC高清移植Nintendo Switch｜第151轮真实WAV音效适配与质量记录

2026-10-23。工程 `D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns`。

## 一、基线与实际优先级

按权威P678续接，上轮**175份未修改GPL-2.0-only上游OpenBGI C99＋1份GPL2原引擎ARM64架构条件适配版＋35份互异Switch libnx/SDL2/GPU/PCM/HD字形/私有SD源码**，真实AArch64 ET_REL Machine183**39,471,208B、130项真实未解全局符号**。原游戏主线程真实停在IPL**225988**、PC**0x20E4D**；PC**127份原版1280×960 CG/OGG/25fps影片/字体/BP合计39,772,982B和玩家Save均不可改写，绝不降画质音质到旧Switch版800×600素材**。

真实原GPL2上游`src/snd/sound.c`的`Sound_PlayWave`通过`OS_PlaySoundFile(path)`实现原x86 Windows `PlaySoundW(...,SND_FILENAME|SND_NODEFAULT|SND_ASYNC|SND_NOWAIT)`；上一轮此符号仍在130项真实缺口中。它是**剧本里的独立WAV音效**接口，不是原OGG配音、WaveMaster内部Vorbis混音或原MPEG1/MP2电影解码接口。第151轮不虚构电影成功，不假称OGG变成WAV后音质不变。

本地SDK查验：实际主`07_工具链环境/.../opt/devkitpro`包含官方`libSDL2.a`和可物理使用的SDL2音频API；另有隔离存档`07_工具链环境/2026-10-19_原始OGG音轨Switch音频SDK历史包隔离来源未验签/data_only_staged_portlibs_ogg_vorbis`，可看到真正`libogg.a`、`libvorbis.a`、`libvorbisfile.a`和`libSDL2_mixer.a`等旧历史ARM64静态库，**签名来源未独立复核、不是当前P678主SDK自动包含的完整游戏OGG后端，也不意味着任何MPEG电影现成可播**。早期确实有独立“非游戏/未上机”的44.1kHz Vorbis原音轨探测NRO/P260+P299等实验，未来应严密区分其独立诊断功能与真正OpenBGI游戏原音画完整引擎。

## 二、P932/P679：实际读源WAV、实时异步SDL PCM队列、严禁不支持时伪报成功

新增GPL2标注的Nintendo源：

`03_脚本工作区/P932_第151轮_真正SDL2原WAV一次性音效不占用原OGG混音/p932_switch_true_original_WAV_SDL2_nonblocking_sound.c`

真正补齐原`OS_PlaySoundFile`缺失API。先通过上轮真实**P473/P474** Win32虚拟C:\当前目录与`sdmc:/switch/subahibi_pc_native_hd_qa/story/`严格只读路径映射，保证文件真实位于项目私有**story/**源树，拒绝`D:`、`..`、非业主Title、Save等目录访问，仅用SDL `SDL_RWFromFile(...,"rb")`读文件。真正`SDL_LoadWAV_RW`解析原波形数据；严禁把非法/空WAV、过大文件、不支持的采样率/声道/PCM格式当成已播；不调用原游戏写入函数，也不对媒体转换/重编码。

对受支持的PCM，`SDL_OpenAudioDevice`请求**原始采样率、原格式与原声道**（采样率8k～96k范围，U8或系统16位整数，单声道或双声道），`allowed_changes=0`，再次比较`got`与`want`完全一致，不能为了硬件兼容静默将**44.1kHz改成48kHz**。仅当真实`SDL_QueueAudio`接受原样字节后`SDL_PauseAudioDevice(dev,0)`启动队列并返回1；失败、设备缺失、SDL拒绝队列时返回0，绝不伪造`SND_ASYNC`成功。Win32 `SND_NOWAIT`语义保留：之前独立WAV队列尚忙时返回0，不为新请求覆盖它；队列排空后可安全释放之前一时音效设备并重新开同类设备。实际为音效单独申请SDL音频设备——**不能假定真Switch后端支持同时使用另一个OpenBGI配音/背景音乐声卡**，是否多声卡和音质/动态混音能同时通过必须由实体机确认；设备拒绝会失败关闭，不强行抢占既有混音设备。

强Nintendo `main`由本轮`p932_nintendo_main_with_original_WAV_cleanup.c`代替前轮P930强`main`（**不可同时链接两份强main**）。保持`userAppInit`真实检测私有SD/ipl._bp和安全`orig` GPL2原机器码入口的二次检测，结束`orig`后调用`P932_ShutdownOriginalWave`只停止自身单独占用的WAV队列和SDL音频设备，保留原GPL2 `OS_AudioStop`/OGG混音拥有者管理的其他设备；原CG与Save零变更。

**同一份实际ARM64 C99源码**宿主编译并执行**20项音效合同＋6项主入口/退场合同＝26条全部PASS**：包括五种不合法源路径零IO、缺WAV、不支持的音频格式、0频率、3声道、初始化失败、实际音频设备拒绝/采样率偏离、`SDL_QueueAudio`失败、队列忙时不覆盖、返回真实接受成功后释放所有分配、退出时幂等关闭自己设备、拒绝`--extract`与不安全存档路径。宿主对SDL函数的应答是受控fixture，**没有实机喇叭播出事实**。

真正ARM64重新由P910未链接EngineMain的**173原GPL2＋24平台**基线物理起步，再放入上轮2份未修改GPL2源码main/hvl、1份GPL2-only ARM64引擎条件适配、9批旧真实Switch SDK原生适配目标、P930原CRT`userAppInit/Exit`及本轮2份新SDL WAV与新main机器码；通过真实GNU C++、SDL2、libnx、newlib SDK进行LLD AArch64 ET_REL局部链接，**最终175未改GPL2＋1GPL2 CPU条件改版＋36份Switch真正原生对象**，无重复`main`定义，`OS_PlaySoundFile`有真正SDL音频机器码，旧130个未解中**仅它1项真正消失、没有新增→129项**。

P679权威JSON：`06_测试记录/P679_第151轮_真实SDL2原GPL2异步WAV音效26宿主与ARM64_129符号.json`。AArch64 ET_REL ELF64 Machine183物理产物：

`03_脚本工作区/P932_第151轮_真正SDL2原WAV一次性音效不占用原OGG混音/P932_175_Original_plus1GPL2adapted_36Switch_trueOriginalWAV_SDL2_AARCH64.o`

实际**39,605,528字节**；SHA256 **`a9a68275ae938ef0c4d2a33a3e28db17d34ddea80573caf625c771378d9e2714`**；真实129个缺口名单`P932_true_native_unresolved_129.txt`。这仍是实际物理AArch64 `.o`，**不是可安装的Nintendo游戏NRO/NSP**。

## 三、真正OGG、MPEG影片与GPU仍是关键阻塞

原GPL2 `src/gfx/movie.c` 依赖`OS_MovieOpen/Start/Stop/SetVolume/IsRunning`实际电影驱动；走原`src/sys/moviefx.c`外部FFmpeg进程作为替代，但真实Nintendo Applet不是PC/Windows FFmpeg CLI。当前完整游戏未接入可运行的MPEG1视频/MP2音频实时解码、40ms逐帧PTS和音画同步，也未达到1080p/1280×960 CG画面实机GPU完整逐帧验证。不能为降低未解数字把`OS_MovieStart`写成无播放仍返回1。已有音频实验的私有SD OGG Vorbis历史静态库签名与其是否适用于最终游戏还需要专门复核；原版压缩码流、采样率、时间戳不能改变。原商业母版和用户原存档保持只读。

## 四、完整历史门禁、发行限制和续接

最终全量回归脚本：

`01_工具脚本/verify_p933_round151_final_originalWAV_full_HD127_1163_GPL2_36Switch.py`

它需从P931整条历史质量链重新运行原PC **127份高清源逐SHA256、1163项历史开发质量测试**和P930真libnx启动，再执行本轮**26项新WAV/强Switch main测试**、重编本轮真正SDK AArch64及物理SHA+129未解名字检查，避免“只引用旧结果就标记通过”。最终权威JSON：

`06_测试记录/P680_第151轮最终_原SDL异步WAV音效26宿主175原GPL2加1架构36Switch_127HD_SHA_1163.json`

最终以**P680实际PASS**判断回归结束。第152轮从**P680、原GPL2主剧情IPL225988/PC0x20E4D、175份原GPL2＋1GPL2架构适配＋36Switch和129真实未解**继续。优先将此前独立的真Vorbis诊断音频路径安全地集成到原WaveMaster及同一实际声卡，进一步为真正原25fps MPEG1/MP2影视引入经授权的原生解码源和全程音视频实测；同时处理NIR/GPU原中文字形与独立安全Save。仍然**`release_install_status=BLOCKED_NOT_SAFE_TO_INSTALL`**，不得发布或安装任何未经用户Switch实体机完成真实音画存档验收的NRO/NSP。

## 五、P933/P680最终整条历史门禁正式PASS

脚本`verify_p933_round151_final_originalWAV_full_HD127_1163_GPL2_36Switch.py`已**真正运行157.62秒**完成，`P680`权威状态：`PASS_P933_ROUND151_TRUE_ORIGINAL_BGI_WAV_ASYNC_SDL2_36_SWITCH_NATIVE_129_GAPS_HD127_QA1163_DEV_ONLY`。并不是引用上轮P678的旧质量记录：它从P931完整历史调用链重新运行**原PC 127份1280×960 CG、原OGG、原25fps MPEG1/MP2影片、字体、BP共39,772,982B逐SHA256全部一致**，重新执行**1,163项历史开发质量断言**，再次重编SDK平台、原GPL2 ARM64架构版Engine_Main和SDL2异步WAV音效源；本轮**20项真实WAV PCM与SDL设备/队列宿主测试＋6项安全Nintendo主入口原`orig`退出WAV清理宿主测试＝26条全部PASS**。

真正物理ELF64 ET_REL Machine183目标 `03_脚本工作区/P932_第151轮_真正SDL2原WAV一次性音效不占用原OGG混音/P932_175_Original_plus1GPL2adapted_36Switch_trueOriginalWAV_SDL2_AARCH64.o` **39,605,528字节**，SHA256=`a9a68275ae938ef0c4d2a33a3e28db17d34ddea80573caf625c771378d9e2714`，最新**129项**真实未解全局符号来自这一机器文件重新扫描，与上轮130项对比仅真实解决`OS_PlaySoundFile`一个，未引入任何新未解符号。源码统计准确为**175份未改GPL2上游、1份明确许可的ARM64 Engine_Main一行分支改版、36份不同Nintendo SD/SDL2音频/GPU/字形桥接**。未修改原商业高清资源、OGG/25fps电影和玩家Save，实体Switch DAC、原电影MPEG1/MP2实时解码及HD CG/NIR GPU逐帧显示依旧未验收。

**下轮唯一续接依据**`06_测试记录/P680_第151轮最终_原SDL异步WAV音效26宿主175原GPL2加1架构36Switch_127HD_SHA_1163.json`；下一步从原剧情IPL225988/PC0x20E4D、175原GPL2＋1 GPL2架构版＋36平台桥接、129项剩余真未解继续，优先整合早期经测试但仍属单独诊断程序的真实OGG/Vorbis音轨解码源和音频混音设备，随后认真解决MPEG1/MP2电影PTS同步，严禁空接口冒充成功或改变原画质音质。发行安全门禁仍`BLOCKED_NOT_SAFE_TO_INSTALL`。
