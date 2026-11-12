# 《素晴日》新版高清PC → NS移植：第169轮双编码与真实中文字形

日期：2026-10-23。工作区：`D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns`。

**第169轮已完成源码宿主与ARM64开发验收，尚未生成或验证可安装的NRO/NSP。** 原始PC音画和字体、原GPL2底稿、已有玩家Save只读保留，未修改、未复制受限字体/PC商业EXE到Switch发行包或公共仓。Switch运行/OS服务/字幕表现/存档持久化和授权仍需实机验收。

## 重要：本轮不是重新造Noto字体，继续利用项目里已有的真实代码

重连ShunCode后复核第167—168轮报告P698—P700均存在，前次旧报告所列NS字体基本接口已经在最新P961源码聚合里**确实定义**，并非还需要重做：

原BGI 7原生ABI：`OS_FontOpen`、`OS_FontClose`、`OS_FontFaceExists`、`OS_FontRender`、`OS_FontOpenMono`、`OS_FontRenderMono`、`OS_FontCharAdvance`。已有P523的`stb_truetype` MIT兼容C99光栅化器以SHA256保护的**OFL Noto Sans SC**真TTF读取、真实渲染中文/日文像素。SHA: `a3041811a78c361b1de50f953c805e0244951c21c5bd412f7232ef0d899af0da`，17,772,300字节，在开发者私有SD QA目录，不会嵌到ARM64 ELF。前述P909第143轮早已做过实编译，本轮没有把其成果误认成“尚未实现”。

**但这也不是原PC `SubahibiFont`的像素级视觉一致性证据**：原PC两种特殊TTF有游戏自定义字符映射；Noto字体仅证明可以绘字，不能未经映射校验拿它替代全部汉化字形/原画字体。

## 真实PC汉化可执行文件来源（只读）

原主篇`BGI-CHS.exe`、主篇修正补丁`BGI_patch.exe`、后日谈`BGI-CHS.exe`原字节都含GBK双字节编码的`素晴字体`；原版`BGI.exe`不含这一串。全部字节来自用户原PC游戏合集，仅做SHA计算与8字节姓名查找，不在发布包里保存Windows可执行文件。

| 原始用户文件 | 大小 | SHA256 | 用途 |
|---|---:|---|---|
| 主篇`BGI-CHS.exe` | 59,940,864 | `6eda794baf07d25092b640f8221ac93da810c144abd9f5d06832868187f97488` | 主篇汉化来源证明 |
| 主篇修正`BGI_patch.exe` | 59,940,864 | `f9f03e1ff648c5ea23facc0aa41a2c704e1978d534b9768c5ad879ae1da0d1e6` | 修订版本 |
| 后日谈`BGI-CHS.exe` | 363,315,200 | `ee7ae668a2bf0d97e21aa9d2fa3ab06759ab9ea51501527b55d936c77d4344cd` | 后日谈中文版本 |
| 日文原版`BGI.exe` | 1,216,512 | `f52f44c9a30cf061c286b6a16f4560802e307309c9610e08169f29ce9da94bf1` | 必须保持CP932、不能误识别为中文版 |

查出的是已知三份**本地文件的SHA/字符串**，不是所有其他PC中文补丁的通用规则，也没有由此证明整个脚本编码都可无条件改为GBK。

## P543/P965：所有21,791组真GBK源码映射+原CP932默认行为

复用第98轮之前存在的 `P542` Python标准库GBK权威码表生成的GPL2 C99转换器和`P546`派生的原`os_common.c`。本轮**重新编译并运行**真C99程序：

- `P543`：逐个遍历**21,791个有效原生GBK双字节→Unicode**及**21,791个Unicode→规范GBK反向**映射，检查无效`0x7F`尾字节、Emoji不可编码/问号、截断UTF-8以及 `素晴字体`原字节回转。PASS。
- `P965`：编译`P546`真实GPL2 `os_common`源码和五个`OS_SjisToCodePoint/SjisToUtf8/Utf8ToSjis/NativeToUtf8/Utf8ToNative` C99编码函数，**16项宿主检查PASS**。初始化仍是原CP932，`0x93FA`→日文“日”；**只有调用`P546_SetChineseLegacyMode(1)`后** `0xBABA`→“汉”，`0xD7D6`→“字”，并恢复为原CP932后继续能解日文。该开关并未凭汉化字体存在就自动开启。
- `P548`：本轮用以上真实源代码、已校验Noto真17.77MB字体及之前P523的7个原BGI接口重新编译Windows宿主程序，真正画出中文GBK“汉、字”和日文CP932“日”，分别核实非空不同灰度像素，单色1bit字图与笔画字宽，并在损坏SHA/错误长度时拒绝不可信字体。执行日志 PASS：`Chinese ink=98/112 Japanese=108`。

因此GBK汉化版本的双字节输入→Unicode→实际栅格字形，从源代码到宿主像素已连通；**不等于原PC所有汉字顺序、剧本文字或原SubahibiFont度量均已验证**。

## 真正安全的干净ARM64重链接，不重定义旧OS函数

