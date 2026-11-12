# 发布包验证记录

验证时间：2026-11-12
验证对象：`story-v1` 三卷分卷（`Subahibi_HD_CHS_full_part1~3.zip`）

## 1. 分卷完整性

| 分卷 | 条目数 | 大小 | SHA256 |
|---|---|---|---|
| part1 | 3 | 1,410,918,137 B | `3b0fe6462098cfbc817d88065b9cfe0b86e54636471153b860f5d0ba0fe5b497` |
| part2 | 7 | 1,579,091,795 B | `98ca2c6cfdd8793dec23cd40f291668094d95fab7aa7b43e47871c23be5a90eb` |
| part3 | 55 | 1,543,346,073 B | `15c0e1b2db49e91e659aebd5ead12c770eab377258ed4215573296bb61e0cc3f` |

- 唯一路径总数：**65**
- 跨卷重复路径：**0**
- 解压后总字节：**4,533,344,569**（与预期完全一致）

## 2. 目录结构完整性

解压三卷到同一目录后：

| 路径 | 状态 |
|---|---|
| `switch/subahibi_pc_native_hd_qa/Subahibi_HD_CHS.nro` | OK |
| `switch/subahibi_pc_native_hd_qa/chs/dialogue_cp932_gbk.bin` | OK |
| `switch/subahibi_pc_native_hd_qa/chs/opening_narration_private_cp932_gbk_26.bin` | OK |
| `switch/subahibi_pc_native_hd_qa/chs/unvoiced_unique_voice_anchor_cp932_gbk_759.bin` | OK |
| `switch/subahibi_pc_native_hd_qa/chs/dialogue_extra.bin` | OK |
| `switch/subahibi_pc_native_hd_qa/font/NotoSansSC_wght.ttf` | OK |
| `INSTALL.md` / `GAMEPLAY.md` / `README.md` / `README-FIRST.txt` | OK |
| `switch/subahibi_pc_native_hd_qa/story/`（55 个文件） | OK |

## 3. 与实机安装逐字节比对

把三卷解压后，与设备上正在运行的安装目录比对（文件名 + 大小）：

| 文件 | 设备端 | 包内 | 结果 |
|---|---|---|---|
| `Subahibi_HD_CHS.nro` | 8,178,787 | 8,178,787 | 一致 |
| `chs/dialogue_cp932_gbk.bin` | 3,267,477 | 3,267,477 | 一致 |
| `chs/opening_narration_private_cp932_gbk_26.bin` | 2,090 | 2,090 | 一致 |
| `chs/unvoiced_unique_voice_anchor_cp932_gbk_759.bin` | 80,307 | 80,307 | 一致 |
| `chs/dialogue_extra.bin` | 1,055,681 | 1,055,681 | 一致 |
| `font/NotoSansSC_wght.ttf` | 17,772,300 | 17,772,300 | 一致 |
| `story/` 55 个文件 | 55 个 | 55 个 | 名称与大小全一致 |

**结论：包内容与实机可用安装完全一致，无缺失、无多余、无尺寸偏差。**

## 4. 关键文件 SHA256

| 文件 | SHA256 | 状态 |
|---|---|---|
| `Subahibi_HD_CHS.nro` | `7c000e75ae8de57dee987b3a8108262deaea91a53fb5250b04b7d2767e78670f` | MATCH |
| `dialogue_extra.bin` | `5b161585d1b744ed254291575b08f597194c45d0b12de05676a690b40489bc5e` | MATCH |
| `NotoSansSC_wght.ttf` | `a3041811a78c361b1de50f953c805e0244951c21c5bd412f7232ef0d899af0da` | MATCH |

## 5. 解压耗时

存储模式（无压缩）解压三卷共 4.5 GB：**约 5.6 秒**（SSD）。

## 6. 关于 `story/` 里的非 arc 文件

`story/` 下 55 个文件中有 54 个 `*.arc` 加一个 **`ipl._bp`（3,344 B）**——这是原 BGI 引擎的 IPL 字节码，**必需**，不是误放的杂项。早期移植轮次里它的 SHA256 校验是启动前的硬性检查之一。

## 7. 已知前置条件

- 启动方式：hbmenu → 素晴日 HD 汉化版 → A
- `UserData/`、`persistent_save_slots/` 由程序首次启动自动创建，包内不含（属于用户数据）
- 字体文件名与尺寸写死在引擎里，不可替换
