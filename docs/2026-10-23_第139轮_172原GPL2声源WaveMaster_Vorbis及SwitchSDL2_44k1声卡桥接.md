# 《素晴日》新版 Nintendo Switch 高清移植｜第139轮

2026-10-23。真实工程：`D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns`。

第139轮从第138轮**原GPL2 C99 161份＋12个Switch SDL2/libnx/SD/EGL/GLES/CRT原生桥接＋255个局部真实链接未解符号**继续。本轮重点不是修更多宿主指令轮转，而是**实际把原 GPL2 WaveMaster背景音乐、SE、语音混音、BitWave PCM/ADPCM/Vorbis流处理接入原生 ARM64 构件，并接上符合原 `inc/bgi/os.h` 声音拉取回调签名的真实SDL2设备输出源码**。PC游戏原素材、OGG音频和玩家Save始终只读，保留原1280×960高清CG和高质量声音，不转成旧版800×600。

## 一、11份原版 GPL2 WaveMaster / BitWave / Vorbis 源码真实ARM64机器码（P893/P643）

本轮从**未改动、只读的原GPL2目录**`07_工具链环境/P419_OpenBGI_最新GPL2_隔离只读参考_未执行未链接游戏/source`精确编译以下11份C99：

| 子模块 | GPL2原源码 |
|---|---|
| 音乐系统 | `src/snd/wm/wavemaster.c`, `bgm.c`, `se.c`, `voice.c`, `record.c` |
| 音频流与解码 | `src/snd/bw/source.c`, `stream.c`, `pcm.c`, `vorbis.c`, `adpcm.c`, `huffman.c` |

每份保持原源码SHA，使用本项目真实隔离 Zig C99→AArch64 编译器产生 **ELF64 ET_REL Machine183**，实际与此前161份原GPL2引擎源码、12份已存在的Switch原生SDL2/SD/EGL适配和真正Switch SDK静态库一起执行`ld.lld -m aarch64elf -r`。新增11份原GPL2源码与既有符号没有重复定义，**原引擎累计172个不同C99原源码ARM64目标**。之前局部未解析的**28项`Wm_*`原WaveMaster接口全部由真正原GPL2源码解决**（含背景音乐、循环、SE、渐入渐出、声音流、计时器）；音频源码在此阶段又引入底层**`OS_AudioStart`与`OS_AudioStop`两项新需求**，所以该阶段的255项未解精确变成**229项**，不是最终完整NS接口数量。

原GPL2音频混音器真实软件实现已有ARM64机器码，但还没有证据表明任天堂扬声器实际收到声音或电影已经音画同步。脚本 `01_工具脚本/verify_p893_round139_original_11_GPL2_WaveMaster_Vorbis_native_ARM64.py`，权威源SHA、11份机码SHA及**229项**真实未解符号清单见 `06_测试记录/P643_第139轮_11份原GPL2真实WaveMaster_BGM_SE_Vorbis声音ARM64编译链接28原接口.json`，机器码产物位于 `03_脚本工作区/P893_第139轮_原GPL2真实WaveMaster_BitWaveVORBIS声音实现ARM64/`。

## 二、真正的Switch SDL2立体声44100Hz PCM拉取设备桥接（P894/P644）

单独新增原生Switch源码 `03_脚本工作区/P894_第139轮_真实SwitchSDL2_44k1PCM混音音频输出OS桥接/p894_switch_sdl2_audio_out.c`，严格按原 `inc/bgi/os.h`：

- `OS_AudioAvailable`：检查SDL2音频子系统初始化结果和**真实枚举设备**，失败时正确返回无设备，不虚报存在扬声器。
- `OS_AudioStart(int rate, OsAudioFill_t fill, void* user)`：使用真正SDL2 `SDL_OpenAudioDevice`请求**传入的完整采样率（原混音器44,100Hz）、S16本机端序、双声道交织**，严格验证SDL2返回格式，拒绝降采样/改格式；设备启动后原混音器提供的同一`fill(user,int16_t*,frames)`回调从SDL音频线程拉取音频。
- `OS_AudioStop`：真实暂停并关闭SDL2设备、等候回调结束、清理本适配层启动的音频子系统。重复关闭不重复操作，也不会改玩家Save。

