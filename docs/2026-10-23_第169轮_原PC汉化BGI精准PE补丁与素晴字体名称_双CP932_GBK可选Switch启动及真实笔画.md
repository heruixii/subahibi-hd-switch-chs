# 《素晴日》PC高清中文版 → NS，第169轮：原汉化EXE版本门禁＋CP932/GBK双编码＋真实字形

工程：`D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns`；日期：2026-10-23。

> **仍为仅供研究、移植开发的源码及ARM64部分链接目标，不是可运行、可直接安装的Nintendo Switch NRO/NSP。** 所有开发宿主测试PASS与交叉编译都不等于Switch真正启动、完整中文显示、正常存档、视频和声音实机通过。原PC商业资源/原EXE、全部旧母版音视频、用户存档未修改；不上传原字体或破解EXE到公开仓库。

## 原工作区恢复

ShunCode连接恢复后实检前一轮`P698/P699/P700`均存在；第167轮ARM64 174原GPL2+1安全存档衍生+1架构+43Switch真实旧目标的SHA固定，仍117个未解析符号。第168轮原字体3份、2个不同SHA，其中主篇与附件完全相同；主篇`SubahibiFont`有3912个Unicode直接cmap项、后日谈`SimHei`有3974项；3911共享，后日谈+63/-1。此处的“Unicode直接映射缺失中文”不证明原PC字形绝对缺少对应笔画，因为汉化补丁有专用字符集。

## P701：双文字模式实际编译为单独NS ARM64分支

已有旧项目源码P542/P546/P548/P909具备21,791个完整CP936 GBK双字节转Unicode和21,791个反向映射、从Python标准库生成的纯C99查表，以及完整OFL Noto Sans SC八位灰度/一位位图光栅器（`stb_truetype`，SHA钉住）。本轮不是重新发明字体或使用未经证实的SDL2_ttf包，而是**复用既有实际源码、重新编译并做干净替换**：

- 上游原`P902` os_common.c仅识别Shift-JIS lead，必须从新目标的源对象清单中去掉，干净替换成`p546_OpenBGI_GPL2_os_common_patched_Chinese_legacy_mode.c`，该源码在默认状态仍按CP932扫描，只有显式`P546_SetChineseLegacyMode(1)`才使用GBK（0x81—0xFE）字符起始。
- 上游原`P905`日文CP932专用三个主要转换接口在干净完整目标中移除，以新P546真实C99 `OS_SjisToCodePoint/OS_SjisToUtf8/OS_Utf8ToSjis`替换，同源同时保留安全的UTF8 SD文件路径转换；使用独立P544 21,791对完整GBK C99转换表，明确区分“中文字体原始字节”和NS私有SD路径UTF8。
- 同源Windows宿主真实**24项断言通过**：默认CP932`0x93FA → 日`、片假名单字节、切换GBK`0xBABA → 汉`、`0xD7D6 → 字`、`0xCBD8C7E7D7D6CCE5 → 素晴字体`、UTF-8直接字符、无效GBK、反向转码、日语模式恢复、SD路径保持原样。
- **43,582项完整C99正/反向GBK对照通过**（21,791+21,791），包括错误字节、Emoji不在GBK的处理等。以上属于编码转换证据，不能自动证明NS屏幕会正确画出3,900多个字形。
- 从安全P958已核的`149原GPL2+1有界存档衍生`与真正原上游其它对象重连，不链接两份`OsCommon/OS_Sjis`强符号。P960真实libnx目录、P961真实Horizon版本、P944 MPEG1影片、P942原MP2/S16抗混叠及OGG声轨全部保留。

**P701结果**：一个新的真正ELF64 AArch64 ET_REL，**173份未改GPL2 + 1份GPL2安全SaveWrite衍生 + 1份GPL2中文兼容os_common衍生 + 1份GPL2原架构适配 + 44份Switch平台适配及单独GBK表**。原有117个ARM64未解析全局符号完全未增加。该版本默认还是日文模式（安全）；未经版本确认不能自动打开GBK。第167轮旧主分支不覆盖。

新脚本：`01_工具脚本/verify_p965_round169_dual_CP932_GBK_gpl2_clean_175_source_45Switch_ARM64.py`（脚本文件名含历史工作名称“45Switch”，实际编译及报告认定为44份）。

新记录：`06_测试记录/P701_第169轮_24断言_CP932默认GBK可选_原21791对照_真实175GPL2_45Switch_ARM64隔离分支.json`。

