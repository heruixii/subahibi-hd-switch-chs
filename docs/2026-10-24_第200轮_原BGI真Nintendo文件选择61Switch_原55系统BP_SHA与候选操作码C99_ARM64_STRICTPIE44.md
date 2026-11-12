# 《素晴日》全高清PC版 → Nintendo Switch：第200轮

日期2026-10-24。接上第198轮**固定游戏入口GameOnly、60份真实Switch适配**以及第199轮的严格 `switch.ld -pie -z text` 最终未解析45项。

## 实际新功能：`80 3B` 原BGI文件选择对话框

原正版GPL2 OpenBGI `src/core/loadfile.c` 的 `FileDialog(path, desc, ext, title, initialDir, mode)` 实际调用 `OS_FileDialog(save,path,n,filter,defExt,initialDir,title)`，原OS.h的ABI与返回约定有源码可查。第200轮实际创建了独立的Nintendo适配：

`03_脚本工作区/P1073_第200轮_原BGI真正Swkbd_FileDialog仅主人QA故事文件_HOS_IPC只读61Switch/p1073_original_BGI_OS_FileDialog_Horizon_Swkbd_owner_story_file_READONLY.c`

真正调用已有P1037防重入Nintendo `swkbdCreate/Show/Close`；P546旧版GBK/日文源标题转换UTF8；Switch历史libnx的 `fsdevTranslatePath` 和 **`fsFsGetEntryType` 真文件存在性IPC**。输入文件只能属于 `sdmc:/switch/subahibi_pc_native_hd_qa/story/` 内严格ASCII安全的只读QA名字，禁止空、非法段、`..`、伪盘符、路径逃逸、超长路径及与 `defExt` 不符的扩展名。只有经真正Horizon确认 `FsDirEntryType_File` 后才回写原调用者输出；取消、无视频、未挂载SD、语言切换、目录/不存在文件均保持原有输出缓冲内容。**save=1严格拒绝**：该接口不是商用存档槽操作；另有经过实际源码回归测试的SaveWrite/SaveLoad开发QA设施。

当前仅是系统键盘输入路径的受限QA文件选择，并**不是**Windows通用带列表GUI文件浏览器；也没有实机验证Nintendo系统键盘UI/存储服务。

### 真实宿主、ARM64和最终PIE验收

- 原C99源码在Windows宿主经编译执行；仅模拟Horizon FS服务和Swkbd，文件选择实际映射到隔离ASCII主机目录的假测试文件，**323项断言通过**，系统软键盘创建/关闭 **26/26**，失败注入与字节保护通过。验证后移除了模拟BP文件，没有复制或改写用户原始私有BP。
- 原第60轮GameOnly 60平台适配干净机器码SHA固定，追加一份真正独立C99 Nintendo ABI源对象；完整AArch64 ELF64 ET_REL、`-u main --gc-sections` 均通过。
- 完整GameOnly适配未解析 **88→87**，GameMain **70→69**；严格Nintendo `switch.ld -pie -z text` 最终链接未解析 **45→44**，真实新增 `OS_FileDialog` 符号完全消失，**无新增未解析符号**。
- 前第194轮修正历史102项绝对重定位的RELRO节元数据只限独立QA机器码副本；真实严格PIE readonly `R_AARCH64_ABS64` 非法错误仍为 **0项**。这不是最终NRO链接成功：仍有44项未定义。

源码脚本与独立结果：

- `01_工具脚本/verify_p1076_round200_true_BGI_FileDialog_HOS_Swkbd_61Switch_STRICTPIE44.py`
- `01_工具脚本/verify_p1079_round200_FINAL_61Switch_STRICTPIE44_owner55BP_metadata_only_no_NRO.py`
- `06_测试记录/P758_第200轮_真正BGI_80_3B_FileDialog_NintendoSwkbd_HOS只读QA文件_323实测61Switch87_GC69_严苛PIE44.json`
- `06_测试记录/P760_第200轮最终_原BGI真HOS文件选择61Switch严格PIE44_主人55BP候选SHA只读_仍禁止安装.json`

## 真正主人IPL与54个系统BP：55份SHA确认与独立C99源审查

利用第94轮经过真实授权源码SHA验证的私有清单P276、真实GPL2 `ProgramHeader_t` 的偏移及长度，重新**逐份哈希全部55个原编译BP**，只在内存中读取并只对**真实代码段范围**做两字节家族候选扫描：`80 xx`、`81 xx`、`B0 xx`。第一层Python实现逐字节扫描；另一份完全独立C99程序以二进制标准输入接收原字节，不创建本地商业文件副本，同一份C源码既运行宿主，也编译成真实AArch64 ELF64对象。

共检查 **55个模块×31个子操作码＝1,705个独立比较**，所有代码段边界/候选数相等，原BP SHA无变化。断言额外包含一个内存中被破坏的BP头部超界必须拒绝、一个内存里 `80 3B` 字节扰动导致候选数减一；这两项都不会落盘原游戏内容。

从原55系统模块**代码区原始字节**找到 `80 3B` 共1组、`B0 11` 共2组。这说明原系统代码包含这些**候选二进制模式**；同时，部分安装器的家族字节模式数量为0。**严禁将0计数解读为完整剧情不可达证明**：这不是CPU/VM指令边界反汇编，某个出现次数可能来自操作数、代码内数据；现阶段未完整覆盖130章剧情脚本在系统运行后的动态加载、所有条件分支、原控制流，以及压缩解码的后续BP。不能因为静态扫描为0就删除GPL2 VM安装器、Child窗口、调试器函数，或用空函数假装平台已实现。

审查结果与逐文件透明清单：

- `01_工具脚本/verify_p1078_round200_real_owner55_BP_80_and_B0_OPCODE_BYTE_CANDIDATES_C99_ARM64_SHA.py`
- `02_清单与差异/P200_主人55原BP系统模块家族操作码候选_仅代码字节非可达性.csv`
- `06_测试记录/P759_第200轮_真实主人55份IPL和54系统BP SHA逐一核验_80及B0家族候选字节_C99双核扫描_不宣称VM不可达.json`

## 第201轮接续优先工作

1. 继续真实检索剩余44项：部分安装器/外部进程与主线作品是否**实际可执行**尚需全场景BP字节码、控制流及动态模块证据，未证明则不从GPL2全局VM中移除。
2. 负责原GPU/Mesa部分真正解决 `nir_shader_clone` 未定义：历史libEGL归档未提供该C定义；必须找同版本NIR真实实现及依赖，或验证可替代的正版Switch图形后端，不能伪造shader或禁用HD渲染。
3. 原BGI八套B0 Child真实子画布仍需要SDL图形目标、事件绘制和销毁一致的GPU方案；不加假 `OS_Child*`。
4. 所有本作主篇/后日谈仍以**1280×960原CG、原25fps MPEG1/MP2音源、原OGG与原私有中文字体、原剧情和存档**为不可改动质量基线，不频繁组装无意义测试包。

**最终状态：`BLOCKED_NOT_SAFE_TO_INSTALL`。有61份AArch64原生适配的完整/主入口部分链接对象，但严格PIE未解决全部44项，未验证历史SDK来源签名，未生成可实际安装的游戏NRO/NSP，更无NS真机硬件运行验收。**
