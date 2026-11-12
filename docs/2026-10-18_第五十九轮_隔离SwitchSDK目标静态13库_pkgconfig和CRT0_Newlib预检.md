# 第五十九轮｜真实 Switch 目标 SDK 静态依赖与启动 ABI 预检

日期：2026-10-18

## 完成的真实工作

- 修改隔离高清 SDL2 源码 Makefile：仅从目标 Switch SDK 的 $(PORTLIBS)/lib/pkgconfig/SDL2_image.pc 读取源码编译和静态链接参数；彻底禁止 Windows 主机 SDL2_image.pc 的误匹配。新增已执行负例：即使宿主 pkg-config 报成功，若目标目录 SDL2_image.pc 缺失，GNU Make 依然报错。
- 使用本机已有的可信 pkg-config.exe，对18个已隔离审核第三方历史软件包中15份 pkg-config 文本进行只读复制与路径重定位，解决历史 /opt/devkitpro 绝对路径以及 $(DEVKITPRO) 宏不能在Windows中文路径正常解析的问题。实际解析出并确认13项目标 Switch 静态库存在，包括 libnx、SDL2、SDL2_image、PNG、JPEG、WebP 与 Mesa/GL 等。
- 新增纯 Python GNU-ar/ELF64 目标字节解析：从隔离真实 libnx.a 中找出 switch_crt0.o 原生 _start 符号，核实 aarch64 机器号、libnx 原生 switch.ld 脚本 PHDR、Newlib/PIC libc、libgcc 与 libnosys，以及 devkitPro 原始 switch.specs 中的 GNU 特有链接参数。Zig 0.15.2 自动 Newlib libc 提供路径当前不兼容，仍需解决真正的目标链接。
- 把上述两项和宿主库误判拒绝测试全部纳入全量质量门禁，且要求报告明确未链接真实 ELF/NRO、未运行第三方归档里的 Windows 二进制。

## 来源限制与画质约束

18个 SDK 包来自第三方历史归档，压缩流、SHA、路径以及静态库 AArch64 架构虽已逐件检查，但尚无独立确认的官方签名。SDK 一直放在 D 盘隔离区，不运行其中未经认证的 GCC/binutils/elf2nro 可执行文件，不覆盖原 C:/msys64、系统 PATH 或旧游戏。四份原生 C99 模块虽已通过真实 Switch SDL2/libnx 头文件的 AArch64 编译，但 .o 文件不等于 NS 可启动的 .nro。

项目继续保留 1505份PC原生PNG、33454份原OGG、五段真正1280×960 25fps MPEG1与48kHz MP2原音码流；不回退到800×600旧ONS，不写原游戏、安装包或玩家 Save。真实 NS GPU、原 BGI D3D9 图层混合、影片/OGG播放及 Save 隔离均未实机验证。正式安装保持 BLOCKED_NOT_SAFE_TO_INSTALL。

## 证据位置

- 01_工具脚本/verify_p228_offline_real_sdk_pkgconfig_ascii_libs_complete_no_exec.py
- 01_工具脚本/verify_p231_real_libnx_newlib_crt0_target_linker_abi_readonly.py
- 06_测试记录/P53_第三方历史SDK原pkgconfig文本隔离ASCII重定位_静态Switch依赖闭包无执行.json
- 06_测试记录/P54_隔离真实Switch_SDK启动符号和Newlib链接所需旗标只读预检_非NRO.json
- 06_测试记录/P54_第五十九轮_隔离SDK目标SDL2image静态13库_CRT0_Newlib及原画质全量门禁.log


## 第五十九轮全量复核完成

已实际跑完全项目中央质量门禁：291份Python工具语法、91项受保护原文件SHA、4324份旧测试件、1505份原PC高清PNG、33454份原OGG均通过。目标SDK 15份 .pc ASCII重定位、13个真实目标静态库和libnx crt0/Newlib条件均纳入强制检查。仍未通过真正ARM64 Newlib链接，也未生成真实Switch NRO；未执行未经独立签名验证的第三方工具程序。旧游戏和玩家存档没有修改。发布状态保持BLOCKED_NOT_SAFE_TO_INSTALL。

快照：06_测试记录/2026-10-18_第五十九轮_隔离SDK目标13库_Newlib启动291工具最终快照.json
