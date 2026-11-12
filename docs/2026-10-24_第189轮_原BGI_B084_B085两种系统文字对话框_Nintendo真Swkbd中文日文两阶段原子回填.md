# 《素晴日》PC高清移植Switch，第189轮：原BGI单/双字段对话框移植到Nintendo系统键盘

2026-10-24。真实原GPL2源码接口、P546原GBK/CP932编码及libnx SwkbdConfig在本轮使用；未生成可安装NRO/NSP。原PC高清CG 1280×960、原影片25fps及MP2/OGG音轨、玩家存档、商业字体未改动。**BLOCKED_NOT_SAFE_TO_INSTALL**。

## 1. 源码语义审计

原GPL2 OpenBGI inc/bgi/os.h、src/sys/dialog.c及原Win32 dialogs.c确认：

- B0 84：OS_DialogInput1(title, initial, maxLen, out)，一个有初值的文本输入框，点击确认返回1并更新0x100原字节缓冲；取消返回0且不改调用者文本；
- B0 85：OS_DialogInput2(title, label1, initial1, maxLen1, out1, label2, initial2, maxLen2, out2)，两个各自有原文字标签、初值和限制的字段。必须两者整体确认才可更新两个原0x100字节缓冲；任何一页取消都不得只写入部分字段；
- 输入按当前原游戏OS_SetTextEncoding决定原GBK/日文CP932或原UTF8模式；日文字节、中文字节不可在maxLen上裁开。

Nintendo系统swkbdShow只提供**一个**文本返回缓冲，本轮实际实现两个页面依次打开真实libnx applet，分别显示原标题和字段label。不是谎称Nintendo原生一次能显示两个Windows Edit框。实际任一页面取消都回到原游戏无更改结果；先临时存放两份已验证GBK/CP932或UTF8，最后同步写入out1/out2。

## 2. 真正实现和失败语义

隔离新增原生C99文件：

03_脚本工作区/P1037_第189轮_原BGI_DialogInput1_Input2真Nintendo_Swkbd_CJK原子取消/p1037_true_original_BGIGPL2_dialog_1_2_Nintendo_Swkbd_safe_CJK_atomic_commit.c

它实现并导出原GPL2 OS_DialogInput1和OS_DialogInput2真实符号；调用libnx swkbdCreate、swkbdConfigMakePresetDefault、swkbdConfigSetHeaderText、swkbdConfigSetSubText、swkbdConfigSetInitialText、swkbdShow、swkbdClose。原标题与字段标签经原P546 OS_SjisToUtf8安全解码以显示Unicode。

输入先作完整UTF8严格合法性验证，再经原OS_Utf8ToSjis/OS_SjisToUtf8逐字双向一致性验证，拒绝非法代理码位、无法映射的emoji、超长原字节输出；maxLen只有>0才限制，否则遵循原版无限但最多0xFF缓冲字节。主VM线程持有互斥重入标记，SDL video不可用时不伪造系统键盘已可用，异步编码变更时拒绝覆盖，关闭Applet路径均配平。

## 3. 真实C99源码链接宿主测试

同目录p1038_host_real_BGIGPL2_B084_B085_Nintendo_Swkbd_CJK_dialog_contract.c与真正P546源码一起编译，只有libnx applet硬件服务由模拟返回，其他编码转换、原BGI B084/B085调用、缓冲写回、事务回滚全部真实执行。

**270项断言全部通过**，包括：实际GBK「汉字」四字节、CP932「日」双字节、UTF8模式六字节，maxLen=1/2/3/5/6严格边界，取消第一/第二页面不变更调用者，第二页出错两字段全部保留，原标题及字段label正确传给系统键盘，emoji和恶意UTF8代理码位拒绝、空字符串确认清空、重复/递归调用拒绝、无Video拒绝。19个创建完成的模拟系统键盘Applet均对应真实swkbdClose。

## 4. 最新真正ARM64游戏开发机器码

从上一轮第188轮P1035 56Switch完整真实AArch64 ET_REL追加一个实际libnx B084/B085 native对象，zig cc C99严格-Werror和ld.lld --relocatable编译链接均通过。未做伪造空函数。

| 指标 | 第188轮 | 第189轮 |
|---|---:|---:|
| 原GPL2未改模块 | 173 | 173 |
| GPL2安全衍生、架构适配 | 2+1 | 2+1 |
| 真Switch native适配 | 56 | **57** |
| 完整对象未解 | 97 | **95** |
| 游戏main可达候选未解 | 79 | **77** |

确切消除两个原Win32 BGI API：OS_DialogInput1、OS_DialogInput2；无新增未解析符号。原P971完整脚本IPL SHA、P454原高清GPU画布、P1026真素晴字体私有SHA字库、原MPEG1/MP2+OGG、真系统键盘聚焦、原SaveLoad/SaveWrite、受限新libnx FS锁、C++支持符号、主游戏main全部保留在两个实际AARCH64机器对象中。

机器码：

03_脚本工作区/P1037_第189轮_原BGI_DialogInput1_Input2真Nintendo_Swkbd_CJK原子取消/P1039_173original2der1arch57Switch_DialogInput1_2_real_libnx_AARCH64.o

同目录P1039_mainRoot_GC_57Switch_Swkbd_two_DialogInput_AARCH64.o。

## 5. 复核脚本与剩余阻断

重做真实P546宿主270项、Switch C99 native编译、LLD完整/main根原游戏符号保存：

01_工具脚本/verify_p1040_round189_original_BGI_B084_B085_two_Nintendo_Swkbd_CJK_atomic_57Switch.py

独立物理SHA、完整依赖manifest、取消双字段原子语义和发行不可安装门禁：

01_工具脚本/verify_p1041_round189_FINAL_genuineB084_B085_57Switch95_main77_safeCancel.py

实际PASS：

- 06_测试记录/P737_第189轮_原BGI_B084_B085真libnx键盘双字段原子回填270断言_57Switch95_GC77.json
- 06_测试记录/P738_第189轮最终_真实Nintendo两字段系统键盘中文原子取消_57Switch95_GC77发布阻断.json

下一步解决原B0 8F四个人物姓名/代词及月份/日期的Profile资料对话框、原B0 Child辅助窗口、Win32残留及真实链接脚本。实机Horizon软键盘Applets进入/返回SDL焦点仍未在真实Switch设备验证；不应因此发表可直接安装包。历史SDK来源亦未完成可靠验签。**BLOCKED_NOT_SAFE_TO_INSTALL。**