从第166轮P958已验证的150原GPL2独立机器码前端重新组装，保留第165—166轮安全的`SaveWrite`有界注释与`OS_FileOpenRead`严格CAD字节长度；用前述GPL2-only P546 `os_common`替换旧上游那**一份**；在第一次NS OS层编译目标拼装阶段，以可选GBK/CP932双码页服务**替换**旧P905原CP932转换，而不是允许两个强符号；并加入完整21,791组GBK转换模块和第167轮原VM创建/删除目录、Horizon版本读取两模块。

为防使用过期AArch64编码对象，本轮已经把P546双编码os_common、五个原OS编码接口与P542完整GBK源码分别**重新执行真实Zig aarch64-freestanding-none C99编译**（三个新对象保存在P965目录），再干净重链接。原第167轮43Switch稳定基线P961**未覆盖**。

得到的P965隔离分支：**173份未修改原GPL2＋2份GPL2-only兼容源码派生（原SaveWrite安全和os_common双编码）＋1份GPL2 CPU架构适配＋44份Switch SDK/SDL2平台源适配＋MIT MPEG-1/MP2真实解码**。物理ELF64 AArch64 ET_REL真机器码，未解析全局符号仍**117个**，与上轮P961真实符号集合完全一致，无新缺口。

再新建`P966`版本许可门禁：仅对已明确核验的上述**3个主人PC汉化版exe SHA256**调用`P546_SetChineseLegacyMode(1)`，遇到原日文`BGI.exe`、未知SHA、长度错误、任何单bit SHA修改立即恢复CP932；**14项实际C99宿主检查通过**。只使用SHA摘要常量，不嵌受版权保护的原EXE；该函数已实际编译进45Switch AArch64新增源平台适配中，**未解析符号仍117个**，无新缺口。

**关键限制：P966来源门禁尚未连接到最终Switch游戏启动逻辑；发布包也没有原Windows EXE及其真实运行时散列输入。因此“源哈希确认、门禁已编译”不等于中文版游戏启动时已正确自动开启GBK。** 后续应以项目打包时真实PC来源校验生成受保护只读构建配置，先证实关联的`ipl._bp`游戏脚本确属该汉化版本再接入初始化。保持不同游戏版本的编码隔离。

第169轮最新源代码脚本：

- `01_工具脚本/verify_p965_round169_isolated_GBK_CP932_dual_source_rebuild_44Switch.py` — 173原GPL2/2派生/44原生平台AArch64干净重链接；
- `03_脚本工作区/P965_第169轮_双编码可选GBK模式与原CP932保真_安全存档HD影片44Switch_ARM64/p965_host_original_GPL2_GBK_PatchedCP932_user_selectable_dual_codepages.c` — 真C99双编码16项；
- `03_脚本工作区/P966_第169轮_实际主人PC汉化三变种_SHA256来源门禁_GBK有条件启用_AARCH64/p966_owner_PC_SHA_verified_BGI_CHS_GBK_mode_selector.c` — 原PC/后日谈SHA门禁14项；
- `01_工具脚本/verify_p967_round169_real_BGICHINESE_sha_GBK_dual_real_glyph_45Switch_AARCH64.py` — 全部结果重新编译/执行、物理ELF/SHA/117未解集合再核验。

结果记录：`06_测试记录/P701_第169轮_可选中文GBK原日文CP932双模式源码合并_44Switch_117未解.json`、`06_测试记录/P702_第169轮_真实主篇后日谈SHA门禁_GBK21791全验_汉字实笔画_45Switch_117缺口.json`。

最后实际AArch64文件：`03_脚本工作区/P966_第169轮_实际主人PC汉化三变种_SHA256来源门禁_GBK有条件启用_AARCH64/P966_173original2GPL2_derivatives_1arch_45Switch_owner_PC_GBK_provenance_HDMovie_AARCH64.o`。完整SHA、大小与117个仍需平台实现的真实符号名单均记录在P702。

## 必须后续完成

1. 把受校验的“主篇汉化/后日谈”来源配置绑定到Switch正式启动，防止原正版日文剧本和汉化GBK混杂；全文抽样验证原`ipl._bp`真实文字编码。保留原高清CG/电影/音质。
2. `SubahibiFont`主篇和`SimHei`后日谈自制字形映射并非通用Unicode字库；仍需验证实际汉字→字形索引、字距、栅格质量、与菜单文字及角色名字契合，不能只靠Noto作正式版权字体代替。
3. `OS_FontAddFile`、`OS_FontAddMemory`、`OS_FontEnumFaces`三个原BGI动态字体管理接口仍未接入；其他Windows专属安装、编辑器和显示控制及NS HOS startup/CRT仍有117个未解析。不能用假的空函数完成数字任务。
4. 完整Nintendo HOS SDK初始化、文件系统安全、原解析器/全部游戏流程/实机GPU、声卡、Joy-Con和QA存档掉电恢复/授权、重启与持续工作仍未实机验收。不得发行安装包。

旧历史127高清原媒体的SHA、1163旧开发断言未在本轮全部重新跑，不能混写成第169轮新通过的检查。原PC商业媒体、原用户Save及汉化字体**未被任何第169轮测试修改或重新分发**。

**发布状态：`BLOCKED_NOT_SAFE_TO_INSTALL`。**
