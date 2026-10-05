# agent-playbook

以 Git 管理個人的代理合作規則：保留精簡的 Codex 核心指示，詳細指南在相關工作發生時讀取。

## 直接複製到 Codex

開啟 **[instructions/codex.md](instructions/codex.md)**，按 GitHub 的 **Copy raw file**，將完整內容貼入 Codex 的個人指示欄位並儲存。也可開啟 [Raw 純文字](https://raw.githubusercontent.com/momonong/agent-playbook/main/instructions/codex.md)全選複製。

Windows、Linux、macOS 使用同一份文字；**不用改路徑、commit、變數或任何佔位符，也不必先安裝腳本或 clone repo**。如果只是貼到一般聊天，僅適用該對話，不等於更新全域個人指示。

代理在需要指南時，依序讀取本機固定快照、本機 repo 的固定 commit，或 GitHub 同一固定版本。沒有本機副本時，需要可用的網路／網頁工具；離線使用可選擇下方安裝方式。文件引用是代理需要主動讀取的規則，不是 Codex 自動匯入功能。

## 文件入口

| 文件 | 用途 |
|---|---|
| [instructions/codex.md](instructions/codex.md) | 可直接複製貼上的跨裝置核心指示 |
| [guides/collaboration.md](guides/collaboration.md) | main／orchestrate／task、對話命名、授權、規格、交接與追蹤 |
| [guides/model-selection.md](guides/model-selection.md) | 已授權新任務的模型、effort 與速度政策 |
| [guides/engineering.md](guides/engineering.md) | 工程決策、路徑、Git、Python、驗證與清理 |
| [guides/service-integration.md](guides/service-integration.md) | 本機模型、國網訓練與家用伺服器的文件入口及跨專案限制 |
| [docs/migration-2026-09-30.md](docs/migration-2026-09-30.md) | 原規則映射、已確認變更與驗證方式 |
| [archive/original-2026-09-30.md](archive/original-2026-09-30.md) | 不變的歷史原文，僅供比對，不屬當前指示 |
| [AGENTS.md](AGENTS.md) | 修改本 repo 時的維護規則，並非全域指示 |

## 儲存與定位

- 已指定／登錄位置優先，其次為既有 `PROJECTS_ROOT` 下的 `agent-playbook`。未設定時，各平台的原生主目錄下 `projects/agent-playbook` 只是候選，需確認存在及 repo 身分；不固定使用者名稱、磁碟代號、OneDrive 或 Documents。repo 可放在其他已確認的位置。
- repo 保存來源；核心原文與按需指南分開。指南固定在核心首行指定的 commit，本機可有同版快照，否則唯讀存取固定 GitHub 版本。普通 git pull、切分支或改草稿不自動變更已貼上的政策。
- `<codex-home>` 是實際 `CODEX_HOME`，未設定時為使用者主目錄的 `.codex`。每台電腦獨立解析，不能複製其他電腦的絕對路徑。

實際命令、各平台路徑範例與可重複安裝流程見 [跨裝置安裝](docs/installation.md)。模型、路徑與授權決策見 [2026-10-02 更新](docs/update-2026-10-02.md)；角色命名見 [2026-10-03 更新](docs/update-2026-10-03.md)；main 階段回報見 [2026-10-04 更新](docs/update-2026-10-04.md)；國網文件入口見 [2026-10-05 更新](docs/update-2026-10-05.md)。

涉及國網訓練時，核心會引導代理先讀服務指南，再唯讀參考 `selfhost-models` 的 `docs/nchc-codex.md`。研究程式、job 與執行紀錄留在原研究 repo；參考文件的 commit 記在研究計畫中，不把操作細節或帳號資料複製進全域指示。這次更新仍只需整份替換 `instructions/codex.md`；詳細指南按需讀取，既有批准用途的 Custom rules 無需因本次文件入口更新而修改。

## 可選：本機安裝／更新

適合需要本機指南快照及備份的人；直接複製貼上的使用者不必執行。以下流程供使用者或已獲授權代理使用；本文件本身不授權更新全域設定。

1. 核對來源 repo、工作目錄、Git 狀態、目標 commit 與交付授權。新正式版本先完成驗證及約定的 GitHub 交付；不把未提交工作或未確認政策安裝為正式版。
2. 核對 `<codex-home>/AGENTS.md` 與 `AGENTS.override.md`。若 override 存在，先確認用途；不可移除／覆寫它或假裝新 AGENTS.md 會優先生效。確認配置中無另外指定的指示來源需處理。
3. 執行預覽並核對來源、目標與 `current_sha256`；套用時帶入該 hash（首次安裝使用 `missing`）。備份既有全域 AGENTS.md 到 `<codex-home>/backups/` 的新檔，記錄其 SHA-256。安裝前再次比對原檔，若期間有修改就停止覆寫並核對。
4. 從指定核心 commit 取得 `instructions/codex.md` 原文，再從其 `guides-commit` 取得該版本全部 Markdown，建立 `<codex-home>/agent-playbook/versions/<指南完整 SHA>/`，保留相對結構與 `SOURCE_COMMIT`。指南版本可以早於核心版本；同名快照只核對，不改寫。
5. 驗證核心沒有佔位符，四份指南屬於其指定版本；核心原樣安裝，沒有模板渲染或裝置路徑替換。
6. 將原始核心以暫存檔加原子替換寫入 `<codex-home>/AGENTS.md`，保留原有檔案權限。不改模型設定，不提高指示大小上限，不動其他專案或既有任務。
7. 核對安裝檔與 repo 中核心原文逐位元組相同，快照與 Git 內容相同；報告來源 SHA、備份、安裝位置與限制。新開一個工作階段核對實際載入來源；不要宣稱既有對話會自動重新載入。

本 repo 不用 symlink 連到可變的工作分支，避免草稿直接影響全域行為。複製到 Codex 的內容是部署產物，維護時回到 repo 修改，再按此流程更新。

## 回復

取得回復授權後，先保存目前全域檔，再原子恢復選定備份並核對 hash；或從已確認的舊 commit 重新安裝。新開階段驗證載入。舊快照與備份保留供回復，清理需另外確認；不在回復時移除其他規則或切換模型。

## 版本與驗證

- 使用工作分支、可追溯 commit 與需要時的 PR 管理。角色與行為變更記錄原決策、取代範圍及仍保留的限制；小型文件調整不另開 task。
- 本次原文基準為 commit `8193e2c0cddbedd9a80412b761309422aed61fa6`。目前政策以核心及其釘選版本的 guides 為準；Git 提交提供版本識別，不建立平行的版本編號系統。
- 檢查 `git diff --check`、所有本地 Markdown 連結／指南路徑、UTF-8、無待替換佔位符、原文 SHA-256、需求映射及 staged 敏感資訊。安裝另核對快照與核心原樣複製一致性。
- 核心維持精簡；不要為了縮短而移除硬限制，也不為短文件建立測試框架。安裝程式以標準函式庫 unittest 驗證，命令為 `uv run --locked python -m unittest discover -s tests -v`；CI 在 Linux／macOS／Windows 跑同組測試。未實際通過的 runner 不能列為已驗證平台。
- 本機路徑存在不等於新階段已讀取，模型／effort 寫在文字裡不等於工具已設定；分別核對。

指南更新時，先保存指南變更為可追溯 commit，再讓核心的 `guides-commit` 與遠端 URL 指向它；同一輪交付完成兩者。使用者只需再次複製核心，無需自行編輯版本。

## 官方載入行為參考

2026-09-30 核對：[AGENTS.md 載入方式](https://learn.chatgpt.com/docs/agent-configuration/agents-md)、[個人指示與全域 AGENTS.md](https://learn.chatgpt.com/docs/personalize)。本機安裝仍須核對實際檔案、override 與客戶端行為；不同入口的限制不混用。