SDL2设备函数的**同一份C99实现**在Windows主机被真实编译并调用，模拟的是SDL回调的设备交互数据（不是Switch扬声器），验证44100Hz S16双声道规格、4帧16位立体声测试采样值、格式不匹配时拒绝、错误初始化/无设备、重复打开/关闭安全、音频线程拉取数据等。与此同时，它被真实交叉编译为**12,432字节 ARM64 Machine183 ELF64**，使用原Switch SDK `libSDL2.a`与上面的**172份真实原GPL2源码＋13个独立原生Switch对象**完成LLVM部分链接，底层 `OS_AudioAvailable/Start/Stop`三项真正有本平台机器码。第139轮声音此时已**无`Wm_*`缺失，也无`OS_AudioStart/Stop`缺失**；该阶段剩**226项**其他真实链接未解。

脚本 `01_工具脚本/verify_p894_round139_true_Switch_SDL2_PCM_44100_audio_device_arm64.py`；宿主测试 `p894_host_sdl2_audio_device_fixture.c`、机器码ELF和运行日志位于 `03_脚本工作区/P894_*`；权威验证 JSON `06_测试记录/P644_第139轮_SwitchSDL2真实44k1立体声PCM回调设备3原OS音频接口机器码与宿主测试.json`。

**边界：** 设备及SDL函数实际上在*宿主测试中以确定性fixture被调用*，ARM64只通过机器码编译及LLVM静态链接验证；没在实体Nintendo Switch启动音频设备、无实体扬声器的BGM、SE或实际OGG音乐与25fps电影同步测试。测试成功**不等于可以安装游戏**。

## 三、Switch没有Windows MCI光驱：按原GPL2合同正确报告不可用（P895/P645）

原GPL2 `inc/bgi/os.h`明确写有：**不支持CD-audio的系统，MCI操作均返回0表示失败**。Switch无Windows MCI光驱，本轮使用不制造虚假CD硬件的明确平台适配实现：`OS_MciOpenCdAudio/SetTimeFormatTmsf/Close/Status/Play/Stop`。此处报告失败是**原GPL2已规定的真实平台语义**，绝不把Windows MCI不支持误写成NS能播放CD，也绝不让它覆盖真正的SDL2 PCM/OGG音乐播放。

同一份C99源经主机实际执行**8条反例测试**，并交叉编译ARM64对象以真实LLD解析6种现存OS MCI缺失接口，无新传递依赖。本轮当前累计**172份原GPL2原生C99机器码＋14份真实Switch原生适配＋真实SDL2/libnx/EGL/GLES/CRT SDK静态归档**，最新真实LLVM部分链接机器码 **37,634,640字节**，局部未解析从226降为**220项**。脚本：`01_工具脚本/verify_p895_round139_switch_no_cd_MCI_documented_failure_native.py`；JSON `06_测试记录/P645_第139轮_6项原GPL2明确无CD音频硬件MCI失败接口ARM64真链接及8主机检查.json`，真实ARM64对象/原源码SHA/220项剩余符号清单在`03_脚本工作区/P895_*`。

## 四、本轮完整高清质量门禁和续接点

最终统一验证脚本：`01_工具脚本/verify_p896_round139_final_172_real_GPL2_WaveMaster_14Switch_PCM_HD127_1163.py`。它在原已有的PC高清校验、原GPL2真实生产线程验证和完整Switch SDK C99/ELF链接基础上，重新执行新增的真实WaveMaster／Vorbis源码编译、真实SDL2音频后端和无MCI平台合同校验。完整权威最终 JSON：`06_测试记录/P646_第139轮最终_172原GPL2声音源码14Switch真PCM链接127HD_SHA_1163.json`。

历史高清质量要求：原PC **127份PNG/OGG/电影/字体/BP相关高清资源共39,772,982字节，逐SHA256一致**；**1,163项历史开发断言**再次实际回归PASS；新版CG、原OGG及电影、原BP、玩家Save均不得降级或修改。原故事主线程IPL仍在**225988／PC=0x20E4D**；子线程原GPL2源码生产Vm_RunPass的安全测试保留，**这些主机隔离音频设备验证不能冒充NS实机体验**。

**第140轮真正优先级：** 以本轮**P646最新172原GPL2＋14Switch SDK源码，220个局部真实未解符号**及P628八个私有BP真实线程现场为准，重点让原GPL2生产`Vm_FrameServices`的窗口渲染、音频/影片、Joy-Con触摸、Save真正经libnx/SDL2进入可在Switch持续运行的调度循环；逐步完善GPU/NIR、窗口消息和音视频同步，谨慎收口最终NRO/NSP。确认真实Switch上全CG1280×960、OGG 44.1k音质和保存稳定性后才可发行；当前严格`BLOCKED_NOT_SAFE_TO_INSTALL`。
