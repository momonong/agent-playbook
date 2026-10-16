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
| [guides/collaboration.md](guides/collaboration.md) | 單一目標對話、討論與執行、subagents、授權與必要交接 |
| [guides/external-execution.md](guides/external-execution.md) | agy 等外部 CLI task 的交接、授權、接續及驗收 |
| [guides/learning.md](guides/learning.md) | 每個指定專案的學習主軸、概念路線、案例與學習交接 |
| [guides/model-selection.md](guides/model-selection.md) | 已授權新任務的模型、effort 與速度政策 |
| [guides/engineering.md](guides/engineering.md) | 工程決策、路徑、Git、Python、驗證與清理 |
| [guides/service-integration.md](guides/service-integration.md) | 本機模型、API Quota Broker、國網訓練與家用伺服器的入口及跨專案限制 |
| [docs/migration-2026-09-30.md](docs/migration-2026-09-30.md) | 原規則映射、已確認變更與驗證方式 |
| [archive/original-2026-09-30.md](archive/original-2026-09-30.md) | 不變的歷史原文，僅供比對，不屬當前指示 |
| [AGENTS.md](AGENTS.md) | 修改本 repo 時的維護規則，並非全域指示 |

## 儲存與定位

- 已指定／登錄位置優先，其次為既有 `PROJECTS_ROOT` 下的 `agent-playbook`。未設定時，各平台的原生主目錄下 `projects/agent-playbook` 只是候選，需確認存在及 repo 身分；不固定使用者名稱、磁碟代號、OneDrive 或 Documents。repo 可放在其他已確認的位置。
- repo 保存來源；核心原文與按需指南分開。指南固定在核心首行指定的 commit，本機可有同版快照，否則唯讀存取固定 GitHub 版本。普通 git pull、切分支或改草稿不自動變更已貼上的政策。
- `<codex-home>` 是實際 `CODEX_HOME`，未設定時為使用者主目錄的 `.codex`。每台電腦獨立解析，不能複製其他電腦的絕對路徑。

安裝命令見[跨裝置安裝](docs/installation.md)；歷史決策由[遷移記錄](docs/migration-2026-09-30.md)追溯，已取代內容不作現行指令。服務與國網只按相關指南取得來源契約，不把操作細節複製進全域指示。

## 一個對話、一個目標

同一完整目標在同一對話討論、規劃、實作、驗證並直接回報；不再強制 main／orchestrate／task 分層，主對話可實作。先討論不等於授權修改；確認執行後在原對話繼續。目標已清楚且已授權時直接做，不要求形式上的討論或另開實作對話。

新的獨立目標或上下文已妨礙工作時才考慮新對話；同一問題的修正沿用原處。需要時用有界 subagents 協助，由原對話核對整合，使用者不用巡查助手或搬運成果。長期跨對話協作僅在具體需要且獲授權時使用。

