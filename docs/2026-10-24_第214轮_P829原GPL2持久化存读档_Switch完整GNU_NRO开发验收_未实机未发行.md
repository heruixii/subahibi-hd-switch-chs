# PC 新版高清《素晴日》→ Nintendo Switch 第214轮：P829 续接报告

日期：2026-10-24；唯一工程根：`D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns`

**本轮确实更新实际 GNU AArch64 游戏机器码，原 GPL2 存档接口从隔离一次性 QA 路径升级为独立私人持久化目录，并重新完成真实源码链接/NRO0 格式验收。但是正式移植未完成，`release_install_status=BLOCKED_NOT_SAFE_TO_INSTALL`。**

## 一、核心安全与画质原则未改变

- 原版 PC `BGI.exe` 1.647 经 SHA 锁定，54个 BURIKO ARC20 原商业档案共4,502,968,565字节，本工程上一轮 P823 全档重新读盘验SHA全PASS；130份故事、55份IPL/BP原SHA仍匹配。**使用原档原画、原OGG以及25fps MPEG1+MP2，不转换为800×600、不降低音画品质。**
- 最新主入口 P822 不是错误的 P818“展开资源目录门禁”，而是**通过真实 FileOpenRead/Size/Read/Close 逐一检查54个 ARC20 原始封包头/大小/成员数**的强ARM64入口。该入口270个否定情况＋2个正向C99宿主测试；虚拟PC `C:\` → `sdmc:/switch/subahibi_pc_native_hd_qa/story/` 的54个ARC路径P826宿主测试PASS。
- 原GPL2 GameOnlyVM1.647私有Profile的3328opcode mask以及完整65个HOS适配、Mesa16shader、原音画接口均作为源码合入机器码，strict PIE未定义符号数 **0**。这仍是静态/宿主验收，不是真机运行。

## 二、P827 本轮重要进展：原版 `.cad` 持久化 SaveWrite/SaveLoad

原 P947、P950、P955 已有严格 GPL2 开发QA存档接口，但目录 `dev_only_disposable_save/` 仅供一次性实验。我们没有粗暴更改原受审源文件，而是建立**独立可审计源码派生对象**，将完全相同的 `BGI####.cad` 四位数字原引擎路径限制映射到：

`sdmc:/switch/subahibi_pc_native_hd_qa/persistent_save_slots/`

此目录与 `story/` 原商业资源完全分开；不能写入原PC存档、Switch Title ID、系统存档或别的游戏路径。只允许指定根目录存在时通过 SDL 文件API写/读/删；缺少路径或不存在根时失败，绝不将写入自动重定向到玩家存档。保留了 P955 对原游戏 `0x40+gGlobalMemSize` 实际存档长度的严格检查和16MiB上限，避免原GPL2 `ReadFileAt` 无边界写导致全局内存破坏。

- P827 实际源码包括原未修改 `src/core/savefile.c`、`src/core/hash.c`、GPL2 P947/P955/P950 安全实现的持久化目录派生版。
- **372项原版GPL2宿主验证全部PASS**，包括写入原 `.cad` 头、hash scramble、SaveReadHeader、SaveCheck、SaveLoad、256字节原游戏全局内存精确恢复、破坏校验和后拒绝及原内存不变。
- 因老宿主夹具先验证一个非游戏格式的8字节测试文件，严格Save读取器会**正确拒绝**，因此分两层执行：372项基础读写机制使用原 P948 兼容读取器的私人目录派生版；真正纳入ARM64游戏的 P955 **严格读取器**另经原320B(64+256)存档以及319B/321B/0B长度错误、内存非法、损坏测试全部PASS。没有为通过测试放宽严格判断。
- 三个完整可运行 AArch64 ELF机器码对象 `OS_FileOpenRead/Read/Size/Seek/Close`、`OS_FileCreate/Write`、`OS_FileDelete` 构建成功。所有源文件相对原GPL2旧源码保持不变；独立QA存档路径不会被误用为玩家默认永久存档。

## 三、P828：`OS_FileAttrs` 能看到真正的持久化 `.cad` 文件

- 从真 P915 SDL IME与HOS `stat` OS_FileAttrs 源码派生，只增加相同严格原 `P947_MapOriginalBGISlotToDevSave` 白名单。合法原BGI `C:\BGI0012.cad` 映射到私人持久目录，由**真实 `stat` 结果**判断是否存在、文件大小/读写类型；没有旧档时返回不可用。资源原路径、滑出沙盒、文件与目录后缀拒绝、原SDL输入法保持不变。
- 从原 P947 源码真实提取文件名映射器，只在测试源构建成独立映射函数，不用虚构的host路径替身；C99宿主正反例通过，AArch64真实 `OS_FileAttrs` 与SDL IME编译通过。

