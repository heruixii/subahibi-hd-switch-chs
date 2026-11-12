# 《素晴日》新版PC高清移植 Switch｜第154轮：原GPL2 BitWave + 真 Xiph Vorbisfile 声音闭环

日期：2026-10-23。工作区：`D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns`。

## 原有基线、动机

上一轮 `P683` 已对17份真实PC高解析音频ARC中**32,993条**BitWave容器、codec 3 `OggS`音轨完成原文件只读普查，同时使用电脑端FFmpeg对9条原声抽样实际解码；然而第152轮 `P934` 真GPL2宿主程序的 `ov_*` 回调为模拟，无法保证上游原`vorbis.c`在真实Vorbis库调用时能正确读出音频。本轮正式消除这个测试缺口，不修改原上游源码、游戏母版或存档。

## 可信宿主解码库的隔离编译

只在 `07_工具链环境/P937_第154轮_Xiph官方SHA隔离源码_仅宿主测试` 下载和展开Xiph公开源码：`libogg 1.3.6`、`libvorbis 1.3.7`。下载后**先严格比对发布方完整SHA256才解包**，值分别为：

- `libogg-1.3.6.tar.gz` = `83e6704730683d004d20e21b8f7f55dcb3383cdf84c0daedf30bde175f774638`
- `libvorbis-1.3.7.tar.gz` = `0e982409a9c3fc82ee06e08205b1355e5c6aa4c36bca58146ef399621b0ce5ab`

核验后以当前可信 `C:\msys64\mingw64\bin\gcc.exe/ar.exe` 直接**逐份编译C源，未运行下载包中的安装器/构建脚本**，产生 Windows x64 宿主静态库 `libogg_host.a`、`libvorbis_host.a`、`libvorbisfile_host.a`。隔离目录不覆盖先前未独立验签的**Nintendo AArch64音频库**，两者不得混用或冒充已经交叉验证的相同二进制。

把 `P419` 早期隔离参考里的六份**与第152轮ARM64编译使用源SHA完全一致且未经改动的GPL-2.0-only**文件 `bw/source.c`、`stream.c`、`pcm.c`、`vorbis.c`、`adpcm.c`、`huffman.c` 以 `BGI_HAVE_VORBISFILE` 统一宏重编译，与上面的真Xiph库直接物理链接。该宿主有实际定义的 `ov_open_callbacks/ov_read/ov_pcm_seek/ov_clear`、`Vorbis_Decode`、`WmStream_Open/Decode/Restart`，**没有mock或自行伪造ov实现**。为了不碰PC路径，宿主只从标准输入获得原BW二进制并在内存转为 `WmSource_FromMemory`；输出PCM也通过标准输出返回测试进程，没有另存商业音频。宿主 OS 文件读写入口显式拒绝。

## 实际P937开发验收

稳定可复现脚本：`01_工具脚本/verify_p937_round154_real_GPL2_Xiph_vorbisfile_host_original_BW_9PCM.py`。

最终权威JSON：`06_测试记录/P684_第154轮_原GPL2真libvorbisfile九原BW音轨宿主全链解码_循环异常_SHA.json`，状态 `PASS_P937_ROUND154_REAL_UNMODIFIED_GPL2_6BW_XIPH_OGG_VORBISFILE_REAL_PCM_9_TRACKS_HOST_ONLY`。

真实游戏声音与独立FFmpeg PCM交叉验证：

| ARC原始条目 | 原格式 | GPL2实际宿主解码范围 | 与FFmpeg逐样本最大误差 |
|---|---|---|---|
| `yuki_000001` | 44.1kHz双声道 | 完整76,550帧 | 1 LSB |
| `yuki_000002` | 44.1kHz双声道 | 完整379,553帧 | 1 LSB |
| `yuki_000002_a` | 44.1kHz双声道 | 完整143,388帧 | 1 LSB |
| `yuki_000012` | 44.1kHz双声道 | 完整60,078帧 | 1 LSB |
| `bgm001`、`bgm002` | 44.1kHz双声道 | 每首17,640帧（各0.4秒首段） | 均1 LSB |
| `se904` | 22.05kHz单声道 | 完整66,056帧 | 1 LSB |
| `se937` | 48kHz双声道 | 96,000帧（2秒首段） | 1 LSB |
| `se_zakuro2` | 44.1kHz单声道 | 88,200帧（2秒首段） | 1 LSB |

共**9个原商品音轨全部实际由OpenBGI原BitWave代码+真Xiph解码产生非零PCM**；校对首段和整段样本帧数、声道、频率，最大误差只有1个16位PCM数值单位（两种合规Vorbis解码浮点舍入可有该微差），**源Ogg/BW压缩字节没有任何转换或修改**。

此外，九条源都调用真实原`WmStream_Rewind`/`ov_pcm_seek`并与源头PCM首段**字节完全一致**；`bgm001` 的真实 `WmStream_Restart`、loopStart=0以及Vorbisfile frame seek，得到的4096帧与原首段**逐字节完全一致**。四种独立内存畸形输入（BW magic、截断头、不存在的codec、OggS signature）由原GPL2解析/实际Vorbis解码器真实拒绝，未产生输出。注意原BGI并不保证拒绝所有人为损坏的BW字段，不能把这四种情况外推为完整恶意输入模糊测试。

本轮没有再次重跑上轮1163条全历史门禁/127PC高清媒体文件SHA；它们仍以第152轮真实PASS基线为准。额外复验第152轮AArch64机器对象SHA不变（`f8bc23fb1c272015d9d61da3fdbddebf7b6d3c71e31a27fd4d2cc5a59524f5e3`），九条原BW独立SHA与第153轮一致，所有此次使用的原PC声音归档大小和mtime不变。保存所有宿主三库与EXE SHA用于后续追踪。

## 实机与安装门禁、下一接续点

**本轮是 Windows宿主的真实 GPL2 声音引擎验证，不是 Switch 实机发声。** 第152轮175原GPL2+1架构改版+36Switch的真实AArch64部分链接文件仍有**129个未解全局符号**；未独立核验历史第三方Switch ARM64静态库来源/签名；原SDL2混音设备、双路BGM+异步WAV交织输出、实机Joy-Con、1280×960高清CG/CJK GPU、游戏本体全路径运行、存档安全、25fps MPEG1/MP2音画同步仍在待证项。

下一轮优先分析原GPL2 `Wm_MixRunning`、`Mixer_Fill`、`OS_AudioStart` 与外部WAV声卡相互持有的设备竞争，添加独立不修改原PC声音的模拟设备并发测试，然后消减129个符号中真正影响主线的调用；确保5部原25fps影片音画同步、高清显示和文本Save安全。不急于生成一个会黑屏/无声的所谓成品安装包。

**最终状态：`BLOCKED_NOT_SAFE_TO_INSTALL`。** 上游OpenBGI为GPL-2.0-only；Xiph源码附BSD风格许可证，游戏商业语音/图片/电影继续保留原素材所有权，不混入公开源代码发行。
