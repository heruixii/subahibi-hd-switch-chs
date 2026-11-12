# 第七十三轮｜原高清＋OGG＋按键检验原 BGI/BP 的真正 AArch64 NRO（非完整游戏）

日期：2026-10-19。项目根目录：D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns

## 本轮实现

在第72轮原130段BGI编译场景与9份原BP系统字节码、276注册handler全量静态匹配的基础上，本轮不再只有孤立ARM64对象，而是将源码加入原有真原生1280×960 PNG、44.1kHz OGG/Vorbis逐帧不阻塞SDL2音画诊断程序，新建真正AArch64 ELF和libnx MOD0格式NRO。保留原P259、原P261 NRO源码与二进制，不覆盖旧QA，更不改用户安装游戏和Save。

新增C99位于：
03_脚本工作区/P300_原高清OGG加BGI_BP只读SD探针_非剧情游戏

- 另建HD+Vorbis主函数源码，只有按键P（键盘）或手柄A才执行Bgi/BP源验证；日常高清/原OGG渲染完全不尝试打开剧情；
- 生产NRO端只能读取固定sdmc:/switch/subahibi_pc_native_hd_qa/story目录下10个文件：九份原系统BP编译模块、原第一段BGI场景data01000/yuzu_2g；
- 源文件有各自从真正原PC原P3源SHA账本生成的SHA256和精确大小，最多单文件8 MiB，仅读一次到内存后**对实际用于解析的这一份内存字节**SHA256验证，规避了先哈希文件再重新打开之间可能替换内容的问题；
- 真正全部9BP源经C99原BP指令格式、3142个真实控制流目标验证框架及276个原BP函数入口边界检查；一个原yuzu_2g剧情经真实C99全层入口检查，940条编译剧情指令、20次外部函数引用、9种处理器；
- 未实装或不可信的原BP VM调用一律拒绝，所有这些是解析、SHA与handler查表，真实原游戏VM及系统BP VM**执行次数为0**，不能直接显示剧情、选择支、动漫字体，也不接触游戏Title的存档；
- 缺失BP/剧情或被篡改资源时，诊断通过日志、窗口标题提示失败，原高清/OGG实验独立继续运行，不进入游戏或假降级模式。

源码生成器与目标编译：
01_工具脚本/p297_generate_source_pinned_optional_SD_BGI_BP_probe_C99.py
01_工具脚本/p299_link_true_ARM64_SDL2_HD_Vorbis_with_BGI_BP_readonly_SD_user_probe.py

新QA NRO：
05_NS测试构建/P300_真ARM64高清原OGG_BGI_BP按键只读探针NRO_严禁标为完整游戏/subahibi_HD_OGG_BGI_BP_private_QA_NOT_HW_TESTED.nro

这是真实AARCH64/ELF64，SDL2/libnx/Vorbis/原BP C99均参与同一目标链接。NRO由官方switchbrew elf2nro源码在本机编译的转换器与独立Python算法两路完成，产物完全相同；实际MOD0、NRO0、HOMEBREW、LNY ABI头均已解析确认。历史SDK静态库仍属隔离且真机兼容尚未验收，NRO不含商业原素材或ROMFS。**Switch设备真实hbmenu/GPU/DAC尚未测试，因此非发行安装包。**

双重NRO验证：
01_工具脚本/verify_p301_true_ARM64_HD_Vorbis_BGI_BP_manual_SHA_source_probe_official_NRO.py
06_测试记录/P106_真实Switch_ARM64原高清44100OGG与BGI_BP按键SHA只读桥单NRO0_官方C和Python双一致非游戏.json

## P302 Host渲染和原编译源故障测试

