# 《素晴日》NS高清移植，第195—196轮：原文件列表与目录选择真正Horizon FS接口

日期：2026-10-24。项目仍位于 D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns。原正版PC高清CG 1280×960、25fps五部MPEG1与MP2原声、所有OGG、IPL及私有TTF原始文件和玩家存档完全未改动。**目前不存在可安全安装的NRO/NSP。**

## 第195轮：实现原OS_WriteNativeFile，并处理一个被严格PIE真正揭出的回归

原GPL2 OpenBGI的 src/core/version.c 明确通过 Engine_SaveGamesJson → OS_WriteNativeFile(path,data,size) 将游戏列表文本写成原生配置。最初C99开发原型使用open/write/fsync/rename的通用CRT调用，虽通过实际Windows宿主41项测试，但接进真实AArch64 59Switch后新引入 `fsync`、`_rename_r` 等依赖，导致严格Switch最终PIE未解项**51→52**，已**废弃，未合入正式开发母版**。

更正后的真实Switch适配：

`03_脚本工作区/P1053_第195轮_原BGI游戏列表gamesJson仅QA隔离原子写入_59Switch/p1056_original_BGI_WriteNativeFile_qa_config_gamesJSON_REAL_Horizon_FS_IPC.c`

实现原 `OS_WriteNativeFile` ABI，但**只允许** `sdmc:/switch/subahibi_pc_native_hd_qa/config/games.json`；其他全部拒绝，包括Nintendo Save和所有原商业资源。真正调用libnx的 `fsdevTranslatePath`、`fsFsCreateFile`、`fsFsOpenFile`、`fsFileWrite`、`fsFileFlush`、`fsFileGetSize`、`fsFsRenameFile`、`fsFsDeleteFile`。专有临时文件名 `games.json.tmp`；同步写入并验证文件长度后，调用Horizon重命名服务发布。为避免非原子覆盖，**有旧版配置则拒绝覆盖**，明确属于开发QA受限功能而非完整桌面写盘API。真实SD硬件重命名语义、并发竞态与断电持久性仍未测试，不能作为发行版存档方案。

宿主直接编译这一份原生C99源码；只用模拟Horizon FS IPC层把命令映射到单独的ASCII私有宿主临时目录，不触碰用户中文路径；**189个检查通过**，覆盖六种FS失败环节、已有输出不能覆写、暂存清理和路径逃逸拒绝。

真实ARM64源编译、游戏完整链接、`-u main --gc-sections`链接均PASS。原58Switch完整未解94→**59Switch完整93**，main根76→**75**。继承上一轮QA副本的102只读常量指针RELRO数据节转换，使用历史libnx原版 `switch.ld`、四个CRT真实启动对象及**严格`-pie -z text`**最终真实链接，原102项不合法只读段重定位仍为0，真实最终缺符51→**50**。

文件与测试：

- `01_工具脚本/verify_p1058_round195_original_gamesJSON_REAL_HOS_FS_IPC_59Switch_strictPIE50.py`
- `01_工具脚本/verify_p1059_round195_FINAL_true59Switch_HorizonFS_GamesJSON_50blocked.py`
- `06_测试记录/P747_第195轮_原BGI游戏目录JSON真实libnx_HorizonFS_IPC189宿主测试_59Switch93_GC75_正式PIE剩50.json`
- `06_测试记录/P748_第195轮最终_原BGI游戏配置真HorizonFS原子写入59Switch_严格PIE剩50_不可安装.json`

## 第196轮：原OS_BrowseFolder由实际Nintendo Swkbd输入并由Horizon验证目录

原GPL2 BGI文件选择VM操作 `OS_BrowseFolder(path,capacity,title,initial)` 的真正开发版移植：

`03_脚本工作区/P1060_第196轮_原BGI选择目录真Nintendo键盘Horizon只读QA故事目录_60Switch/p1060_original_BGI_OS_BrowseFolder_TrueNintendo_Swkbd_Horizon_SD_StoryDir_readonly.c`

它确实使用libnx `swkbdCreate/Show/Close`，共享前轮P1037输入会话锁，不允许嵌套系统软键盘；原GBK/CP932日文中文标题经真正P546转UTF8。Nintendo选择的目录路径先严格限定为 `sdmc:/switch/subahibi_pc_native_hd_qa/story` 或其字母数字、下划线、横线组成的安全相对子目录，拒绝 `../`、重复斜线、尾随斜线、其他Title/Save路径、未知路径和过长缓冲。然后**真实**调用 `fsdevTranslatePath → fsFsOpenDirectory(只读) → fsDirClose`，成功后才修改原VM输出路径。原版Win32文件夹浏览器是图形窗口，这里通过系统键盘输入目录名，交互形式有明确差异；实体Switch系统Applet、中文字体显示与目录服务还需真机QA。

宿主**330项C99断言PASS**，原P546 CP936双字节标题、有效sysprg子目录、非法路径在Horizon IPC之前拒绝、未知文件夹FS不通过、目录关闭、视频不可用、编码切换以及取消不改调用者输出全部验证；21次系统软键盘模拟创建与关闭严格配平。

真ARM64平台对象由59份变为**60份**，完整未解93→**92**，main根75→**74**，严格Switch PIE最终缺符50→**49**，仍没有新增未定义符号，也没有不合法102项旧重定位。两份物理机器码均为ELF64 AArch64 ET_REL而非可运行NRO：

- `03_脚本工作区/P1060_第196轮_原BGI选择目录真Nintendo键盘Horizon只读QA故事目录_60Switch/P1062_173orig2der1arch60Switch_realBrowseFolder_HOS_Swkbd_AARCH64.o`
- 同目录 `P1062_60Switch_mainGC_BrowseFolder_Swkbd_Horizon_AARCH64.o`

开发版QA用上一轮已经验证的`switch.ld`严苛PIE＋102项仅隔离副本RELRO节调整，不更改任何原GPL2机器码或原声音图像文件。

复现测试与最终独立硬门禁：

- `01_工具脚本/verify_p1064_round196_original_BGI_BrowseFolder_REAL_Swkbd_HOS_FS_60Switch_STRICTPIE49.py`
- `01_工具脚本/verify_p1065_round196_FINAL_native60_REAL_CJK_BrowseFolder_STRICTPIE49.py`
- `06_测试记录/P749_第196轮_原BGI_文件夹选择Swkbd加实际HOS只读目录校验330项_60Switch92_GC74_最终PIE49.json`
- `06_测试记录/P750_第196轮最终_真实60Switch读目录和中日文字软键盘_STRICT_PIE最终49仍不可安装.json`

## 未完成的重要事项

严格PIE剩余**49项**是真实未定义：其中包含与Switch叙事游戏通常无关但仍保留在原OpenBGI总入口中的Windows安装器、注册表、快捷方式与外部进程功能，此外有八个需要实际离屏画布/销毁回调而不能伪造的B0子窗口接口、调试窗口、文件对话框、文件属性及Mesa `nir_shader_clone`。后续优先做**原GPL2主入口的游戏专用功能裁剪和真实可达性评估**，争取一次解除多个与本作不相关的安装器依赖，不应继续无限加入无画面的空OS符号实现。

截止本轮，隔离历史SDK没有作者签名验证，真正Nintendo主机没有执行测试，正式PIE最终链接仍失败且**没有最终可用NRO或NSP包**；不得发布、不应告诉用户直接安装。
