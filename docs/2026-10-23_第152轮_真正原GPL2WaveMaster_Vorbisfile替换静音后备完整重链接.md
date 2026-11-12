# 《素晴日》新版PC高清Nintendo Switch移植｜第152轮原GPL2声音引擎Vorbis恢复

日期：2026-10-23。路径：`D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns`。

## 1. 权威基线与意外发现的真实静音缺口

第151轮权威`P680`：**175份GPL-2.0-only未改上游C99＋1份明确保留GPL2的Switch ARM64 Engine_Main一行宏条件适配＋36份互异Nintendo SDK/libnx/SDL2/安全SD/GPU/声音适配对象**，真正AArch64 ELF64 ET_REL **39,605,528B**，SHA `a9a68275ae938ef0c4d2a33a3e28db17d34ddea80573caf625c771378d9e2714`，未解真实129个全局符号。上轮的真正`OS_PlaySoundFile`只修复原Windows风格的一次性异步WAV音效，不能代替OGG/Vorbis的BGM和配音。

直接阅读**未经修改**的上游GPL2 `src/snd/bw/vorbis.c`发现：该文件默认在没有`BGI_HAVE_VORBISFILE`和`BGI_USE_STB_VORBIS`宏时编译进一个**返回规定长度全零PCM**的静音后备分支，即使原上游WaveMaster/BGM/SE/声音设备整个对象已经物理链接，实际Vorbis codec 3也可能只输出静音！上轮P680真实AArch64机器码中确实没有任何`ov_open_callbacks/ov_read/ov_pcm_seek/ov_clear`机器符号，因此本轮优先修复这个真正的声音阻塞，而不是写一套与原故事引擎毫无关系的孤立OGG播放器。

## 2. P934/P681：从加入WaveMaster之前的真实源码基线整套重链接

**原GPL2源码原文件一字不动，未把旧商业OGG重编码或转成降低音质的WAV。** 第152轮从`P890`**161份真实GPL2上游机器模块＋12份Switch已有SDL2平台对象**的基线重新构建，而不是直接把新`Vorbis_Open`叠加到已经定义了同名旧静音函数的P680大ELF造成符号冲突。

上游原`src/snd/bw/bw_internal.h`的`struct WmStream`在`BGI_HAVE_VORBISFILE`条件下包含`OggVorbis_File`成员，而默认静音版的结构大小不同。故不是只重新编译一个`vorbis.c`，而是**所有六份会包含BW内部结构的源：`bw/source.c`、`stream.c`、`pcm.c`、`vorbis.c`、`adpcm.c`、`huffman.c`，统一以`-DBGI_HAVE_VORBISFILE`真实AArch64编译**，同时重编上游5份未改WaveMaster/BGM/SE/Voice/Record声音源码。合计**11份原封不动的GPL2 C99声音源码**，真实导入`ov_open_callbacks`、`ov_read`、`ov_pcm_seek`、`ov_clear`，保留原64字节BW包装头后面的内嵌`OggS`数据起始、双配对音乐源、原sample frame seek和PCM增益逻辑。该宏禁用旧的以`memset(buf,0,n)`强制假造静音的后备源码分支。

再加入一份未改原`src/os/os_common.c`、上轮原GPL2的`main.c`/`hvl.c`及独立GPL2许可的ARM64 Engine_Main改版，以及所有12个中途已验证的Switch HD/GPU/PCM/文字/SDL2机器码阶段与其后12个Switch平台适配（含安全SD、真实libnx `userAppInit/Exit`、SDL WAV音效和安全`orig`主入口），获得**175份未修改GPL2 C99＋1份明确修改一行的GPL2 ARM64源码＋36份Switch原生适配**总结构。原上游源码数量没有因为重编而增加；机器源码路径结构在本轮全部重新枚举验证。

用于真正Vorbisfile ABI的三份**存在于原工程早期隔离数据区的ARM64静态库**：

`07_工具链环境/2026-10-19_原始OGG音轨Switch音频SDK历史包隔离来源未验签/data_only_staged_portlibs_ogg_vorbis/lib/libvorbisfile.a`

同区`libvorbis.a`和`libogg.a`。这三份是在历史阶段保留的**隔离未独立验签、来源仍需进一步核对**的ARM64纯数据`.a`库，只由现有可信编译/链接工具读取，没有执行其中的EXE、安装器或脚本。**虽然真正源码静态库已被链接，不能推论已完成安全发行供应链验收。**

真实SDK LLVM `ld.lld -m aarch64elf -r`产物：

`03_脚本工作区/P934_第152轮_真实原GPL2WaveMaster_Vorbisfile解码替代静音后端/P934_RealGPL2_BitWave_VorbisFile_175Original_1EngineAdapted_36Switch_AARCH64.o`

**39,939,112字节**，SHA256=`f8bc23fb1c272015d9d61da3fdbddebf7b6d3c71e31a27fd4d2cc5a59524f5e3`，AArch64 ELF64 ET_REL Machine183；实际`ov_open_callbacks`、`ov_read`、`ov_pcm_seek`、`ov_clear`与上游原`Vorbis_Decode/WmStream_Decode/OS_AudioStart/OS_PlaySoundFile`机器码均真实定义。132? **正确沿用P680的129项真实未解符号，集合与上一轮129完全一致，零新增符号**。原MPEG影片、GPU/NIR等未解决的缺口保持真实记录，不能伪装已可播。此阶段证据：`06_测试记录/P681_第152轮_真实原GPL2_WaveMasterVorbisfile动态PCM替换静音_11原模块39MBARM64.json`；执行脚本`01_工具脚本/verify_p934_round152_real_original_GPL2_WaveMaster_Vorbisfile_non_silence_ARM64.py`。

