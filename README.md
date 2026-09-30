# agent-playbook

以 Git 管理個人的代理合作規則：保留精簡的 Codex 核心指示，詳細指南在相關工作發生時讀取。

## 文件入口

| 文件 | 用途 |
|---|---|
| [instructions/codex.md](instructions/codex.md) | 安裝到 Codex 的核心指示模板 |
| [guides/collaboration.md](guides/collaboration.md) | main／orchestrate／task、授權、規格、交接與追蹤 |
| [guides/model-selection.md](guides/model-selection.md) | 已授權新任務的模型、effort 與速度政策 |
| [guides/engineering.md](guides/engineering.md) | 工程決策、路徑、Git、Python、驗證與清理 |
| [guides/service-integration.md](guides/service-integration.md) | selfhost-models／selfhost-servers 的文件入口與跨專案限制 |
| [docs/migration-2026-09-30.md](docs/migration-2026-09-30.md) | 原規則映射、已確認變更與驗證方式 |
| [archive/original-2026-09-30.md](archive/original-2026-09-30.md) | 不變的歷史原文，僅供比對，不屬當前指示 |
| [AGENTS.md](AGENTS.md) | 修改本 repo 時的維護規則，並非全域指示 |

## 儲存與定位

- 已指定位置優先；macOS／Linux 的預設來源目錄是 `~/projects/agent-playbook`，或既有 `PROJECTS_ROOT` 下的 `agent-playbook`。Windows 沿用已確認的專案集合目錄。
- repo 保存來源；Codex 使用固定 commit 的本機快照。普通 git pull、切分支、改草稿不會自動變更生效政策，也不需要執行任務時連上 GitHub。
- `<codex-home>` 是實際 `CODEX_HOME`，未設定時為使用者主目錄的 `.codex`。每台電腦獨立解析，不能複製其他電腦的絕對路徑。

## 安裝／更新規則

以下是給使用者或已獲授權代理執行的流程；本文件本身不授權更新全域設定。

1. 核對來源 repo、工作目錄、Git 狀態、目標 commit 與交付授權。新正式版本先完成驗證及約定的 GitHub 交付；不把未提交工作或未確認政策安裝為正式版。
2. 核對 `<codex-home>/AGENTS.md` 與 `AGENTS.override.md`。若 override 存在，先確認用途；不可移除／覆寫它或假裝新 AGENTS.md 會優先生效。確認配置中無另外指定的指示來源需處理。
3. 備份既有全域 AGENTS.md 到 `<codex-home>/backups/` 的新檔，記錄其 SHA-256。安裝前再次比對原檔，若期間有修改就停止覆寫並核對。
4. 從確切 commit 讀取全部受版本控制的 Markdown 文件（核心、指南、入口與歷史比對資料），建立 `<codex-home>/agent-playbook/versions/<完整 commit SHA>/`，保留原相對結構、README 與 `SOURCE_COMMIT`。同名快照若已存在，核對內容一致，不改寫既有快照。
5. 以完整 SHA 取代核心模板中唯一的 `{{PLAYBOOK_COMMIT}}`，以該主機實際快照絕對路徑取代唯一的 `{{PLAYBOOK_SNAPSHOT}}`。驗證沒有剩餘佔位符，並核對四份指南都存在且對應相同 commit。
6. 將渲染後核心以暫存檔加原子替換寫入 `<codex-home>/AGENTS.md`，保留原有檔案權限。不改模型設定，不提高指示大小上限，不動其他專案或既有任務。
7. 核對安裝檔與預期渲染內容相同，快照與 Git 內容相同；報告來源 SHA、備份、安裝位置與限制。新開一個工作階段核對實際載入來源；不要宣稱既有對話會自動重新載入。

本 repo 不用 symlink 連到可變的工作分支，避免草稿直接影響全域行為。複製到 Codex 的內容是部署產物，維護時回到 repo 修改，再按此流程更新。

## 回復

取得回復授權後，先保存目前全域檔，再原子恢復選定備份並核對 hash；或從已確認的舊 commit 重新安裝。新開階段驗證載入。舊快照與備份保留供回復，清理需另外確認；不在回復時移除其他規則或切換模型。

## 版本與驗證

- 使用工作分支、可追溯 commit 與需要時的 PR 管理。角色與行為變更記錄原決策、取代範圍及仍保留的限制；小型文件調整不另開 task。
- 本次原文基準為 commit `8193e2c0cddbedd9a80412b761309422aed61fa6`。目前政策以核心及 guides 為準；Git 提交提供版本識別，不建立平行的版本編號系統。
- 檢查 `git diff --check`、所有本地 Markdown 連結／指南路徑、UTF-8、模板佔位符、原文 SHA-256、需求映射及 staged 敏感資訊。安裝另核對快照與渲染一致性。
- 核心維持精簡；不要為了縮短而移除硬限制，也不為短文件建立測試框架。沒有 CI 時如實報本機驗證，不能寫成 CI 通過。
- 本機路徑存在不等於新階段已讀取，模型／effort 寫在文字裡不等於工具已設定；分別核對。

## 官方載入行為參考

2026-09-30 核對：[AGENTS.md 載入方式](https://learn.chatgpt.com/docs/agent-configuration/agents-md)、[個人指示與全域 AGENTS.md](https://learn.chatgpt.com/docs/personalize)。本機安裝仍須核對實際檔案、override 與客戶端行為；不同入口的限制不混用。
