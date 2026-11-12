# 安装教程

> **先说清楚：本发布包不能开箱即玩。**
>
> Release 里只有两个文件（主程序 NRO + 汉化覆盖层）。一套能跑的安装还需要 **游戏素材 `story/`**、**基线词典 `chs/dialogue_cp932_gbk.bin`** 和 **中文字体 `font/`**，这三样都不在本发布内，需要你自己准备。

---

## 一、你需要准备什么

| 必需项 | 来源 | 是否在本发布内 |
|---|---|---|
| 正版 PC 版《素晴らしき日々 全语音 HD 版》 | 自行购买 | ❌ 需自备 |
| `Subahibi_HD_CHS.nro` | 本 Release | ✅ |
| `dialogue_extra.bin`（汉化覆盖层） | 本 Release | ✅ |
| `story/` 游戏剧本与资源 | 从正版 `*.arc` 提取 | ❌ |
| `chs/dialogue_cp932_gbk.bin`（基线词典 34,974 条） | 由旧汉化版 + 原剧本生成 | ❌ |
| `chs/*_26.bin`、`chs/*_759.bin` 两个侧车词典 | 由原剧本生成 | ❌ |
| `font/` 中文字体 | Noto Sans SC（OFL 许可，可自由分发）或游戏自带字体 | ❌ |
| SD 卡（exFAT 或 FAT32） | — | — |
| hbmenu 自制程序环境 | Atmosphere | ❌ |

> 基线词典和侧车词典是用旧汉化版的译文与原版剧本对齐生成的，属于二次创作产物；生成脚本见仓库 `tools/` 与 `docs/` 中的记录。**这两份词典不随发布提供。**

---

## 二、目录结构

把文件放到 SD 卡的同一目录下，**目录名不能改**：

```
sdmc:/
└─ switch/
   └─ subahibi_pc_native_hd_qa/
      ├─ Subahibi_HD_CHS.nro                          ← 发布包
      ├─ chs/
      │  ├─ dialogue_cp932_gbk.bin                    ← 需自备（基线，34,974 条）
      │  ├─ opening_narration_private_cp932_gbk_26.bin ← 需自备（26 条）
      │  ├─ unvoiced_unique_voice_anchor_cp932_gbk_759.bin ← 需自备（759 条）
      │  └─ dialogue_extra.bin                        ← 发布包（13,715 条）
      ├─ story/                                       ← 需自备（游戏资源）
      ├─ font/                                        ← 需自备（字体）
      ├─ UserData/                                    ← 自动创建（存档）
      └─ persistent_save_slots/                       ← 自动创建（存档槽）
```

### 关于 `story/`

里面是提取出来的剧本文件（`.bsd`）与资源索引，来自正版游戏的 `data*.arc`。本移植**不提供提取器之外的任何素材**。提取与转换流程见 `docs/` 中 2026-10 各轮的记录。

---

## 三、安装步骤

1. **格式化 SD 卡**为 exFAT（推荐）或 FAT32
2. 建立目录 `sdmc:/switch/subahibi_pc_native_hd_qa/`
3. 把 `Subahibi_HD_CHS.nro` 放进去
4. 建子目录 `chs/`，放入你自备的三份词典 + 本发布的 `dialogue_extra.bin`
5. 建子目录 `story/`、`font/`，放入自备资源
6. 插卡开机，进 **hbmenu**
7. 列表里应出现一项：**素晴日 HD 汉化版 / ALTIRKIE / 1.0.0**，带封面图标
8. 按 A 启动

---

## 四、首次启动检查

| 现象 | 说明 |
|---|---|
| 进入标题画面，菜单为中文 | 正常 |
| 文字是方块 / 乱码 | `font/` 缺失或字体不含中文字形 |
| 报错退出、提示找不到文件 | `story/` 或 `chs/` 路径不对，检查目录名 |
| 全程日文 | `chs/dialogue_extra.bin` 没放对位置（应在 `chs/` 下，不是根目录） |

第一次启动会自动创建 `UserData/` 和 `persistent_save_slots/`。

---

## 五、升级与卸载

### 只更新汉化

`dialogue_extra.bin` 单独替换即可，**不需要重装 NRO，不影响存档**：

```
删除：chs/dialogue_extra.bin
放入：新版 dialogue_extra.bin
```

### 更新主程序

直接覆盖 `Subahibi_HD_CHS.nro`。

### 卸载

删掉整个 `switch/subahibi_pc_native_hd_qa/` 目录。存档在 `UserData/` 与 `persistent_save_slots/` 内，如需保留请先备份这两个目录。

---

## 六、常见问题

**Q：能不能装到系统主页，像正常游戏一样点图标启动？**
不能。forwarder NSP 在 Atmosphere 22.0.0 上无法启动，试过 8 种构建组合全部失败，详见 `docs/2026-11-12_第323轮_主页磁贴八次构建与结论.md`。只能从 hbmenu 启动。

**Q：能不能触屏操作？**
不能。光标只支持右摇杆（按住 ZL 进入精瞄低速档）。触屏方案做过设计但未实现，见 `docs/2026-11-12_第324轮_触屏直点方案计划.md`。

**Q：画质和 PC 版一样吗？**
原版 1280×960 资源按 4:3 比例输出，未做拉宽变形。

**Q：存档在哪？换机器怎么迁移？**
`UserData/` 与 `persistent_save_slots/` 两个目录整体拷走即可。

**Q：为什么有些句子还是日文？**
成人向场景（158 条）、说话人名（48 条）、单条超 512 字节（33 条）、GBK 不可编码字符（9 条）不在汉化范围内，合计 248 条，占 0.40%。

---

## 七、校验

安装后可比对文件大小：

```
Subahibi_HD_CHS.nro     8,178,787 B
dialogue_extra.bin      1,055,681 B
```

SHA256：

```
Subahibi_HD_CHS.nro   7c000e75ae8de57dee987b3a8108262deaea91a53fb5250b04b7d2767e78670f
dialogue_extra.bin    5b161585d1b744ed254291575b08f597194c45d0b12de05676a690b40489bc5e
```
