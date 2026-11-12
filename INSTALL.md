# 安装教程

> ⚠️ **18+ 年龄限制**
>
> 本作原版是成人向作品，游戏素材中包含成人向场景。本项目**不翻译**这些场景的正文，
> 但它们仍随游戏资源存在于本包内。**未满 18 岁请勿使用。**


> **能玩到什么程度**
>
> 下载 **完整包 `Subahibi_HD_CHS_v1.0.0_full.zip`（17 MB）**，解压后覆盖到 SD 卡，再放进你自己的 `story/` 目录，就能直接玩。
>
> **推荐直接下载 `story-v1` 的三卷分卷**——里面已经是完整安装树（程序 + 四份词典 + 字体 + `story/` + 三份说明），解压到 SD 卡就能玩。
>
> `v1.0.0` 只适合「已有素材、想单独更新程序或汉化文本」的场景。


## 两个版本

| 版本 | 内容 | 获取 |
|---|---|---|
| **完整版** | 原版内容 + 全量汉化（99.60%） | Release `v1.0.0`：`Subahibi_HD_CHS_v1.0.0_full.zip`（程序+词典+字体）<br>Release `story-v1`：游戏素材三卷分卷 |
| **和谐版（屏蔽指定 CG 与语音）** | 同程序与汉化，另含：成人向场景正文改为占位句、**210 张指定 CG 替换为纯黑帧**、**248 条对应语音替换为静音** | Release `v2.0-clean`：`dialogue_extra_clean.bin` + 13 个改写归档（1.71 GB） |

**两个版本共用同一个 NRO**，只替换 `chs/` 与 `story/` 下的数据文件；切换即改文件，不需要重装或换程序。

> 和谐版（屏蔽指定 CG 与语音）的改写方式是**原地覆盖**：归档结构、条目数、偏移与文件大小全部与原版一致，只把目标条目的数据换成黑帧/静音，并把该条目的 `size` 改小。

### 和谐版（屏蔽指定 CG 与语音）安装

1. `dialogue_extra_clean.bin` → 改名为 `dialogue_extra.bin`，覆盖到 `chs/`
2. Release `v2.0-clean` 里的 13 个 `.arc` → 覆盖到 `story/`
3. 启动方式不变

**切回完整版**：13 个 arc 换回原版，`chs/dialogue_extra.bin` 换回完整版覆盖层（1,055,681 B）。

---
---

## 一、下载哪个

| Release | 文件 | 大小 | 用途 |
|---|---|---|---|
| **story-v1** | `Subahibi_HD_CHS_full_part1~3.zip` | 共 4,533,344,569 B | **推荐，一次到位**：程序 + 四份词典 + 字体 + 游戏素材 + 三份说明，解压即得完整安装树 |
| v1.0.0 | `Subahibi_HD_CHS_v1.0.0_full.zip` | 17,122,088 B | 仅程序 + 词典 + 字体（已有素材时用） |
| v1.0.0 | `Subahibi_HD_CHS.nro` | 8,178,787 B | 仅主程序 |
| v1.0.0 | `dialogue_extra.bin` | 1,055,681 B | 仅更新汉化文本（不影响存档） |

完整包内的目录结构：

```
switch/subahibi_pc_native_hd_qa/
├─ README-FIRST.txt                                  快速上手说明
├─ Subahibi_HD_CHS.nro                               主程序（内嵌图标与名称）
├─ chs/
│  ├─ dialogue_cp932_gbk.bin                         基线词典 34,974 条      3,267,477 B
│  ├─ opening_narration_private_cp932_gbk_26.bin     开场旁白 26 条               2,090 B
│  ├─ unvoiced_unique_voice_anchor_cp932_gbk_759.bin 无语音锚点 759 条            80,307 B
│  └─ dialogue_extra.bin                             汉化覆盖层 13,715 条      1,055,681 B
└─ font/
   └─ NotoSansSC_wght.ttf                            中文字体              17,772,300 B
```

---

## 二、完整分卷（含游戏素材）

story/ 是 55 个原版 data*.arc，合计 **4,502,971,909 B（4.29 GB）**，不随仓库提交，放在私有 Release：

<https://github.com/heruixii/subahibi-hd-switch-chs/releases/tag/story-v1>

### 还原

| 分卷 | 大小 | SHA256 |
|---|---|---|
| story_vol1.zip | 1,410,917,945 B | 32ca02709ce9a56e7ece9ae3dc075d208a01b62629498434090121c9327d96f2 |
| story_vol2.zip | 1,579,091,347 B | 48bf56dfc3b0a3ec0a3dc3662c9988ffa1f687ff47a12b8ddeaebb6b90bf055a |
| story_vol3.zip | 1,512,968,923 B | 8912dbea41ee8fbe0c4c5629541156fdc2b7f7049008b6188b47d4585a22886a |

