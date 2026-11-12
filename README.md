# 素晴日 HD 简体中文移植（Switch）

把 PC 版《素晴らしき日々 ～不連続存在～ 全语音 HD 版》移植到 Nintendo Switch（自制程序环境），并完成简体中文本地化。

> **本仓库不包含任何游戏素材。** 引擎源码、图像、音频、剧本原文均不在本仓库内；使用前请自备正版游戏。

---

## 当前状态

| 项 | 状态 |
|---|---|
| 版本 | 1.0.0（2026-11-12） |
| 平台 | Switch，Atmosphere 1.11.0 / 固件 22.0.0（emuMMC 实测） |
| 启动方式 | hbmenu 启动 NRO（已在 hbmenu 显示图标 / 名称 / 发布者） |
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

## 安装

SD 卡目录结构：

```
sdmc:/
└─ switch/
   └─ subahibi_pc_native_hd_qa/
      ├─ Subahibi_HD_CHS.nro        ← 主程序（含图标与名称）
      ├─ chs/
      │  ├─ dialogue_cp932_gbk.bin
      │  ├─ opening_narration_private_cp932_gbk_26.bin
      │  ├─ unvoiced_unique_voice_anchor_cp932_gbk_759.bin
      │  └─ dialogue_extra.bin      ← 本项目的汉化覆盖层
      ├─ story/                     ← 游戏剧本与资源（需自行从正版提取）
      ├─ font/                      ← 字体
      ├─ UserData/                  ← 存档
      └─ persistent_save_slots/
```

**启动**：hbmenu → 选「素晴日 HD 汉化版」→ 进入。

存档位于 `UserData/` 与 `persistent_save_slots/`，升级覆盖层不影响存档。

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

本仓库的 `tools/dsh_build_shim.py` 在调用层解决这个问题：拦截 `subprocess`，把 `-o <含中文路径>` 改写为 ASCII 暂存路径，编译成功后再用 Python 复制回原位置。读取中文路径本身是正常的，只有写入有问题。

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

## 目录结构

```
docs/          每轮开发记录与结论（287 篇）
tools/         字典构建、校验、抽样、构建 shim
translation/   权威修正表、最终覆盖层源与二进制
engine/        引擎侧补丁（光标绘制等）
```

---

## 法律声明

- **引擎**：OpenBGI，GPL-2.0。本仓库只提供补丁与构建说明，不重分发引擎源码；如需构建请从上游获取。
- **游戏素材**：《素晴らしき日々》的剧本、图像、音频版权归 KeroQ 所有，本仓库**不含任何素材**。
- **汉化文本**：本项目的译文为二次创作，仅供已购买正版游戏的玩家在自制程序环境使用。请勿用于商业用途。
- **使用风险**：自制程序环境下的操作风险自负；本移植不含任何绕过正版校验的功能。

---

## 致谢

- OpenBGI 引擎作者与 GPL-2.0 社区
- libnx / devkitPro / SDL2
- 上游汉化组的既有人名与术语参考

---

## 文档

| 文件 | 内容 |
|---|---|
| [INSTALL.md](INSTALL.md) | **安装教程**：必备文件清单、目录结构、逐步安装、升级卸载、常见问题、校验值 |
| [GAMEPLAY.md](GAMEPLAY.md) | **操作教程**：完整按键对照表、光标使用、存读档流程、设置菜单、故障排查 |

> ⚠️ **本发布包不能开箱即玩。** Release 内只有主程序与汉化覆盖层；story/ 游戏资源、chs/ 三份基线词典、ont/ 中文字体需自行准备，详见 INSTALL.md 第一节。