對話按專案分類，名稱只寫核心目標；學習、專利與歷史保留必要用途標記，完整命名規則見[合作指南](guides/collaboration.md#目標命名與接續)。

模型依目標選擇，主對話保留使用者設定；需要選型時以 Astra Medium、Sol 6.1 High 等既有配置為起點，不綁角色、不強制換模型、不全面升級。舊對話與 learn／專利用途保留，不因更新刪除、封存、改名、傳訊或恢復工作。

完整規則見 [合作指南](guides/collaboration.md)及[模型指南](guides/model-selection.md)，授權與取代範圍見 [2026-10-16 單一目標對話改版](docs/update-2026-10-16-goal-conversations.md)。這項政策取代先前固定分層及集中 main 回報規則；歷史更新紀錄只作追溯。

## 開發與學習並行

採用此模式的個人專案各有一個指定學習對話（learn），由使用者確認主軸、目標與範圍，再建立概念與先備知識路線；learn 是用途稱呼，不是固定標題。開發成果是教學案例，不按每次 commit 排課；原工程目標對話仍負責決策確認、交付與驗收。共通方法見 [學習指南](guides/learning.md)，各專案的主軸、案例與進度留在該專案。規則更新不會自動建立對話、讀取所有專案或啟用排程。

## 外部 CLI task

原目標對話可直接實作；在階段授權涵蓋供應商、資料與操作範圍時，也可由 agy 等外部 CLI 承擔具體工作。簡單工作用短指令，多輪工作用 Markdown 與明確 session 接續；協調者核對成果，不另建只轉傳的 Codex task。規格、結果與證據留在原專案，具體流程見 [外部執行指南](guides/external-execution.md)。新增規則不自動啟用外部模型、修改批准設定或保證節省比例。

## 共用 API 服務

API 配額與供應商路由接入先讀 [服務指南](guides/service-integration.md#api-配額與供應商路由api-quota-broker)，再引用 Broker 已發布的接入契約。這是應用後端的共用 Gateway；文件更新不自動切換既有服務或 Codex 模型呼叫。版本與需求映射見 [2026-10-12 更新](docs/update-2026-10-12.md)。

## 可選：本機安裝／更新

適合需要本機指南快照及備份的人；直接複製貼上的使用者不必執行。以下流程供使用者或已獲授權代理使用；本文件本身不授權更新全域設定。

依[安裝流程與保護規則](docs/installation.md#一次安裝流程)執行：核對來源及指示優先順序、預覽固定 commit、備份舊檔、保存釘選指南、原子安裝並驗證 hash。只有核對過且完成約定 Git 交付的版本才作正式安裝；本文件不授權改設定。

安裝不切換模型或恢復舊任務，也不保證舊對話自動重新載入。核心與指南各以 commit 追溯，不用 symlink 連到可變工作分支；完整步驟只在安裝文件維護。

## 回復

取得回復授權後，先保存目前全域檔，再原子恢復選定備份並核對 hash；或從已確認的舊 commit 重新安裝。新開階段驗證載入。舊快照與備份保留供回復，清理需另外確認；不在回復時移除其他規則或切換模型。

## 版本與驗證

- 使用工作分支、可追溯 commit 與需要時的 PR 管理。角色與行為變更記錄原決策、取代範圍及仍保留的限制；小型文件調整不另開 task。
- 本次原文基準為 commit `8193e2c0cddbedd9a80412b761309422aed61fa6`。目前政策以核心及其釘選版本的 guides 為準；Git 提交提供版本識別，不建立平行的版本編號系統。
- 檢查 `git diff --check`、所有本地 Markdown 連結／指南路徑、UTF-8、無待替換佔位符、原文 SHA-256、需求映射及 staged 敏感資訊。安裝另核對快照與核心原樣複製一致性。
- 核心維持精簡；不要為了縮短而移除硬限制，也不為短文件建立測試框架。安裝程式以標準函式庫 unittest 驗證，命令為 `uv run --locked python -m unittest discover -s tests -v`；CI 在 Linux／macOS／Windows 跑同組測試。未實際通過的 runner 不能列為已驗證平台。
- 核心以 UTF-8 約 8–9 KB 為維護目標，保存首次行動所需規則與必讀入口；完整模型表、外部 CLI 操作、教學及追蹤流程留在既有指南。此數字不是官方上限或用量保證。新增核心內容須說明常駐必要性，並記錄大小變化與規則落點，見 [核心精簡記錄](docs/update-2026-10-10.md#核心精簡與後續維護)。
- 本機路徑存在不等於新階段已讀取，模型／effort 寫在文字裡不等於工具已設定；分別核對。

指南更新時，先保存指南變更為可追溯 commit，再讓核心的 `guides-commit` 與遠端 URL 指向它；同一輪交付完成兩者。使用者只需再次複製核心，無需自行編輯版本。

## 官方載入行為參考

2026-09-30 核對：[AGENTS.md 載入方式](https://learn.chatgpt.com/docs/agent-configuration/agents-md)、[個人指示與全域 AGENTS.md](https://learn.chatgpt.com/docs/personalize)。本機安裝仍須核對實際檔案、override 與客戶端行為；不同入口的限制不混用。