## 四、四类持久化源实际进入 GameOnly 机器码并经原 GNU 链接

- 在原 `P958.actual_c_sources` 组装中，只替换第6个严格文件读取器为P827私有持久化源；在51输入主游戏组装中，用新的P947写、P950删、P915 stat替换旧QA对应单个AArch64对象，**没有用 `--allow-multiple-definition` 偷过编译**，其余原GPL2代码不动。
- 重跑源级整合验证：`P811_...` 中 `actual_compiled_main_owner_ALL54_original_ARC20_file_header_size_index_guard_machine_integrated=true`、`original_GPL2_strict_PERSISTENT_owner_only_privateSD_SaveWriteReadDelete_REAL_NATIVE_source_machine_integrated=true`、`actual_native_GPL2_real_STAT_BGI_four_digit_persistent_SaveAttrs_instead_of_story_only=true`。
- 再次真实执行从GNU签名源码+官方devkitPro补丁派生的 AArch64 `ld-new.exe`，以原版 `switch.specs` 与 `switch.ld` 全参数链接最新ARM64代码，退出码0，无未定义符号。原 switchbrew源码编译 `elf2nro` 真实产生有效NRO0，`MOD0`、`.nx-module-name`、`DT_RELR` 和加载段结构检验PASS，8,081,408字节。**开发用ELF/NRO验证后自动删除，没有提供未经真机检验的安装包，也没有绑定任何商业媒体。**
- 最新权威验证结果：`06_测试记录/P827_第214轮_真GPL2_原CAD持久化SwitchSD隔离存读删路径_372宿主加真实3ARM64对象_非实机.json`、`P828_第214轮原GPL2真实FileAttrs保留原ARC20+原CAD持久化只读stat_宿主_ARM64_非实机.json`、`P829_第214轮最终_原1647真VM54ARC20_原GPL2持久化存读档372正反严格保护_全GNU_NRO0_未上机未发行.json`。

## 五、私人 SD 部署与安全：还未接实体设备

- `01_工具脚本/p1167_private_SD_original_ARC20_deployment_check_copy_SHAsafe.py` 默认**只干跑零复制**。当确认 `--sdroot` 真正挂载用户自己的Switch SD并且明确`--commit`后，才顺序复制原54个ARC20及一份SHA验证IPL到固定 `story/`，逐文件完整SHA核验，原目标已存在且内容不同则禁止覆盖；全部原资源拷贝成功后才创建其兄弟目录 `persistent_save_slots/`，不迁移、覆盖或删除任何旧 `.cad` 存档，也不假装当前已写成功。
- 本轮再次执行 P824 六项非商业模拟小文件安全用例，以及全54商业源零复制干跑；都PASS。没有将4.5GB商业档案上传GitHub或拷贝到非设备的大型重复目录；原PC游戏、原存档和母版未改。
- 本机 `Get-PnpDevice -PresentOnly` 没有检测到 Nintendo `VID_057E` 或DBI MTP。实体Switch未在本工作区暴露，不能执行或宣称真实Horizon SD读写及存档恢复，也未检查所有原版剧情/间接VM分支。原main 0x7F在已分析的55份BP中**0处直接调用**，但动态运行语义未完全证明；仍保留NotImplemented而非伪造成功。

## 六、剩余真正发布硬阻塞

1. 用户将自己的Switch SD真实挂载到能由ShunCode访问的Windows卷；核实卷路径无误后仅在私人设备上按P1167复制54原档与IPL并校验全套SHA。
2. 真实HOS家用机启动、SD路径/文件服务、退出与重入、持久化 `SaveWrite/SaveLoad` 往返及电源中断安全性还没有实机证据；目前存档SDK内部QA只是 C99/ARM64源码验收。
3. 在实体 Switch 对照原版130剧情、55系统BP，验证 1280×960 原画／中日字体、25fps MPEG1+MP2音画同步、OGG配音与BGM、菜单/输入、全部分支、返回标题与存档恢复。遇到未支持的原PC1.647运行时0x7F或其他私有OP，须结合真实迹线移植，绝不把未实现操作码伪装成成功。
4. 工具链发行前还应核实官方SDK全部依赖的可信来源及OpenBGI GPL2和其他依赖许可。**公开发布只可包含合法自有补丁/独立源码，不得附加用户的商业 ARC20、OGG、影片和CG。**

**总状态 `P829=PASS_R214_INTERNAL_OWNER1_647_REAL_ARC20_54SHA_NATIVE_PERSISTENT_Save_372Host_GNU_NRO_STRICT_NO_HARDWARE`；`release_install_status=BLOCKED_NOT_SAFE_TO_INSTALL`。本轮开发代码完成，但游戏正式移植仍未完成。**