新隔离SDL+Vorbis主机模拟器重新编译与上述ARM64同源的所有C99组件，不修改旧模拟代码。
- 无按键，1280×960模拟GPU连续4帧、零BP读取；
- 用户按P、手柄A：BP源不存在应拒绝但GPU继续各4帧，窗口显示错误且不崩溃；
- 原PC九BP+一个yuzu_2g原编译场景均必须SHA验证并找到全部276系统入口；
- 14个临时坏输入（九份BP每份同尺寸单字节篡改、一段剧情同尺寸单字节篡改、缺失根目录、单BP丢失、单字节截短、超长非法路径）全部严格拒绝，私有临时测试副本自动删除。

P302脚本：
01_工具脚本/verify_p302_HD_OGG_BGI_BP_source_SHA_memory_host_button_and_14_bad_sources.py
报告：
06_测试记录/P107_真高清OGG与原BGI_BP按键只读SD探针_主机渲染持续和10原文件_SHA内存校验14负例.json

## P303 完全私有25文件SD测试目录，严禁公开发行

已于D盘独立隔离暂存完整的个人源文件布局（不修改此前P263媒体QA目录），包含13张真PC高清PNG、1条原OGG音轨、9份原BP编译系统文件、1份原BGI场景，以及新生成的真ARM64诊断NRO，共25份且合计20360612字节，全体SHA逐项确认：

05_NS测试构建/P303_原高清OGG加BGI_BP真实源码只读QA私有SD演练_不可公开/SD_PRIVATE_25_ORIGINAL_SOURCE_QA_FILES_NOT_A_GAME

目录内switch/即个人私有SD的文件结构。编译程序为switch/subahibi_pc_HD_OGG_BP_readonly_qa.nro，PNG/OGG/BP/故事读取路径均在switch/subahibi_pc_native_hd_qa/之下。这些文件属于用户自己的原PC商业游戏原数据，**不能上传GitHub、不能作为公开下载release，不能替换安装游戏RomFS，更不能混为正式Switch移植补丁**。该目录配有风险README和.gitignore作为误上传提醒。

P303脚本和报告：
01_工具脚本/verify_p303_stage_private_25_source_files_real_HD_OGG_BP_scene_ARM64_qa.py
06_测试记录/P108_私有SD_13真高清PNG原OGG_9BP及原BGI场景SHA和真ARM64按键只读QA25文件_绝不公开.json

## 严格限制

仍不存在原BGI/BP双层VM完整执行，底层title._bp的0x56真实操作码长度与栈效果未知、真实CG动画特效/中文对话/选项/全部音轨/原五部25fps MPEG1+MP2影片均未完整集成，本机Host SDL测试不是Nintendo硬件测试。

所有原PC与旧NS素材、旧汉化补丁、以前NRO及玩家Save保持不变。正式完整游戏安装发行仍严格BLOCKED_NOT_SAFE_TO_INSTALL。

中央质量门禁日志：
06_测试记录/P109_第七十三轮_真AARCH64高清OGG加BGI_BP按键私有SHA_NRO0_14反例与25个私有SD源_全量门禁.log


## 第七十三轮正式完整333工具回归验收

已完整重跑333项中央质量脚本并全部通过；91个受保护源文件SHA、4324份历史QA资源、1505张原PC高清PNG、33454份原OGG验证保持正常。真ARM64 ELF+SDL2/libnx/原OGG与BGI/BP只读按键源探针统一NRO0，官方switchbrew C及独立Python输出逐字节相同（新NRO SHA256：c4ad6d15ea2c2a13ae5d44d56b2c6da256845e5d4733d1aa3ec2f682109dd0f2）。P302主机3路真实C99按键/无按键测试和14类损坏原BP/场景测试通过，P303私人用户SD布局25文件20360612字节逐源SHA确认。P261先前正常诊断NRO SHA完全不变；真实BCI/BP游戏VM执行步数零；真机未上机，非完整游戏。\n\n第73轮冻结快照：06_测试记录/2026-10-19_第七十三轮_真ARM64高清OGG原BGI_BP按钮QA_NRO0和私有SD25文件_333工具不可变质量快照.json\n\n发布BLOCKED_NOT_SAFE_TO_INSTALL。\n