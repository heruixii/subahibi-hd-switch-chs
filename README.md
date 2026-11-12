# 素晴日 HD 简体中文移植（Switch）

把 PC 版《素晴らしき日々 ～不連続存在～ 全语音 HD 版》移植到 Nintendo Switch（自制程序环境），并完成简体中文本地化。

> 仓库内只有源码、脚本、文档与汉化数据；**游戏素材 `story/` 放在私有 Release**（`story-v1`），版权归 KeroQ，仅供本人使用。

---

## 下载

| Release | 文件 | 大小 | 用途 |
|---|---|---|---|
| **story-v1** | `Subahibi_HD_CHS_full_part1~3.zip` | 共 4,533,344,569 B | **推荐，一次到位**：程序 + 四份词典 + 字体 + 游戏素材 + 三份说明，解压即得完整安装树 |
| v1.0.0 | `Subahibi_HD_CHS_v1.0.0_full.zip` | 17,122,088 B | 仅程序 + 词典 + 字体（已有素材时用） |
| v1.0.0 | `Subahibi_HD_CHS.nro` | 8,178,787 B | 仅主程序 |
| v1.0.0 | `dialogue_extra.bin` | 1,055,681 B | 仅更新汉化文本（不影响存档） |

**story-v1** 的三卷分卷里已经是完整安装树（程序 + 四份词典 + 字体 + `story/` 55 个原版 `data*.arc` + `INSTALL.md` / `GAMEPLAY.md` / `README-FIRST.txt`），解压到 SD 卡即可玩。`v1.0.0` 保留给「已有素材、只想更新程序或译文」的场景。

