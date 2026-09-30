# 2026-09-30 指示詞拆分

## 來源與範圍

- 使用者提供的 16 節完整合作指示，與當時本機 Codex 全域 AGENTS.md 位元組相同。
- 原文保存於 [歷史檔](../archive/original-2026-09-30.md)，共 41,978 bytes；SHA-256：`def91c5512b3ae5a79380eb1d38501c5394461137f0fb56a9ac9296b8a67ad9a`。
- repo 起始 commit：`1ae5f2745eef1444cea5c9fde04f2abe885c8650`；原文基準 commit：`8193e2c0cddbedd9a80412b761309422aed61fa6`。
- 本次授權：整理詳細規則、精簡 Codex 指示、版本控制與推送，最後更新 Codex 指示。PR 合併與清理需依另行明確授權，不能把本記錄當成授權擴張。
- 歷史檔僅供比對。現行規則由核心及四份 guides 組成，不能因讀歷史檔而恢復已取代的預設。

## 已確認的行為變更

使用者於本次對話確認：「採用這兩項調整，其餘授權與角色限制保留」。對應問題為：

1. 單一、明確且無跨 task 相依的工作，可由 main 直接交付 task；已指定 orchestrate 時仍沿用。
2. 新建的例行調度或機械處理工作，可依難度選 Medium，其他主要工作維持 High。

第一項只增加精簡路徑，不授權 main 實作、建立未授權 task 或繞過已指定 orchestrate。第二項只調整新建配置，不切換現有對話設定、不自動授權新任務。

其餘以重組、合併重複及按需載入為主；保留建立任務、Git、部署、外部資源、批准、資料與服務保護界線。固定 commit 快照是避免來源工作分支改動影響生效規則的安裝方式，不改合作權限。

## 原章節對應

| 原章節 | 新位置與保留要點 |
|---|---|
| 1 合作目標 | [核心](../instructions/codex.md)；繁中、總交付成本、品質、自主範圍與討論不等於執行授權 |
| 2 人類入口與授權傳遞 | [合作](../guides/collaboration.md)；來源 ID／原文、單一入口、不能擴張及正式批准 |
| 3 角色責任 | [核心](../instructions/codex.md)及[合作](../guides/collaboration.md)；main／orchestrate 不實作、task 完整交付；新增已確認精簡路徑 |
| 4 階段定義 | [合作](../guides/collaboration.md)；完整規格、授權、停止條件、工程與研究區別 |
| 5 工程決策 | [工程](../guides/engineering.md)；簡潔、根因、局部自治、契約、證據重用及不盲目升級 |
| 6 自主推進與追蹤 | [合作](../guides/collaboration.md)及[核心](../instructions/codex.md)；接續責任、事件／cursor、節制、回報與真實背景能力 |
| 7 模型及 subagents | [模型](../guides/model-selection.md)及[合作](../guides/collaboration.md)；保留 ID、High 主要預設、Standard、實際設定核對；新增已確認 Medium 彈性 |
| 8 目標規格保存 | [合作](../guides/collaboration.md)；版本一致、已確認／待決策／已取代、暫時規格、task 保存 |
| 9 任務交接 | [合作](../guides/collaboration.md)；責任、來源、起點、證據、限制及資源保留 |
| 10 路徑與隔離 | [工程](../guides/engineering.md)；OS、主機、PROJECTS_ROOT、既有目錄、並行與共用資源 |
| 11 Git | [工程](../guides/engineering.md)；工作分支、命名、相依、merge／rebase 與 force push 界線 |
| 12 Python | [工程](../guides/engineering.md)；uv、locked、既有工具、版本來源、worktree／跨平台環境 |
| 13 驗證整合 | [工程](../guides/engineering.md)；風險相稱、證據重用、整合分支、相容性及重驗 |
| 14 交付清理 | [工程](../guides/engineering.md)及[核心](../instructions/codex.md)；操作授權、保存成果、資源盤點、不影響別人 |
| 15 本機模型 | [服務](../guides/service-integration.md)；client-integration 契約、health／models、安全取 key、主機及部署界線 |
| 16 家用伺服器 | [服務](../guides/service-integration.md)；共用文件、原專案負責、路由保護、reload／驗證與現場狀態 |

服務細節以原專案文件為來源；新指南保存跨專案限制與入口，不複製現場主機設定。拆出第四份指南，避免所有工程工作都讀取服務規則。

## 驗證重點

- 歷史檔 hash 不變，16 節都有新位置，兩項變更的授權可追溯。
- 每種需延後讀取的工作有核心觸發入口；精簡路徑下回報、決策及部署的路由一致。
- 詳細指南不能擴張核心授權；main／orchestrate 角色限制、現有模型設定、正式批准與資料保護保持。
- 本機連結、核心指南路徑與安裝佔位符有效，所有檔案 UTF-8；原始機器路徑只留在歷史資料或部署產物。
- 安裝使用同一 commit 的核心與指南，保留可回復備份；本機部署核對與新工作階段的實際載入分開回報。
