# agent-playbook

以 Git 管理個人的代理合作規則：保留精簡的 Codex 核心指示，詳細指南在相關工作發生時讀取。

## 直接複製到 Codex

開啟 **[instructions/codex.md](instructions/codex.md)**，按 GitHub 的 **Copy raw file**，將完整內容貼入 Codex 的個人指示欄位並儲存。也可開啟 [Raw 純文字](https://raw.githubusercontent.com/momonong/agent-playbook/main/instructions/codex.md)全選複製。

Windows、Linux、macOS 使用同一份文字；**不用改路徑、commit、變數或任何佔位符，也不必先安裝腳本或 clone repo**。如果只是貼到一般聊天，僅適用該對話，不等於更新全域個人指示。

核心保留首次行動所需規則與必讀路由。代理執行命中的工作前，讀適用指南章節全文，再沿指南讀必要專案契約與文件；多類工作各讀相應章節，摘要或看到連結不算已讀。同版已讀章節可重用，普通問答不按關鍵詞全讀。

指南依序定位本機固定快照、本機 repo 的固定 commit，或 GitHub 同一固定版本；缺少必要文件時回報，不猜測規則。沒有本機副本時需要網路／網頁工具；離線可選下方安裝方式。這是代理須主動執行的讀取規則，不是 Codex 自動匯入功能，也不保證模型每次都會遵守。

## 文件入口

| 文件 | 用途 |
|---|---|
| [instructions/codex.md](instructions/codex.md) | 可直接複製貼上的跨裝置核心指示 |
| [guides/collaboration.md](guides/collaboration.md) | 單一目標對話、討論與執行、subagents、授權與必要交接 |
| [guides/external-execution.md](guides/external-execution.md) | agy 等外部 CLI task 的交接、授權、接續及驗收 |
| [guides/learning.md](guides/learning.md) | 每個指定專案的學習主軸、概念路線、案例與學習交接 |
| [guides/model-selection.md](guides/model-selection.md) | Astra Ultra 目標責任、Sol 6.1 Ultra 實作分工與設定界線 |
| [guides/engineering.md](guides/engineering.md) | 工程決策、路徑、Git、Python、驗證、HTML 可讀交付與清理 |
| [guides/service-integration.md](guides/service-integration.md) | 本機模型、API Quota Broker、私人 HTML 預覽、國網訓練與家用伺服器的入口及跨專案限制 |
| [docs/migration-2026-09-30.md](docs/migration-2026-09-30.md) | 原規則映射、已確認變更與驗證方式 |
| [docs/update-2026-10-18-model-and-branch-policy.md](docs/update-2026-10-18-model-and-branch-policy.md) | 模型分工、分支分類、短核心與按需必讀的決策及發布界線 |
| [docs/update-2026-10-18-astra-ultra-ownership.md](docs/update-2026-10-18-astra-ultra-ownership.md) | 後續 Ultra 預設、Astra 全程負責與 Sol subagent 承接決策 |
| [docs/update-2026-10-20-html-delivery.md](docs/update-2026-10-20-html-delivery.md) | 使用者當前裝置的 HTML 渲染交付與待啟用預覽服務決策 |
| [docs/update-2026-10-20-html-preview-integration.md](docs/update-2026-10-20-html-preview-integration.md) | 工程驗證通過的私人 HTML 預覽之固定契約、授權範圍及正式接入 |
| [archive/original-2026-09-30.md](archive/original-2026-09-30.md) | 不變的歷史原文，僅供比對，不屬當前指示 |
| [AGENTS.md](AGENTS.md) | 修改本 repo 時的維護規則，並非全域指示 |
| [docs/device-sync.md](docs/device-sync.md) | 每台裝置的唯一承接對話、同步範圍與開場指示 |
| [docs/update-2026-10-22-device-sync.md](docs/update-2026-10-22-device-sync.md) | 裝置同步、技能來源與保護規則的決策及需求映射 |
| [skills/README.md](skills/README.md) | 共用個人技能快照、來源／授權與依賴 |
| [docs/academic-research-skills.md](docs/academic-research-skills.md) | 六項學術技能的獨立安裝來源、用途、授權及驗證界線，尚未共用納管 |

## 儲存與定位

- 已指定／登錄位置優先，其次為既有 `PROJECTS_ROOT` 下的 `agent-playbook`。未設定時，各平台的原生主目錄下 `projects/agent-playbook` 只是候選，需確認存在及 repo 身分；不固定使用者名稱、磁碟代號、OneDrive 或 Documents。repo 可放在其他已確認的位置。
- repo 保存來源；核心原文與按需指南分開。指南固定在核心首行指定的 commit，本機可有同版快照，否則唯讀存取固定 GitHub 版本。普通 git pull、切分支或改草稿不自動變更已貼上的政策。
- `<codex-home>` 是實際 `CODEX_HOME`，未設定時為使用者主目錄的 `.codex`。每台電腦獨立解析，不能複製其他電腦的絕對路徑。

安裝命令見[跨裝置安裝](docs/installation.md)；歷史決策由[遷移記錄](docs/migration-2026-09-30.md)追溯，已取代內容不作現行指令。服務與國網只按相關指南取得來源契約，不把操作細節複製進全域指示。

引用 `selfhost-servers` 時，依[伺服器文件定位規則](guides/service-integration.md#家用伺服器selfhost-servers)核對來源、版本及同版文件，再按受限部署契約讀能力矩陣與唯讀 preflight；登錄目錄或工作樹名稱不代表最新，不為讀文件改動既有工作。

## 一個對話、一個目標

同一完整目標在原對話持續承接討論、規劃、實作、驗證並直接回報；不強制 main／orchestrate／task 分層，實作分工依模型指南。先討論不等於授權修改；目標已確認且已授權時在原對話推進，不要求另開實作對話。

明確要求 `grill-me` 或深入挑戰方案時，依[合作指南](guides/collaboration.md#使用-grill-me-深問方案)在原對話收斂待決問題；共識不取代執行授權，固定技能來源與界線見[決策紀錄](docs/update-2026-10-22-scoped-deployment-and-grill-me.md)。

新的獨立目標或上下文已妨礙工作時才考慮新對話；同一問題的修正沿用原處。需要時用有界 subagents 協助，由原對話核對整合，使用者不用巡查助手或搬運成果。長期跨對話協作僅在具體需要且獲授權時使用。

對話按專案分類，名稱只寫核心目標，不強制 main／dev 前綴；學習、專利與歷史保留必要用途標記，完整命名規則見[合作指南](guides/collaboration.md#目標命名與接續)。

Astra Ultra 負責討論、決策、推進與最後核對，已確認且已授權的實作預設交 Sol 6.1 Ultra subagent；工具操作與設定界線見模型指南。舊對話、既有設定與 learn／專利用途保留，不批次換模型、刪除、封存、改名、傳訊或恢復工作。

完整規則見 [合作指南](guides/collaboration.md)及[模型指南](guides/model-selection.md)，授權與取代範圍見 [2026-10-16 單一目標對話改版](docs/update-2026-10-16-goal-conversations.md)。這項政策取代先前固定分層及集中 main 回報規則；歷史更新紀錄只作追溯。

分支入口與短核心／按需必讀見 [2026-10-18 首輪決策](docs/update-2026-10-18-model-and-branch-policy.md)，後續模型與承接方式以 [Astra Ultra 目標責任決策](docs/update-2026-10-18-astra-ultra-ownership.md)取代；指南提交、核心重新釘選與固定版本安裝依下方流程核對。

## 開發與學習並行

採用此模式的個人專案各有一個指定學習對話（learn），由使用者確認主軸、目標與範圍，再建立概念與先備知識路線；learn 是用途稱呼，不是固定標題。開發成果是教學案例，不按每次 commit 排課；原工程目標對話仍負責決策確認、交付與驗收。共通方法見 [學習指南](guides/learning.md)，各專案的主軸、案例與進度留在該專案。規則更新不會自動建立對話、讀取所有專案或啟用排程。

## 外部 CLI task

指定 agy 等外部 CLI 為執行方式前，須有涵蓋供應商、資料、操作與資源的階段授權；未指定時依模型指南的預設承接。簡單工作用短指令，多輪工作用 Markdown 與明確 session 接續；原對話跟進並核對成果，不另建只轉傳的 Codex task。規格、結果與證據留在原專案，具體流程見 [外部執行指南](guides/external-execution.md)。新增規則不自動啟用外部模型、修改批准設定或保證節省比例。

## 共用 API 服務

API 配額與供應商路由接入先讀 [服務指南](guides/service-integration.md#api-配額與供應商路由api-quota-broker)，再引用 Broker 已發布的接入契約。這是應用後端的共用 Gateway；文件更新不自動切換既有服務或 Codex 模型呼叫。版本與需求映射見 [2026-10-12 更新](docs/update-2026-10-12.md)。

## 私人 HTML 交付

本次 HTML 產生與私人預覽交付已獲授權，且既有通道已配置可用時，依[工程交付流程](guides/engineering.md#html-交付)與[私人預覽入口](guides/service-integration.md#私人-html-預覽html-preview)，上傳指定單份成品、取得 HTTPS 網址與期限、核對瀏覽器，再由原對話附連結及原稿。日常操作沿用既有權限，不逐次要求部署或 sudo；不擴張為掃描或上傳歷史文件。服務接入以固定契約為準，啟用依據及未完人工驗收見[本次整合紀錄](docs/update-2026-10-20-html-preview-integration.md)。不修改上游 HTML skill 或模型設定。

## 可選：本機安裝／更新

新裝置在已授權位置 clone 本 repo，既有裝置沿用原目錄取得已合併版本；Git 取得來源後仍須明確安裝。Git 與 Python 3.11+ 即可直接執行 `python scripts/install.py`；既有環境建議 `uv run --locked python scripts/install.py`。缺工具先回報，由該裝置對話依授權處理，不自動安裝全域 runtime。

每台環境沿用或由使用者指定一個 `agent-playbook｜裝置名稱` 對話，負責本裝置開發環境與已確認習慣同步；遠端／WSL 分開核對。依[裝置契約與開場指示](docs/device-sync.md)，再走[安裝文件](docs/installation.md#一次安裝流程)的固定完整 SHA → 預覽 → 雙 hash CAS／備份安裝 → check。加 `--with-skills` 同步七份 manifest 技能（含 `ui-ux-pro-max`、基本 `caveman`）；Superpowers 走[官方插件與逐裝置核對](docs/installation.md#superpowers-官方插件)，不納入 manifest。省略技能選項時保留原核心／指南安裝介面。直接貼核心的使用者仍不必執行。

同一版本提供核心、釘選指南及技能的相同 bytes；工具／插件、客戶端發現與人工接受另核對。安裝不改模型、effort 或其他設定、不搬技能位置、不恢復舊任務，也不保證既有對話重新載入。新共用技能的已授權安裝任務須一併納入快照與 manifest，避免只裝一台；完整保護與命令只在安裝文件維護。

六項學術研究技能目前採固定上游來源的本機獨立安裝，未加入七包共用 manifest；`--with-skills` 不會同步它們。來源 pin、功能／runtime、ARS 非商業授權及 Windows 已測／未測範圍集中於[學術技能文件](docs/academic-research-skills.md)，跨裝置納管仍待完成。

## 回復

取得回復授權後，先保存目前全域檔，再原子恢復選定備份並核對 hash；或從已確認的舊 commit 重新安裝。新開階段驗證載入。舊快照與備份保留供回復，清理需另外確認；不在回復時移除其他規則或切換模型。

## 版本與驗證

- 新工作分支依主要目的用 `feat/`、`fix/`、`docs/` 等分類，取代工具一般 `codex/` 預設，不加 `codex/` 外層；沿用合適既有分支，不擅自改名。完整分類及專案規範優先原則見[工程指南](guides/engineering.md#git-分支與提交)。使用可追溯 commit 與需要時的 PR 管理；行為變更記錄決策、取代範圍與保留限制，小型文件調整不另開 task。
- 本次原文基準為 commit `8193e2c0cddbedd9a80412b761309422aed61fa6`。目前政策以核心及其釘選版本的 guides 為準；Git 提交提供版本識別，不建立平行的版本編號系統。
- 檢查 `git diff --check`、所有本地 Markdown 連結／指南路徑、UTF-8、無待替換佔位符、原文 SHA-256、需求映射及 staged 敏感資訊。安裝另核對快照與核心原樣複製一致性。
- 核心維持精簡；不要為了縮短而移除硬限制，也不為短文件建立測試框架。安裝程式以標準函式庫 unittest 驗證，命令為 `uv run --locked python -m unittest discover -s tests -v`；CI 在 Linux／macOS／Windows 跑同組測試。未實際通過的 runner 不能列為已驗證平台。
- 核心以 UTF-8 約 8–9 KB 為維護目標，保存首次行動所需規則與必讀入口；完整模型表、外部 CLI 操作、教學及追蹤流程留在既有指南。此數字不是官方上限或用量保證。新增核心內容須說明常駐必要性，並記錄大小變化與規則落點，見 [核心精簡記錄](docs/update-2026-10-10.md#核心精簡與後續維護)。
- 本機路徑存在不等於新階段已讀取，模型／effort 寫在文字裡不等於工具已設定；分別核對。

指南更新時，先保存指南變更為可追溯 commit，再讓核心的 `guides-commit` 與遠端 URL 指向它；同一輪交付完成兩者。使用者只需再次複製核心，無需自行編輯版本。

## 官方載入行為參考

2026-09-30 核對：[AGENTS.md 載入方式](https://learn.chatgpt.com/docs/agent-configuration/agents-md)、[個人指示與全域 AGENTS.md](https://learn.chatgpt.com/docs/personalize)。本機安裝仍須核對實際檔案、override 與客戶端行為；不同入口的限制不混用。
