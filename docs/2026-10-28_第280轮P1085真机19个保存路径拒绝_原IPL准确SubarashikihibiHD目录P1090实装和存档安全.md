# 第280轮：P1085首次定位19个保存路径拒绝；P1090原IPL准确用户数据目录映射实机部署

P1085用户亲测：右摇杆已经可以接受，可再适当优化；点击Save空槽仍无反应。DBI通过原14项四NRO严格只读回收四日志到`D:/tmp/subahibi_P1085_AFTER_REAL_SAVE_FAILURE_4LOG_READONLY_20261028_R1/`。四份旧P1080完整字节前缀不变，P845新加68545字节，P853新加7784，P859脚本错误文件零增长。

**真实断点**：新增的`P1085 SAVE_IO`标记准确19条`phase=CREATE_REJECT`，包括原虚拟文件`C:\BGI.gdb`一次及`C:\UserData\Su...`十八次。原P1171写映射白名单仅支持`C:\BGI####.cad`，因此用户确实选中存档槽，却被文件路径兼容性在OS_FileCreate层挡住。这是实际日志确证的原问题之一，不能凭此宣称最终存档完全恢复。

进一步读取**原PC新版真实启动脚本**`04_HD转换样本/P2_扩展归档/system/ipl._bp`，明确含`SubarashikihibiHD`恰好两次、`UserData`恰好一次（而非猜测）。新版`C:\UserData\SubarashikihibiHD\BGI####.cad`及对应`BGI.gdb`是游戏独立数据目录，与旧版根`C:\BGI####.cad`不同。

P1090在原GPL2 native OS源层只支持四类**完整严格名字**：根`C:\BGI.gdb`映射私有`UserData/BGI.gdb`；旧根`C:\BGI####.cad`映射原`persistent_save_slots/`不变；`C:\UserData\SubarashikihibiHD\BGI.gdb`和`...\BGI####.cad`映射私有`UserData/SubarashikihibiHD/`。`OS_FileCreate/Write`保留真正返回值并最多48条`P1090 SAVE_IO phase=CREATE|CREATE_REJECT|WRITE`有界日志；`OS_FileOpenRead`支持真实系统数据库（不错误按CAD精确长度拒绝）及真实存档长度守卫；`OS_FileAttrs`只识别原游戏IPL准确文件夹，`OS_DirCreate`只允许真实游戏自有目录，`OS_FileDelete`只允许原`BGI####.cad`，拒绝删除任何BGI.gdb。所有其他Windows分区、目录穿越、其他游戏文件、冒号路径、恶意扩展拒绝，17项宿主负例通过。真实新五原ABI对象、完整65HOS SHA源门禁和真正GNU/libnx NRO0构建通过。

全新完整P1090 NRO大小**8,122,368字节**，SHA256：`91db5c1c5e4b61f114d80dd65b7b1b7fdadf2250de7db9bdacc5267a08e9e0c6`。独立SHA复核：`06_测试记录/P1090D_第280轮完整原65HOS新真实NRO0与正确IPL五源接口和全部旧版SHA独立复核.json`。已通过DBI**只新增**到`1: SD Card/switch/subahibi_pc_native_hd_qa/`并从真实设备整个NRO复制回PC：`D:/tmp/subahibi_P1090_REAL_SWITCH_FULL_NRO_SHA_READBACK_20261028_R1/`，SHA全字节一致。为确保原IPL私有目标目录存在，严格检查UserData原先0项后，仅在它下面创建准确`SubarashikihibiHD`文件夹，无其他现有数据被删改。独立只读复核root15包含5个NRO（P1033、P1074、P1080、P1085、P1090），55项剧情、2中文、字体及三存档目录仍在，UserData仅有准确新子目录，用户原存档没有被改写。上一版本保留回退，未执行删除旧NRO。

**重要**：首次保存及读取成功并未在P1090实机确认。下次用户应在Switch Homebrew Menu启动`P1090`，在剧情Save里按ZL+右摇杆精准瞄准槽位1，按A后确认是否显示存档时间/截图以及是否能在Load界面读取该真实档。勿主动覆盖已有用户存档。退出游戏重接DBI后，本地准备了PowerShell零语法错误的**只读四日志回收脚本**：

`03_脚本工作区/P1427_第280轮_P1090原IPL实机首次保存和读取后五NRO精确目录只读四日志/p1427_P1090_P1085_P1080_P1074_P1033_exact15_onlyfourlogs_WPD_READONLY.ps1`

后续应从P1090新`P1090 SAVE_IO`判断`CREATE`和`WRITE`是否真正成功，并只读检查`UserData/SubarashikihibiHD/`是否生成原格式存档，必要时进一步追到SaveLoad原安全reader；绝不能声称“源码和编译都过了所以真正存档已经修好”。字幕最终中文字形与游戏帧率卡顿仍单独未解决，高清画质音质不得缩水，禁止将本QA版本称为正式release。