## 3. 原GPL2非静音PCM测试的准确边界

实际同一份**上游原GPL2**`vorbis.c`以`BGI_HAVE_VORBISFILE`宿主编译并执行原`Vorbis_Open/Decode/ReadBytes/SeekFrame/Close`，通过20项检查：原0x40 BW头后的`OggS`读取、`ov_*`函数位置/返回语义、4帧双声道非零PCM按原字节复制、解码后帧数、末尾无补零、seek、拒绝打开、解码故障返回0、资源释放和重复关闭。**宿主程序中的`ov_*`由受控mock应答，这项测试只说明原GPL2解码调用/音频缓冲处理和失败条件真实经过验证，不说明用真实Vorbisfile算法完成过Switch平台原OGG解码**。实际libvorbisfile源码机器码存在于AArch64 ET_REL中，不等于物理Switch扬声器成功播放，也不证明不同硬件音频混音设备可同时使用。

需要实机验证的内容仍包括：原游戏`*.bw`封装的codec 3结构和真实原Vorbis码流逐帧解码准确性、配音/BGM与SDL2音效设备实际同时输出、DSP/44.1kHz混音、原25fps MPEG1/MP2声音同步，以及高清CG和中文字形GPU呈现。**无实机音画/存档已验收的可安装完整游戏NRO/NSP。**

## 4. 全量历史质量门禁与续接

第152轮最终整链脚本：`01_工具脚本/verify_p935_round152_final_GPL2_realVorbis_no_silence_HD127_1163.py`，真实从上一轮`P933/P680`历史链重新执行**127份PC原1280×960高清CG/OGG/25fps电影/字体/BP合计39,772,982B SHA256逐文件检查与1163条历史开发断言**，再重新编译11份上游GPL2真Vorbisfile声音机器码并执行20项宿主回调/错误测试、校验三份历史第三方库SHA及LLVM AArch64真实机器码、129项真实未解集合。

权威最终`06_测试记录/P682_第152轮最终_175原GPL2原BW真VorbisPCM加1架构适配36Switch_127HD_SHA_1163.json`——**该文件真实产生并PASS才是整轮完成的唯一依据**。下一轮从原剧情IPL **225988**／PC **0x20E4D**、**175原GPL2＋1许可GPL2架构改版＋36Switch、129个未解外部函数**继续。最高优先先补第三方音频库独立来源审查和实际原OGG/BitWave码流解码验证，再做统一SDL声卡协同及真正MPEG1/MP2影片40ms PTS同步、1280×960高清CG GPU/CJK、Joy-Con与独立安全Save；严禁降低画质音质或篡改原母版/玩家存档。GPL-2.0-only、OFL与游戏商业素材需各守其许可。`release_install_status=BLOCKED_NOT_SAFE_TO_INSTALL`。

## 5. P935/P682最终质量验证完成，保留准确的历史回归过程

**最终权威`P682`已真实生成且状态PASS：**`PASS_P935_ROUND152_TRUE_GPL2_BW_VORBISFILE_NON_SILENCE_36_SWITCH_HD127_1163_DEV_ONLY`。本轮第一次完整P935调用**确实物理重跑了上轮全历史P933/P680的127份原PC高清CG/OGG/25fps电影/字体/BP逐SHA256全相同与1163条质量断言，以及本轮P934/P681原GPL2 Vorbis C99重新编译、20条宿主非零PCM/回调/失败测试和真ARM64+libvorbisfile三个静态库链接**，随后在最终P935 JSON核验代码遇到一个仅Python报告层的`check`应为`ck`的拼写错误，源代码与机器产物并无问题。修复报告拼写后用`--reuse-fresh-round-checkpoints`严格要求**同轮P680/P681刚于10分钟内生成、全部PASS且完整检查SHA和ELF未修改**，只复用这次刚物理执行过的全历史回归，不再徒增几分钟重复大编译；P682如实标注`full_current_invocation_reexecuted_original_HD127_SHA_and_1163_QA=false`与`full_HD127_SHA_and_1163_quality_reexecuted_during_this_round_with_recent_P680_P681_checkpoints=true`，避免虚报第二次短核验再次做了全部测试。

最终机器仍是**39,939,112字节 AArch64 Machine183 ELF64 ET_REL**、SHA256=`f8bc23fb1c272015d9d61da3fdbddebf7b6d3c71e31a27fd4d2cc5a59524f5e3`，原GPL2已有的175原封不动源码＋1 GPL2许可架构版和36份真实Nintendo原生平台对象同链；**129项真实未解符号**严格保持，无任何新引入；原新版HD媒体合计39,772,982B和玩家Save零修改。第三方静态Vorbis库的签名仍未独立核验，20条宿主是模拟`ov_*`的原GPL2调用验证，**均不是实机Vorbis已经可听见**。发行/安装门禁继续**`BLOCKED_NOT_SAFE_TO_INSTALL`**。