## P702：真实主人PC汉化引擎版本，原PE仅5+22补丁特征和本地化字体名

只读读取用户原PC高清游戏根目录：

- `BGI.exe`：**1,216,512字节**，SHA256 `f52f44c9a30cf061c286b6a16f4560802e307309c9610e08169f29ce9da94bf1`。
- `BGI-CHS.exe`：**59,940,864字节**，SHA256 `6eda794baf07d25092b640f8221ac93da810c144abd9f5d06832868187f97488`。
- `BGI_patch.exe`：**59,940,864字节**，SHA256 `f9f03e1ff648c5ea23facc0aa41a2c704e1978d534b9768c5ad879ae1da0d1e6`。

对原PE的**同名/同RVA/同文件偏移/同长度**节逐字节对照（并非整个受保护EXE的简单比较）：`.text`两汉化文件都**恰有5字节不同**，`.rdata`都恰有**22字节不同**，`.data/.rsrc/.reloc`没有差异。两款60MB汉化EXE另有`.enigma1/.enigma2`封装段，包装数据不同很多，**绝不能说整个两个EXE只差27字节**。

进一步实际解出`BGI-CHS.exe`的`.rdata`两个固定八字节GBK字串，均为**“素晴字体”**（只是字符串，不传播EXE机器码）。主篇和后日谈`font.ttf`的SFNT名称表都各有Windows`platform=3, encoding=1, language=0x0804`记录，`nameID=1/4/6`显示**素晴字体**。这真实关联“PC汉化版请求字体的名称”和“原用户字体文件在简体中文环境下报告的Family”，比只查看英文字体Family`SubahibiFont/SimHei`准确。

**注意**：原字体只含3,912/3,974个Unicode直接cmap字码，常用“汉”等在直接Unicode映射中仍缺失；它可能通过GDI汉化专用字槽或其它重编码呈现。尚未逆推出主篇／后日谈的完整私有字形号和轮廓对应关系，不能以这项名称验证当作“所有汉字最终显示正确”。

没有运行用户原PC x86执行程序、没有解包或重写Enigma封装、没有把商业原EXE/字体复制到Switch工作目录之外的发行包。

脚本：`01_工具脚本/verify_p702_round169_original_owner_CHS_PE_5text_22rdata_font_localized_names_SHA.py`；报告：`P702_第169轮_原PC_BGI_CHS_执行段5字节字库22字节及两TTF真实中文本地字体名_SHA门禁.json`。

## P703：安全编译**中文版专用真正启动入口**，不是未调用的开关

从第151轮现有原P932 Nintendo启动源码制作GPL2隔离衍生P967，不改P932原文件：

1. 首先保留`P930_BootResourcesVerified()`、`P922_EnsureOwnerSourceSdReady()`和只读`ipl._bp`检查，所有失败按原返回码20/21/22结束；无私人SD来源不得开启游戏或更改字体编码。
2. 在成功通过以上检查、真正调用原`orig(1,safeArgs)`**之前**，仅当`P967_OWNER_VERIFIED_CHS`为构建宏才设置`P546_SetChineseLegacyMode(1)`；平常主分支保持CP932模式0。构建宏的专用脚本首先核对P702主PC汉化原EXE精准SHA、五/二十二字节补丁证据和简体中文字库名称。
3. 不改变原WAV清理`P932_ShutdownOriginalWave()`，拒绝伪造跳过资源启动前置检查。
4. **日文默认模式9项宿主断言**、**授权中文版9项宿主断言**均通过，检测失效时不会进入游戏；场景启动时显式GBK正确，能够调用原`orig`且只关原WAV一次。
5. 只把**新版中文入口一个C99对象**替换旧P932强`main`，从P958原150源对象、P546模式／转换、P960/961、原OGG/MP2电影适配全部重新LLD物理链接。没有`--allow-multiple-definition`，无覆盖旧主分支操作。

新版独立`P968`真正ARM64开发目标仍有**117个未解析符号**，和日文主分支集合逐个完全相同，满足“不为了中文模式破坏原游戏接口”的质量门禁。**主分支和中文分支都尚不是可直接安装的成品**。

代码：`03_脚本工作区/P967_第169轮_严格绑定原PC_CHS源SHA后可选GBK启动_不覆盖主工程/p967_owner_verified_originalCHS_optional_GBK_main_GPL2.c`

脚本：`01_工具脚本/verify_p968_round169_verified_owner_CHS_boot_original_VM_full_AARCH64.py`

