# 《素晴日》NS高清移植，第197轮：严格Switch最终链接49项逐源码定位

2026-10-24。承接第196轮**60份真实Switch原生适配，原173份GPL2 C99模块，完整ET_REL未解92、main-root未解74**。应用之前仅作用于QA副本的102项历史只读指针RELRO节修正后，历史libnx原版 `switch.ld` ＋真实CRT ＋ `-pie -z text` 的**严格最终链接**真实未定义为**49项**，不合法只读段重定位为0，但最终链接**仍失败且不存在可安全安装NRO/NSP**。

## 本轮真正核查

从第196轮LLVM LLD完整错误记录逐个解析49个缺失全局名称、`>>> referenced by`原C99源码文件和行号、产生引用的符号所有者函数，再从真实60Switch机码SHA反核。不是按名称随意猜测，也没有把不曾执行的代码直接宣称“剧情肯定不需要”。

| 真实49个未解函数／依赖的类别 | 数量 | 后续正确处理办法 |
|---|---:|---|
| 桌面安装器、卸载器、注册表、快捷方式、光盘解包 | 21 | 优先证明不属于固定NS游戏启动路径；重建GPL2游戏专用引擎分支 |
| Windows外部进程、管道、IPC、命名互斥体 | 10 | 明确原VM可达性，保留真正脚本安全语义，分别处理 |
| 原B0 10—1C八个独立子窗口OS句柄／DC | 8 | 需独立SDL子画布、真实像素渲染和销毁回调；禁止空句柄 |
| 桌面调试器额外窗口 | 4 | 评估游戏发布模式是否可编译移除，不应无依据清零 |
| 桌面文件属性与文件选择器 | 2 | 需要真实平台功能或经证据支持的非运行时分支 |
| 桌面拖放与壁纸操作 | 2 | Switch无Windows桌面，必须明确语义差异及可达性 |
| 通用多游戏启动器 | 1 | 固定游戏ROMFS/QA SD路径替代电脑多游戏目录选择 |
| Mesa NV50 NIR程序克隆 `nir_shader_clone` | 1 | 真正Mesa源码/图形后端兼容构建，不得编造shader返回值 |
| **合计** | **49** | 以上每项均具有真实LLD符号引用追踪 |

关键追踪示例：`CheckRegistration` 直接来自原 `src/vm/ops_sys.c` 的 `Opcode_Sys_CheckRegistration`；`Install_RunDialog` 来自原VM安装器操作码；`OS_ChildCreate` 来自 `src/sys/child.c` 的 `Child_Create`；`Launcher_Run` 来自原GPL2 CPU适配版 `Engine_Main`；`nir_shader_clone` 被 `nv50_program_translate` 引用。这些依赖的**函数所属分支**已证明，但是否会由本作故事脚本执行，仍需真正源码编译与真VM可达性检查，不能由文件名判断。

## 为什么优先游戏专用Engine_Main

当前第190轮游戏原主入口继承OpenBGI通用桌面开发功能。经读取实际P928 GPL2架构改版引擎 `Engine_Main`，在加载故事与运行VM之前仍保留 `--list`、`--extract`、安装器调用、通用 `Engine_ChooseGame/Launcher_Run` 等路径。因此即使Nintendo主机只运行一款《素晴日》，链接器仍可能从通用入口保留非游戏功能，进而将安装器/Windows程序接口拉入真正的ELF，增加大量无法发行的兼容工作。

后续优先事项：在**隔离GPL2源副本**中规划固定Switch引导模式；只裁剪已确定与主线资源/系统存档/截图/HD音轨完全无关的桌面工具分支，保留正版原游戏VM事件、CG/GPU字形、影片MP2/OGG、按键与Horizon FS。需要干净重建早期母版源码中包含的Engine_Main模块，再运行原玩法QA及真正严格PIE；禁止使用 `--allow-multiple-definition`、用空函数代替原符号或绕过发行验证。

## 可复现源码记录

- `01_工具脚本/audit_p1066_round197_original_strictPIE49_all_symbols_real_GPL2_callsite_categories.py`
- `01_工具脚本/verify_p1067_round197_FINAL_strictPIE49_original_source_LLD_refs_no_stubs.py`
- `02_清单与差异/P197_严格SwitchPIE剩49全符号真实引用位置与移植优先级.csv`
- `06_测试记录/P751_第197轮_严格PIE真实49项未解_原GPL2源码引用与Mesa分类_优先重建游戏专用入口.json`
- `06_测试记录/P752_第197轮最终_49项安装器调试窗口真实引用全追踪_不伪造游戏入口与NIR.json`

**原PC高清CG、25fps影片/MP2、OGG、私有TTF、汉化脚本与玩家Save均未修改；实际Switch硬件、历史SDK签名以及可安装NRO/NSP仍全部缺少完整验收，不能把当前ET_REL误当成游戏成品。**