下载页：[v1.0.0](https://github.com/heruixii/subahibi-hd-switch-chs/releases/tag/v1.0.0) ｜ [story-v1](https://github.com/heruixii/subahibi-hd-switch-chs/releases/tag/story-v1)

---

## 游戏素材（私有 Release）

完整安装树放在 **story-v1** 的三卷分卷里（4.53 GB，65 个文件）：

| 分卷 | 大小 | SHA256 |
|---|---|---|
| `Subahibi_HD_CHS_full_part1.zip` | 1,410,918,137 B | `3b0fe646…0fe5b497` |
| `Subahibi_HD_CHS_full_part2.zip` | 1,579,091,795 B | `98ca2c6c…be5a90eb` |
| `Subahibi_HD_CHS_full_part3.zip` | 1,543,346,073 B | `15c0e1b2…61e0cc3f` |

解压后得到 `switch/subahibi_pc_native_hd_qa/`（程序 + `chs/` 四份词典 + `font/` + `story/`）以及 `INSTALL.md`、`GAMEPLAY.md`、`README.md`、`README-FIRST.txt`。

> 素材版权归 KeroQ 所有，**仅供本人使用，禁止分发**；因此放在私有仓库的 Release 里。

---

## 文档

| 文件 | 内容 |
|---|---|
| [`INSTALL.md`](INSTALL.md) | **安装教程**：完整包结构、`story/` 准备、逐步安装、首次启动自检、字体硬性要求、校验值 |
| [`GAMEPLAY.md`](GAMEPLAY.md) | **操作教程**：完整按键对照表、光标使用与精瞄、存读档流程、设置菜单、故障排查 |
| [`RELEASE-VERIFY.md`](RELEASE-VERIFY.md) | **发布包验证记录**：三卷完整性、目录结构、与实机安装逐字节比对、SHA256 |

---

## 当前状态

| 项 | 状态 |
|---|---|
| 版本 | 1.0.0（2026-11-12） |
| 平台 | Switch，Atmosphere 1.11.0 / 固件 22.0.0（emuMMC 实测） |
| 启动方式 | hbmenu 启动 NRO（已显示图标 / 名称 / 发布者） |
| 汉化覆盖 | 61,291 / 61,539 条消息 = **99.60%**；可译范围内 100% |
| 覆盖层条目 | 13,715 条 |
| 残留错误率 | 0.34%（295 条同口径抽样，1 条错） |
| 存读档 | 正常 |
| 光标 | 桌面箭头样式，1× 尺寸，带平滑跟随 |

---

## 特性

### 汉化

- **文本规模**：13,715 条词条覆盖 99.60% 的消息
- **编码方案**：正文走 GBK（CP936），说话人名名牌走 CP932，由运行时开关 `P546_ChineseLegacyMode` 切换
- **字典栈**：设备上 `chs/` 四个文件叠加

  | 文件 | 条目 | 用途 |
  |---|---|---|
  | `dialogue_cp932_gbk.bin` | 34,974 | 基线词典（`SBCHS001`） |
  | `opening_narration_private_cp932_gbk_26.bin` | 26 | 开场旁白 |
  | `unvoiced_unique_voice_anchor_cp932_gbk_759.bin` | 759 | 无语音锚点 |
  | `dialogue_extra.bin` | 13,715 | **本项目的覆盖层**（`SBCHS004`） |

- **质量方法**：全量逐条复审 3 轮 + 随机抽样审计（严口径），累计修正 1,450+ 条

### 字体

引擎只接受固定的一份字体，位置与尺寸都写死：

```
sdmc:/switch/subahibi_pc_native_hd_qa/font/NotoSansSC_wght.ttf
必须恰好 17,772,300 B
SHA256 a3041811a78c361b1de50f953c805e0244951c21c5bd412f7232ef0d899af0da
```

Noto Sans SC，SIL Open Font License 1.1，允许再分发。

### 光标

原版移植的准星改成桌面箭头：

- 12×19 位图，黑描边 + 白填充（白底和深色 CG 上都可见）
- 热点在箭尖，与点击命中点一致
- **限速跟随**：每帧最多移动 9 px 且不小于 0.75 px，抵消低帧率下的整数步进顿挫
- 位移超过 48 px（脚本把光标跳到菜单）时直接吸附，不拖影
- 绘制在输出层，不写进 1280×960 游戏纹理

### 图标与名称

NRO 尾部追加 `ASET` 段（结构依据官方 switchbrew `elf2nro.c`）：

```
[原 NRO 数据] [4 字节对齐] [ASET 头 56 B] [icon 35,883 B] [control.nacp 16,384 B]
```

- 名称：素晴日 HD 汉化版
- 发布者：ALTIRKIE
- 版本：1.0.0
- 图标：256×256 JPEG

---

## 目录结构

完整包解压后：

```
switch/subahibi_pc_native_hd_qa/
├─ README-FIRST.txt                                  快速上手说明
├─ Subahibi_HD_CHS.nro                               主程序
├─ chs/
│  ├─ dialogue_cp932_gbk.bin                         基线词典 34,974 条
│  ├─ opening_narration_private_cp932_gbk_26.bin     开场旁白 26 条
│  ├─ unvoiced_unique_voice_anchor_cp932_gbk_759.bin 无语音锚点 759 条
│  └─ dialogue_extra.bin                             汉化覆盖层 13,715 条
└─ font/
   └─ NotoSansSC_wght.ttf                            中文字体
```

还需要自己放入：

```
switch/subahibi_pc_native_hd_qa/story/   游戏剧本与资源（自备）
```

---

## 构建

### 工具链

| 组件 | 版本 |
|---|---|
| 编译器 | Zig 0.15.2（`-target aarch64-freestanding-none`） |
| 链接器 | devkitA64 GNU ld（Switch specs） |
| 运行库 | libnx + SDL2 + EGL/GLES2 |
| NRO 转换 | 官方 switchbrew `elf2nro` 算法 |

### 一条重要的坑：mingw 工具链写不了中文路径

`msys64` 的 gcc/ld **无法把输出写到含中日韩字符的目录**：

```
$ gcc t.c -o "D:\tmp\中文\p.exe"
ld.exe: cannot open output file D:\tmp\中文\p.exe: No such file or directory
```

本仓库的 `tools/dsh_build_shim.py` 在调用层解决这个问题：拦截 `subprocess`，把 `-o <含中文路径>` 改写为 ASCII 暂存路径，编译成功后再用 Python 复制回原位置。读取中文路径本身正常，只有写入有问题。

```python
import dsh_build_shim          # 装上补丁
import <构建模块>; <构建模块>.main()
```

`tools/run_build.py` 就是带 shim 的运行入口。

### 构建步骤

1. 准备 OpenBGI 引擎源码（GPL-2.0）与 libnx / SDL2 / devkitA64
2. 应用 `engine/` 下的补丁（光标绘制等）
3. 依序重建对象 → GNU 链接 → `elf2nro` 转 NRO
4. 需要时用 `tools/p1492_add_aset_current.py` 追加图标与名称

> 完整链路涉及两百余个目标文件与多轮门禁校验，工程脚本未全部收录；`docs/` 下有每轮的详细记录。

---

## 汉化数据格式

覆盖层 `dialogue_extra.bin`：

```
偏移 0x00: "SBCHS004"        魔数
其后:      u32 条目数
每条:      u16 key_len, key（CP932 原文）, u16 val_len, val（GBK 译文）
```

字段上限 512 字节（含 `\n` 转义的 2 字节），超长条目无法写入引擎。

`translation/manual_pairs.tsv` 是权威修正表（12,424 行），`translation/overlay_manual5.tsv` 是合并后的最终 13,715 条。

### 校验与构建脚本

| 脚本 | 作用 |
|---|---|
| `tools/prune_pairs.py` | 按转义后长度裁剪超限条目 |
| `tools/merge_overlay5.py` | 合并修正表与基线，生成最终覆盖层源 |
| `tools/check_integrity.py` | 校验每条修正都真正落进覆盖层 |
| `tools/make_audit.py` / `tools/build_weighted.py` | 按权重抽样，供审计使用 |
| `tools/coverage_m20.py` | 覆盖率统计 |
| `tools/apply_fixes.py` | 批量应用修正，含长度/缩进/转义一致性校验 |

---

## 已知限制

| 限制 | 数量 | 说明 |
|---|---|---|
| 成人向场景正文未译 | 158 | 内容边界，不在本移植范围内 |
| 说话人名未译 | 48 | 名牌走 CP932 通路，改动会导致乱码 |
| 单条超过 512 字节 | 33 | 引擎字段上限 |
| GBK 不可编码字符 | 9 | `・` `♪` `∀` `∃` `⇔` `☆`、半角假名等 |
| 触屏输入 | — | 未实现；光标仅支持右摇杆（ZL 精瞄） |
| 主页磁贴 | — | forwarder NSP 在 AMS 22.0.0 上无法启动，已放弃；仅支持 hbmenu 启动 |

### 关于主页磁贴

尝试过 forwarder NSP（Nro2Nsp 3.3.5 / 3.3.6 Beta4，8 种构建组合：不同 Title ID 段、npdm、keygen、plaintext、NRO 封装），全部失败：

- 症状演进：`无法启动软件` → `一直加载` → `黑屏` → `关闭卡死需强制断电`
- 已排除：签名补丁缺失（sys-patch 日志显示 es/fs/ldr 全部 Patched）、缺 ticket、keygen 不匹配、NRO 格式异常、安装位置
- 结论：Nro2Nsp 这一代 forwarder 依赖的 hbloader 链式加载在 AMS 22.0.0 上不工作

详见 `docs/2026-11-12_第323轮_主页磁贴八次构建与结论.md`。

---

## 目录结构（仓库）

```
docs/          每轮开发记录与结论（287 篇）
tools/         字典构建、校验、抽样、构建 shim、ASET 追加
translation/   权威修正表、最终覆盖层源与二进制
engine/        引擎侧补丁（光标绘制等）
```

---

## 法律声明

- **引擎**：OpenBGI，GPL-2.0。本仓库只提供补丁与构建说明，不重分发引擎源码；如需构建请从上游获取。
- **游戏素材**：《素晴らしき日々》的剧本、图像、音频版权归 KeroQ 所有，本仓库与发布包**不含任何游戏素材**。
- **字体**：Noto Sans SC，SIL Open Font License 1.1，允许随包再分发。
- **汉化文本**：本项目的译文为二次创作，仅供已购买正版游戏的玩家在自制程序环境使用。请勿用于商业用途。
- **使用风险**：自制程序环境下的操作风险自负；本移植不含任何绕过正版校验的功能。

---

## 致谢

- OpenBGI 引擎作者与 GPL-2.0 社区
- libnx / devkitPro / SDL2
- 上游汉化组的既有人名与术语参考
