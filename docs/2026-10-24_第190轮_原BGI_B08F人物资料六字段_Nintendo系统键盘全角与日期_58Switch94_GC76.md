# 《素晴日》PC高清中文版→Switch：第190轮，原B0 8F人物资料对话框功能移植

日期2026-10-24；开发项目D:\switch游戏\素晴日\素晴日整合\1.游戏合集\移植新版素晴日ns。**此项目依然BLOCKED_NOT_SAFE_TO_INSTALL，尚无可供Switch安装的完整NRO/NSP，任何工具链来源或手持Horizon系统键盘均未实机验证。**

## 1. 实际GPL2 Win32 BGI B0 8F原语义

从原GPL2源码inc/bgi/os.h、src/sys/dialog.c、src/os/win32/dialogs.c逐段读取，而非根据猜测补齐：原OS_DialogProfile(surname,givenName,nickname,pronoun,month,day)对应Windows资源0x77，拥有四个全角姓名/昵称/人称字段、每个最多10原编码字节加NUL；两个日期列表提供1-12月、1-31日，在代码中0-based保存。月份切换导致日期列表按31、29、31、30等原数组重新裁剪，二月上限为29（原游戏并无年份字段）。原ProfileField代码要求每个输入的字符在原Win32 CP932中必须精确转换为两个字节，若任何半角字符被输入就提示错误并继续停留在原窗口。原Win32对话框没有取消按钮，正常只能点击确认，创建失败时返回0。

Nintendo libnx的系统Swkbd只有单字段返回文本，本轮采用6页系统输入Applets：四页依次取得全角名称，后两页分别输入可验证的数字月份、日期。该流程是真正的libnx swkbdCreate/Show/Close调用，不虚报同一屏可以实现Windows六控件同时排布。Nintendo硬件层是否允许六页连续Applets及SDL焦点/音频保持仍要在实体机器上验收。Nintendo按返回取消时应**整份Profile保持原始值**，兼容原VM失败返回的功能安全含义；这是相对于原Win32“没有取消按钮”的明确平台差异。

## 2. 真正实现与安全性

新增隔离C99源码：

03_脚本工作区/P1042_第190轮_原BGI_B08F_六阶段姓名生日Profile真Nintendo_Swkbd/p1042_real_original_BGIGPL2_Profile_4fullwidth_names_month_day_Swkbd_atomic.c

并扩展原第189轮P1037 Dialog的同一个native libnx键盘源，增加P1037_BeginExternalDialogSession/P1037_ExternalProfileInputPage/P1037_EndExternalDialogSession三个专门供B0 8F使用的原子性输入会话API。任何嵌套B0 84/B0 85对话框或编码切换都不会中途插入并覆盖玩家资料。

原Profile姓名输入逐字段使用真正P546原GBK/CP932或UTF8解码，兼容每个字段原字节小于等于10、禁止ASCII半角和日文半角片假名，阻止不能在原代码页以一个全宽双字节表示的emoji，并在UTF8脚本模式进行真实OS_Utf8ToSjis/OS_SjisToUtf8编码往返确认。数字月份允许1..12，数字日期1..对应月份天数，复现原0-based脚本返回。所有六页结果使用临时缓冲，**只有所有字段及日期都确认并验证通过，才统一修改原四文本输出和month/day**；任何失败均不提交任何一项结果。

## 3. 真正运行原GPL2 C99源码的宿主QA

同目录p1043_host_originalGPL2_Profile_4fullwidth_2dates_realCJK_MonthDay_source_contract.c提供有断言的系统Applet模拟，并一起链接上述真实Profile、修改后的原第189轮真实Swkbd桥接和P546原GPL2中文GBK/日文CP932转换源，不模拟玩家文字转换逻辑。

结果**631项宿主断言通过**：GBK四个真实2字节中文姓名、CP932四个日文全宽字符、UTF8全角返回，2月29日真实有效、2月30日与13月非法，第六页取消或第四页创建失败时保留全部原Profile输出，原ASCII和无法表示的emoji拒绝，原双字段对话框不能在Profile输入期间递归唤起，SDL video不可用不启动Horizon Applet。**50次成功创建的模拟libnx键盘均有50次正常关闭**。

## 4. 真实AARCH64 Switch移植版本现状

上一轮57Switch包含原B0 84/B0 85两个平台输入接口。本轮使用上一轮已验的56Switch GPL2源母版，并以更新过共享Profile会话源的B0 84/85和新增B0 8F两个源对象重新真实aarch64-freestanding-none编译，由LLVM LLD -m aarch64elf -r完整链接并用--gc-sections -u main再生成入口可达候选。

| 指标 | 第189轮 | 第190轮 |
|---|---:|---:|
| 未改GPL2源 | 173 | 173 |
| GPL2安全衍生 + 架构源 | 2+1 | 2+1 |
| 真Switch平台适配 | 57 | **58** |
| 真实完整AARCH64未解全局 | 95 | **94** |
| 真实main入口可达未解全局 | 77 | **76** |

第190轮不仅强定义原OS_DialogProfile，也同时保留OS_DialogInput1/2、原OS_EditFocus与系统键盘、真原TTF字形P1026、高清P441/P454、原MPEG1/MP2及OGG、用户存档SaveLoad/SaveWrite、私有SDK受限文件锁、主故事main和IPL SHA门禁，没有新增未解析项。

真实机器码：

- 03_脚本工作区/P1042_第190轮_原BGI_B08F_六阶段姓名生日Profile真Nintendo_Swkbd/P1044_173orig2der1arch58Switch_SwkbdProfile4names_dates_AARCH64.o
- 同目录P1044_58Switch_mainGC_realProfile_fullwidth_dates_AARCH64.o

两者仍是未完成的ELF64 AArch64 ET_REL，不是可直接安装包。

## 5. 可重复测试、文件记录与剩余阻断

01_工具脚本/verify_p1045_round190_original_BGI_B08F_Profile_6_Horizon_Swkbd_58Switch.py：实际宿主源码631项、两个ARM64模块交叉编译、主游戏真实链接、源VM符号差集及完整SHA验收。

01_工具脚本/verify_p1046_round190_FINAL_original_Profile_B08F_58Switch_94_76_no_Save_or_Hardware.py：独立物理ELF SHA、原API强定义/剩余76项完整对照、取消全字段保留与发行阻断。

PASS归档：

- 06_测试记录/P739_第190轮_原BGI_B08F六字段人物资料真Switch系统键盘631项_58Switch94_GC76.json
- 06_测试记录/P740_第190轮最终_原BGI资料四全角姓名与月日三对话框_真58Switch94_GC76_不可安装.json

剩余76项含Windows安装器、原B0 Child辅助窗口、调试窗口、外部进程/FFmpeg管道回退、Windows OS文件/桌面接口、CRT及Horizon启动链接脚本特殊地址。下一步应核对原B0 Child八窗口是否真的由剧情脚本使用，以及是否可以在Nintendo SDL单窗口中保真呈现多个原BGI子画布，而不是新增无画面的空窗口句柄。不能编造原CG/media文件、偷偷降低原1280×960画质或原48kHz/OGG音质，不要覆盖或上传商业TTF。

**发布与安装仍然BLOCKED_NOT_SAFE_TO_INSTALL。**
