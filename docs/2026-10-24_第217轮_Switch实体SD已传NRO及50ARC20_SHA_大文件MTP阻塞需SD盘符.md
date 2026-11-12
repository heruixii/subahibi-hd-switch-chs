# 第217轮：真实 Switch DBI MTP 私人安装进度

日期：2026-10-24。Windows 已识别 Nintendo Switch WPD（VID_057E、PID_201D），1: SD Card 可访问。全程只操作 switch/subahibi_pc_native_hd_qa，不碰 NAND/系统存档。

## 实际已安装与校验

- P830 全原1.647游戏NRO 8,081,408字节已传入Switch，从设备回读SHA256一致：80b97ecffdf87791da8fb2a91781e47be1e29ea31447f3a17c84df98d1d8f591。
- story/ipl._bp 3,344字节已上传并从Switch回读SHA256一致：4c86a967974ba8a1aecae3af2b9750762c70ad9e61a3025b6f1b92ad1c28512f。
- 54个BURIKO ARC20中有50个已在Switch落盘并整文件回读SHA256匹配原PC母版；详细日志P835。
- 独立持久化存档目录persistent_save_slots已创建，未改动任何既有玩家存档。

## 未完成安装（不可启动判定为通过）

- data04010.arc：MTP设备侧显示312,838,704字节，Windows大文件回读失败，尚不能确认SHA一致。
- data02100.arc、data02980.arc、data02920.arc：未成功传入，原文件均已在本机完整SHA核验。Shell WPD的大文件操作出现超时，已经停用该传输路径。
- Switch SD story当前实际为52份文件：50个已完整SHA的ARC20、一个仅校验大小的ARC20、一个SHA验证过的IPL；目标应为55份。
- P836记录最后四个文件的状态。没有NAND安装、没有公共发行、没有运行期可玩性实测。

## 物理切换访问方式后继续

请退出DBI MTP，在Hekate Tools > USB Tools > SD Card启用USB Mass Storage（不要选择eMMC/emuMMC），或关机取出microSD通过读卡器连接Windows。仅在Windows出现真实盘符且可见原Nintendo、switch、atmosphere目录时继续；如提示格式化/修复，一律取消。

下一步：直接在真实盘符下完整SHA重验已有50个档案及data04010；若data04010不匹配，则只在本项目私有story目录隔离原文件后恢复正确副本，不触碰用户Save。再复制剩下三个ARC20并核对目标完整SHA，确认55份资源和NRO齐全，安全弹出SD，交给用户在Homebrew Menu首次启动验证。

状态：私人实机测试程序已经写入，但原资源缺失3份，不能宣称安装完成或正式移植可玩。
