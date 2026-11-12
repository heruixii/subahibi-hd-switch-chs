# 第五十八轮：第三方历史开发包隔离与真实Switch头文件AArch64源码编译

日期：2026-10-18
工程根：D:/switch游戏/素晴日/素晴日整合/1.游戏合集/移植新版素晴日ns

## 已实际解决：历史工具包数据与真实libnx/SDL2头文件可读

根据用户明确要求试用非官方源，找到 Leseratte 的历史devkitPro归档（https://wii.leseratte10.de/devkitPro/）。其中收录2026年6月的devkitA64 r30和对应GCC 16.1.0/binutils 2.46.0、libnx 4.12.0；第三方归档还包括Switch SDL2 2.28.5、SDL2_image 2.0.4、Mesa、libpng、JPEG、WebP、zlib、switch-tools以及Newlib、pkg-config等，共18个历史包。

隔离路径：
07_工具链环境/2026-10-18_第三方历史devkitPro包_隔离审查/

已完整下载并保存每个源URL、SHA256、makepkg包内元数据，逐个解压测试并检查压缩流完整性、.MTREE中的内部文件SHA256、归档路径越界、软/硬链接去向和18个包的依赖闭包。报告：
06_测试记录/P52_第三方devkitPro历史18包SHA256压缩完整性_路径审查与原版签名未验证.json

随后仅将归档的文件数据隔离展开到：
07_工具链环境/2026-10-18_第三方历史devkitPro包_隔离审查/isolated_untrusted_sdk_data_only/opt/devkitpro/

包内的libnx/switch_rules、libnx.a、真实Switch SDL2/SDL2_image头文件和AArch64静态库均已存在。只在D:/tmp创建一个指向此隔离SDK数据目录的ASCII名字Junction，供Windows路径和包配置检查使用；Windows原系统PATH、注册表和C:/msys64均不修改。

必须注意：来自社区的第三方重分发文件尚没有能够独立确认的devkitPro上游包签名；归档包内的“packager=Dave Murphy”只是包自身的文字声明，包SHA与.MTREE自校验也只能证明传输稳定和内容未意外损坏，不能证明未被篡改。因此**没有执行第三方归档中的GCC/binutils/elf2nro.exe、安装脚本、未知Windows程序，也没有将这些程序加入系统PATH**。原Windows Defender目前未启用，但系统检测到腾讯电脑管家系统防护，并不等于整个电脑无安全产品。

## 真正AArch64源代码编译（进展超越原host mock）

使用此前从官方ziglang.org稳定版下载并按官方HTTPS index SHA校验的Zig 0.15.2，读取刚获得的**真实libnx + Switch SDL2/SDL2_image目标头文件**，将工程现有四份ISO C99源代码全部成功交叉编译为e_machine=183的AArch64 ELF64 ET_REL对象：
- native_pc_hd_core.o（真PC源PNG1280×960无降级超宽图层/透明源几何）
- native_pc_movie_clock.o（原25fps MPEG1/48kHz MP2 PCM采样整数时钟）
- native_pc_png_verify.o（原13源PNG文件字节SHA256强制校验）
- native_hd_switch_sdl2_qa.o（真实目标SDL2/SDL2_image头签名，不再是fake SDL头文件）

对象位于：
07_工具链环境/2026-10-18_第三方历史devkitPro包_隔离审查/zig_real_headers_link/

已使用本机信任的readelf独立确认4个都是ELF64 AArch64可重定位格式；并用自编Python直接遍历并检查10种关键真实Switch目标静态库（libnx、SDL2、SDL2_image、EGL、glapi、drm_nouveau、PNG、JPEG、WebP、zlib）的ar头与成员ELF machine 183，共确证1276个AArch64编译对象；不执行任何第三方归档的PE程序。

独立报告：
06_测试记录/P53_18第三方SDK历史包真实Switch静态库头与四对象_AArch64_ELF架构只读验收_无NRO.json

## 链接及可信来源尚未解决的阻断

从真实目标C99对象到NRO必须包含libnx的真正链接脚本、Newlib、SDL2_image静态库的完整PNG/JPEG/WebP/Mesa依赖和合法NRO转换。第一次使用Zig尝试链接时发现Zig的链接参数与devkitA64/GNU脚本有兼容差异（--require-defined、--no-dynamic-linker等不受支持），进一步使用freestanding目标时提示无法自动提供目标libc。**这意味着尚没有成功的目标ELF链接结果，更没有可供NS安装的NRO**。

不能将四个.o改名为NRO或采用低清旧ONS冒充新版NS移植，不能无安全保障地运行未经确认来源的第三方Windows编译/转换可执行文件。离线SDK的pkg-config源.pc原始写死/opt/devkitpro路径，Windows中文路径又可能出现编码问题，因此仍需ASCII路径和隔离重定位的静态依赖校验；没有建立可用的最终目标构建环境。

所有新版PC原生1505PNG、33454原OGG、五段1280×960真正25fps MPEG1与48kHz双声道MP2、原BGI优先级和用户已安装旧NS游戏/玩家Save均未被本轮修改；主机fake SDL图层诊断仍不能代替Switch GPU输出。

正式安装及发布状态继续：BLOCKED_NOT_SAFE_TO_INSTALL。

质量日志：
06_测试记录/P53_第五十八轮_第三方SDK十八包零可执行运行与十静态库ARM64全量质量门禁.log
