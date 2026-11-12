# 第216轮 P834｜Switch 已连接，DBI MTP 的 SD 目录目前不可稳定访问

日期：2026-10-24。**设备已识别，但本轮没有在实机拷贝或运行游戏。**

## 真实连接检查

- Windows PnP：`USB\VID_057E&PID_201D\XJJ70004080667`，厂商 `Nintendo`，名称 `Switch`，`Class=WPD`，`Service=WUDFWpdMtp`，`Status=OK`，设备 `Present=True`。
- Windows Shell「此电脑」确实枚举出 `Switch`，设备根曾可见 `1: SD Card`、`5: SD Card install`、`6: NAND install`、`7: Saves`、`8: Album` 等。**只有 `1: SD Card` 属于本项目允许的资源操作范围**。不触碰安装区、NAND、系统 Saves。
- Windows 普通文件系统盘符只有 `C:` 和 `D:`，没有 Nintendo SD 盘符。P1175 是真实磁盘根路径部署工具，不能把 WPD MTP 当成 `E:` 去运行。
- 调用 Windows `Shell.Application` 进入 `1: SD Card` 的内部目录、枚举其文件和使用 `ParseName("switch")` 时发生约 18 至 22 秒超时。其后直接列举 MTP 设备根也出现 13 秒超时；WPD PnP 设备状态仍然 OK。这表明 USB 已识别，但实际 SD MTP 内容服务当前卡住/不可可靠枚举。尚无任何原版游戏资源实际复制，也无任何 NRO 已装到 Switch。

## 已完成可用的私人实机版本

- P830 已保留完整 GameOnly 原主人 1.647 SHA 固定的 `Subahibi_PC1647_HD_PRIVATE_HARDWARE_QA_NOT_VERIFIED.nro`，8,081,408B，SHA256 `80b97ecffdf87791da8fb2a91781e47be1e29ea31447f3a17c84df98d1d8f591`。
- P831 包 `Subahibi_PC1647_HD_PRIVATE_QA_NRO_ONLY_NO_GAME_MEDIA.zip`，3,579,751B，只有 NRO 和安全验证文档，**不含原商业 ARC20/CG/OGG/视频**。
- 待从原PC自有真实完整54个 ARC20 + 3344字节 IPL 共 `4,502,971,909` 字节，按 `story/` 目录布局部署，保留独立 `persistent_save_slots/`。现有完整 SHA 来源 P823 已验证。

## 当前依赖的用户物理操作

请在Switch上继续打开/重启 **DBI → Run MTP responder**，保持页面打开、USB 数据线连接、屏幕不休眠。然后在 Windows「此电脑 → Switch → 1: SD Card」试着打开 SD 根目录，确认能够看到真实文件夹（例如 `switch`、`Nintendo`、`atmosphere`）。如仍然加载不出，安全断开后重新打开 MTP responder 再连接。不应通过 `5: SD Card install` 或 `6: NAND install` 代替。

重新可以浏览后恢复工作：先安全确认真实存储路径与剩余空间，再复制原版54档+IPL到私人 `story/`，逐项校验，然后只传P830 NRO、在Homebrew Menu进行首启测试；如仅MTP可用，需使用可验证MTP复制方式，不能假设Windows文件系统盘符。**目前正式游戏实机可玩性未验收，发布仍阻塞。**