报告：`06_测试记录/P703_第169轮_原PC_CHS_SHA显式启用_两套原机启动守卫_44Switch_ARM64_117未解.json`

## P704：真正七字体接口＋真实汉字／日文字形重新验证

已有的P523原BGI七字体接口改用**真实OFL Noto Sans SC 17,772,300字节**，原来源SHA256 `a3041811a78c361b1de50f953c805e0244951c21c5bd412f7232ef0d899af0da`（含初始化之前完整SHA检查，任何变长/变字节拒绝解析），透过`stb_truetype`真实渲染。此代码早在第143轮P659已合入过同源AArch64，并非这一轮重新发明。

本轮用P546中文原GBK模式复核`OS_FontOpen/OpenMono/Render/RenderMono/CharAdvance/Close/FaceExists`全部七个函数，真正渲染`GBK BABA → 汉`、`D7D6 → 字`和`CP932 93FA → 日`，获得独立非零灰度像素计数**98/112/108**，一位位图非零、字宽真实，从用户私人SD的SHA固定OFL字体来源加载；也测试错误SHA和错误长度安全拒绝。

最初在Windows宿主测试运行时由于**旧MinGW测试程序使用窄字符`fopen`无法正确解析混合中文的源目录路径**而失败，并非字体文件损坏。经源文件SHA和长度检查，旧私人SD路径中字体验证完全正确。为了测试Windows宿主，脚本仅在`D:\tmp`的临时英文目录**复制一份完全相同的私有OFL字体供当次宿主程序读取**，退出即清理，随后反向对照原始源文件和字体的SHA/mtime未变；不上传、嵌入或公开任何字体文件，用户原目录不改。

脚本：`01_工具脚本/verify_p969_round169_real_OFL_Noto_Chinese_GBK_JP_pixel_fixture_ascii_temp_cleanup.py`；报告：`P704_第169轮_原BGI七字体接口与GBK汉字日文字形灰度蒙版真实OFL_SHA_临时中文路径兼容修复.json`。

**该P704证明的只是Noto的真正字形光栅化、GBK/CP932切换无故障；不能替代原“素晴字体”完整字体的原样行距、笔画、背景和实机字形验证。**

## P705：统一独立验收和真正剩余阻塞

脚本：`01_工具脚本/verify_p970_round169_final_source_provenance_localized_font_CHS_arm64_dual_release_gate.py`，报告：`06_测试记录/P705_第169轮最终_原汉化PE精确字库映射_可选CHS真正启动_双码_真实字体_两AARCH64未解117安全闸.json`。

已独立核对P698旧主分支、P701双模式开发分支、P703中文版专用启动分支的**三份真实ELF64 ARM64机器码SHA和确切未解析符号集合**：均为117项，集合相等；P703仅用于已验证的私人汉化版本。P702原PC汉化EXE实际SHA、.text5/.rdata22及简体中文字库名，P704真实位图SHA、24项转换＋43,582完整GBK对照、日/中启动保护9+9均有证据。旧上游原文件、原高清音视频、玩家存档和NS发行包**均未改动**。

### 仍未完成，禁止伪报成品

1. **原商业“素晴字体”独特映射与字体度量**：原专有TTF直接Unicode CMap缺常见中文，虽然GBK文本解码和OFL Noto真笔画测试通过，但原汉化源码可能还使用特殊字形槽，不得凭Noto绘出几个字就说剧情文本全对。后日谈英文字体Family和主篇不同，不能直接互盖。
2. **原`OS_FontAddFile/OS_FontAddMemory/OS_FontEnumFaces`完整动态字库注册**等平台服务仍需安全实现，不能用虚假成功空函数凑链接数。原字体授权和用户目录要遵守。
3. **真正Nintendo SDK、所有剩余117个ABI、Horizon服务、CJK游戏画面、Joy-Con、原1280×960画面与44.1/48kHz音频混合、存档读写、整章剧情VM**都没有在Switch实机完成验收。当前是AArch64 ET_REL**部分链接**，不是已解决最终链接/启动。
4. 旧SDK和静态Vorbis来源隔离未独立验签，原版权媒体/字体不可公开再分发。保持用户已指定的质量与画质策略：不将1280×960原高清CG/影片降为800×600；不频繁打包无意义的测试包，不做病句检查或汉化润色，但安全、测试和文档必须保留。

**最新：第169轮真实双模式研发分支与中文版启动分支可重复构建，未解析符号仍117，安装/发布门禁 `BLOCKED_NOT_SAFE_TO_INSTALL`。**
