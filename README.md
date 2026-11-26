> ## ⚠️ 启动方式（必读）
>
> **必须「按住 R 键 + 点任意已安装游戏」进入 hbmenu，不要从相册（Album）进。**
>
> | 进入方式 | 可用内存 | 结果 |
> |---|---|---|
> | 相册 → hbmenu | 约 400 MB（applet） | 加载第一张位图时分配失败：黑屏退回或崩溃（2168-0001） |
> | 按住 R → hbmenu | 约 3 GB（title override） | 正常进入游戏 |
>
> 日志特征：`P941 REAL_VM_MODULE_CHANGE [t1 count2 topbitmap._bp]` 之后崩溃。
>
> 另外：游戏目录下的 `locks`、`UserData`（含 `SubarashikihibiHD`）、`persistent_save_slots`
> 三个目录必须存在，引擎不会自动创建。缺了会启动被拒或初始化崩溃，可用包内 `清锁.bat` 修复。

# 素晴日 HD Switch 简体中文移植 · 完整版

> **本分支 = 完整版（原版内容 + 全量汉化）**。和谐版见 `clean` 分支与 Release ②。

## 安装（推荐）

下载 Release **①【完整版】完整安装包（三卷，独立目录）**，三卷解压后把 `switch/` 复制到 SD 卡根目录即可，一次装完。

安装后目录：

```
switch/subahibi_pc_native_hd_qa/
├─ Subahibi_HD_CHS.nro        主程序（hbmenu 显示：素晴日 HD 汉化版）
├─ chs/                        4 个词典（基线 34,974 条 + 覆盖层 13,715 条）
├─ font/NotoSansSC_wght.ttf
└─ story/                      54 个 data*.arc + ipl._bp
```

## Release 一览

| 序号 | Tag | 用途 |
|---|---|---|
| ① | `v1.1-full-standalone` | **完整安装包（三卷）——推荐** |
| ② | `v2.1-clean-standalone` | 和谐版完整安装包（三卷），装在 `subahibi_clean_hd_qa_chs/`，可与本版共存 |
| ③ | `v1.0.0` | 仅程序与词典，用于后续小幅更新 |
| — | `story-v1` | 旧素材分卷，内容已含在 ① |

## 数据目录

完整版读 `sdmc:/switch/subahibi_pc_native_hd_qa/`；和谐版读 `sdmc:/switch/subahibi_clean_hd_qa_chs/`。两套目录独立，可同时安装，存档各自独立。

## 汉化情况

- 覆盖率 **99.60%**（61,291 / 61,539 条消息）
- 角色名与正文分开处理（名盘 CP932、正文 GBK）
- 15 条超长文本受引擎 512 字节字段限制未能覆盖

---

## 安装流程（两个版本完全一致）

1. 三个分卷**全部下载**到同一目录
2. 逐个解压到**同一个位置**（提示合并时选「是」）
3. 把解压出的 `switch` 文件夹整个复制到 SD 卡根目录
4. 插卡开机 → hbmenu → 选对应入口 → A 启动

首次启动自动创建 `UserData/` 与 `persistent_save_slots/`。

---

## 法律声明

引擎为 OpenBGI（GPL-2.0）。游戏素材版权归 KeroQ 所有，仅存放于私有 Release，**仅供本人使用，禁止分发**。汉化文本为二次创作，仅供已购买正版的玩家使用。

## 已知问题

**X 键「回想 / 履历」界面文字为乱码。**

- 正文、菜单、存档界面均正常，仅历览界面受影响
- 原因：引擎历览缓冲区保存脚本原文（CP932），与汉化后的解码方式不匹配，属引擎设计结果
- 修复需重新编译 NRO 或二进制补丁，均需真机动态验证，当前版本未包含
- 不影响存档、剧情推进与和谐版内容屏蔽