三个分卷**解压到同一个目录**（zip 为存储模式，无压缩），得到：

`
story/
├─ data01000.arc
├─ data01101.arc
├─ ...
└─ data05010.arc      （共 55 个）
`

放到：

`
sdmc:/switch/subahibi_pc_native_hd_qa/story/
`

> 素材版权归 KeroQ 所有，仅供本人使用，禁止分发。

---

## 三、安装步骤

1. SD 卡格式化为 exFAT（推荐）或 FAT32
2. 解压 `Subahibi_HD_CHS_v1.0.0_full.zip`
3. 把里面的 `switch` 文件夹整个复制到 SD 卡根目录（已有同名目录则合并）
4. 把你自备的 `story/` 放进 `sdmc:/switch/subahibi_pc_native_hd_qa/story/`
5. 插卡开机 → 进 **hbmenu**
6. 列表里出现 **素晴日 HD 汉化版 / ALTIRKIE / 1.0.0**（带封面图标）
7. 按 **A** 启动

首次启动会自动创建 `UserData/` 与 `persistent_save_slots/`。

---

## 四、首次启动检查

| 现象 | 说明 |
|---|---|
| 标题画面出现，菜单是中文 | 正常 |
| 文字显示为方块 | `font/NotoSansSC_wght.ttf` 缺失或尺寸不对（必须恰好 17,772,300 B） |
| 报错退出、提示找不到文件 | `story/` 路径不对，检查是否放到了 `subahibi_pc_native_hd_qa/story/` |
| 全程日文 | `chs/dialogue_extra.bin` 没放对位置（应在 `chs/` 下） |

### 字体是硬性要求

引擎只接受这一份字体，位置和尺寸都固定：

```
sdmc:/switch/subahibi_pc_native_hd_qa/font/NotoSansSC_wght.ttf
大小必须 17,772,300 B
SHA256 a3041811a78c361b1de50f953c805e0244951c21c5bd412f7232ef0d899af0da
```

换别的字体会被拒绝加载。该字体为 Noto Sans SC，SIL Open Font License 1.1，允许再分发。

---

## 五、升级与卸载

### 只更新汉化文本

替换 `chs/dialogue_extra.bin` 即可，**不需要重装 NRO，不影响存档**。

### 更新主程序

直接覆盖 `Subahibi_HD_CHS.nro`。

### 卸载

删除整个 `switch/subahibi_pc_native_hd_qa/` 目录。存档在 `UserData/` 与 `persistent_save_slots/` 内，需要保留请先备份这两个目录。

---

## 六、常见问题

**Q：能不能装到系统主页，像正常游戏一样点图标启动？**
不能。forwarder NSP 在 Atmosphere 22.0.0 上无法启动，试过 8 种构建组合全部失败，详见 `docs/2026-11-12_第323轮_主页磁贴八次构建与结论.md`。只能从 hbmenu 启动。

**Q：能不能触屏操作？**
不能。光标只支持右摇杆（按住 ZL 进精瞄档）。触屏方案做过设计但未实现，见 `docs/2026-11-12_第324轮_触屏直点方案计划.md`。

**Q：画质和 PC 版一样吗？**
原版 1280×960 资源按 4:3 输出，未拉宽变形。

**Q：存档怎么迁移？**
把 `UserData/` 与 `persistent_save_slots/` 两个目录整体拷走即可。

**Q：为什么有些句子还是日文？**
成人向场景 158 条、说话人名 48 条、单条超 512 字节 33 条、GBK 不可编码 9 条不在范围内，合计 248 条，占 0.40%。

**Q：光标移动一顿一顿的？**
由渲染帧率决定，光标每帧只能更新一次。移植层做了限速平滑（每帧最多 9 px、最少 0.75 px），能消除忽快忽慢，但无法超过帧率本身的上限。

---

## 七、校验值

```
Subahibi_HD_CHS.nro             8,178,787 B
  7c000e75ae8de57dee987b3a8108262deaea91a53fb5250b04b7d2767e78670f
dialogue_extra.bin              1,055,681 B
  5b161585d1b744ed254291575b08f597194c45d0b12de05676a690b40489bc5e
dialogue_cp932_gbk.bin          3,267,477 B
opening_narration_private_cp932_gbk_26.bin   2,090 B
unvoiced_unique_voice_anchor_cp932_gbk_759.bin  80,307 B
NotoSansSC_wght.ttf            17,772,300 B
  a3041811a78c361b1de50f953c805e0244951c21c5bd412f7232ef0d899af0da
```

完整包 zip（17,122,088 B）SHA256：

```
04b4c2f59a5b35978a9e6bf7b691a968927fdc06c4985015f7dc4fa70f482009
```
