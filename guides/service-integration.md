# 共用服務與運算資源入口

只在任務涉及下列服務或運算資源時讀取。這份指南保存跨專案的安全界線及文件路由；endpoint、主機清單、SSH、網路、部署設定與操作流程，以各來源 repo 的契約及當次現場核對為準。這些規則不授權連線、部署、提交計算或修改共用服務。

## 本機模型：selfhost-models

- 只有使用者要求本機模型，或專案已決定採用 selfhost-models 時接入；不要因指南存在就替每個專案接模型。
- 優先用已指定／登錄位置，否則按 [工程指南](engineering.md) 解析 `<projects-root>/selfhost-models`；先讀 `docs/client-integration.md`。
- 本機文件不可讀時，可讀 [遠端接入契約](https://github.com/momonong/selfhost-models/blob/main/docs/client-integration.md)；遠端版本不代表本機部署，仍須核對。
- 不推測 endpoint、能力、認證或錯誤語義。依契約確認位址與連線方式，再依序核對 `/health/ready`、`/v1/models`，使用實際 model id、backend 與 capabilities；契約與歷史規則衝突時先查證，不直接套用。
- API key 依契約安全取得；契約仍採既有檔案方式時，從專案根目錄 `.state/api-key` 讀取。不得輸出到原始碼、Git、聊天或日誌。
- 不能假設開發電腦已部署；找不到服務不自行安裝、啟動或複製部署。依目前 OS、主機、容器／WSL／VM 的網路確認 localhost，不猜跨環境位址。
- 接入不代表可改共用模型服務；部署、重啟、切 backend、GPU 使用、網路／認證調整及對外開放須核對當次授權及其他工作的影響。不自行開 LAN／公網，也不假設跨容器可連。
- 超出範圍依已指定 task → orchestrate → main 路徑決策；適用精簡路徑則 task → main。

## 國網訓練：selfhost-models

涉及國網／NCHC／Nano5 訓練、研究 smoke 或其 Slurm 工作準備時，先讀研究 repo 自身的 `AGENTS.md`、README 與訓練入口，再按以下方式取得參考文件。一般本機訓練或其他 Slurm 叢集不自動套用 Nano5 規則。

- 優先使用已指定／登錄的 `selfhost-models` 位置，其次依 [工程指南](engineering.md) 查 `PROJECTS_ROOT`；未設定時只核對原生主目錄下的 `projects/selfhost-models` 候選。明確指定位置無效時回報，不另猜副本、不掃全磁碟、不自行 clone 或安裝。
- 核對來源為 `momonong/selfhost-models`，先讀 `docs/nchc-codex.md` 與其指定的 `examples/nchc-smoke/README.md`；個人歷史操作依該指南再讀 `docs/nchc-personal.md`。它們是國網入口，推論用的 `docs/client-integration.md` 不能替代訓練指南。不要將參考 repo 的 `AGENTS.md` 套用到研究 repo。
- 參考版以研究計畫已指定的 commit 為準；尚未指定時，核對本機 HEAD 並從該 commit 讀取文件，記錄完整 SHA、相對路徑與查閱日期。工作樹草稿不冒充已提交版本，不為讀指南切分支、pull 或覆寫修改。
- 沒有可用本機副本時，可用 GitHub 唯讀工具從 [國網指南入口](https://github.com/momonong/selfhost-models/blob/main/docs/nchc-codex.md) 定位，再解析所用 commit 並讀取該版本的完整文件及相關引用。不能確認版本或取得必要全文時，明說缺項，只暫停依賴它的操作；不憑搜尋摘要或聊天記憶補齊。
- 本 playbook 的 `guides-commit` 只固定本 repo 的指南，不固定外部服務 repo。國網參考 commit 由代理記入研究計畫／交接，同一 run 沿用；更新參考版時核對差異及其對既有計畫的影響，不悄悄改成 latest，也不要求使用者手改全域指示詞中的版本。
- `selfhost-models` 保存可重用操作方法與證據；研究程式、環境鎖檔、傳輸清單、Slurm 腳本、資源／費用上限、job ID 與結果紀錄留在原研究 repo 的既有結構。大型或受限資產依該專案政策保存，不因紀錄需求納入 Git。本 playbook 只維護入口與共通界線，不複製整份操作筆記或帳號設定。
- 先在已授權研究範圍內完成離線準備，再依來源指南及當次授權進行唯讀 preflight、短 GPU／研究 smoke 與完整訓練。讀文件不授權登入、傳輸、安裝遠端環境、提交 job 或使用額度；已有明確操作與資源範圍的授權就直接推進，不逐條重問。密碼／OTP 由使用者透過正式認證介面輸入，不交給代理保存。
- account、partition、配額、費用、環境與資料保留條件須在實際使用時依官方文件及已授權的現場核對確認；個人歷史值不是通用預設。區分 CPU 流程 smoke、實際 GPU 計算、完整訓練與研究品質證據，不把既有樣本成功視為新研究環境已驗收。
- 原研究專案沿用既定角色與 main 回報入口；引用文件不把工作移交 selfhost-models 對話，也不自動授權修改該 repo、啟用 UI 或擴充共用平台。

## 家用伺服器：selfhost-servers

涉及家用伺服器、HP／ASUS、momonong.me、Cloudflare Tunnel 或 Caddy 時，先定位 `<projects-root>/selfhost-servers`（已指定／登錄位置優先），依序讀：

1. `AGENTS.md` 與 `README.md`。
2. 依任務讀 `docs/infrastructure.md`、`docs/operations.md`、`config/Caddyfile`。

- 文件缺漏時核對已知資料並標待確認，不假設文件或部署存在。此 repo 是主機清單、SSH、資源、網路拓樸、服務設定及操作流程的共同來源；其他專案引用，不各自維護副本。
- 2026-09-30 原始規則確認的入口約束是 Cloudflare Tunnel → HP Caddy → 應用；momonong.me 根路徑保留首頁。這是需保留／查證的架構約束，不是本指南對現場部署的健康證明。

## 責任與協調

- 各應用專案沿用原 main／orchestrate／task 負責部署；其 task 自行讀共用文件、連線目標、驗證與回報。selfhost-servers 對話不是固定部署窗口或常駐佇列，只接使用者直接指定或明確轉交的工作。
- 已授權部署範圍內，原 task 可作必要 Caddy 路由及 selfhost-servers 設定／文件更新；不因跨 repo 另建任務。但共用入口、服務重啟等仍需確認是當次授權的一部分。
- 只有同時修改相同設定、占用資源或持有必要資訊時才跨對話協調；不因此移交整個部署責任。
- 必須人工輸入 sudo、操作 Cloudflare 等，由原專案提供已準備審查的指令、預期結果與驗證方式，不要求使用者換對話傳話。工具若要求原 task 批准，按正式機制說明最少步驟。

## 現場核對與變更

- Ubuntu 4090 桌機、HP、ASUS 與其他主機是不同環境；操作前核對主機、使用者、cwd，SSH 用文件中已核對的別名。localhost、port 與路徑依執行環境解析。
- 新增服務前核對目標資源、程序、port、資料、啟動方式與可達性；沿用現有入口，不重建 Tunnel、加裝另一套代理或占用既有 port。
- 子路徑必須核對 base URL、靜態資源、API、redirect、Cookie 與相關 WebSocket。不支援時提出子網域方案，未授權不改已確認公開 URL。
- 公開服務、應用登入與私人管理介面分別依需求設定；不為單一服務限制整個共用網域，或解除既有保護。
- 分別核對瀏覽器→Cloudflare、Tunnel→入口、入口→後端的連線與加密；外部 HTTPS 不證明跨主機內網已加密。
- 改共用設定前比對 repo 與現場，保留可回復版本，核對其他服務及同時編輯；只改本專案必要部分，保留首頁與其他路由，不覆寫別人的成果。
- Caddy 先驗證再載入，優先 reload；驗證失敗不切流量。常駐服務用 systemd 或專案既定方式，不能把前景測試當正式部署。
- 驗證包含後端健康、經 Caddy 路由、外部 HTTPS、存取控制及受影響既有服務。歷史設定／紀錄不能代替現在狀態。
- 完成後由原 task 同步 selfhost-servers 的受影響設定及文件，記錄日期、環境、結果、待確認，區分預定、已部署與已驗證。
- Token、私鑰、密碼、認證 hash 不進 Git／聊天／日誌；避免輸出含憑證的完整啟動參數或設定。文件只存必要位置與安全取得方式。
- 部署、DNS／Tunnel／Caddy、對外開放、重啟、清理及兩個 repo 的 Git 交付各依當次授權；不能因使用共用設施取得所有主機／服務權限。超出範圍交原專案決策路徑，不自動轉交 selfhost-servers 對話。
- 分別報告應用 repo、selfhost-servers repo 與現場部署的提交／PR／合併／推送／清理及驗證狀態。
