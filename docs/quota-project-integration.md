# Quota 共用接入說明

給 Calcifer 或其他後端專案的交接是：**本說明與固定版完整手冊、同版 SDK 接入包，以及另走私人管道的專案 token**。完整 API／SDK／維運契約由 Broker 維護；本頁只集中首次接入所需資訊，不另建一份權威手冊。

本頁於 2026-11-14 核對 `momonong/api-quota-broker` 已合併 commit `d03ee867c04bb7ed7039183db0b2ac4374ff5f91`（[PR #9](https://github.com/momonong/api-quota-broker/pull/9)）。以下連結固定同版；更新接入版本時先比對差異。文件及歷史驗收不證明目前服務健康、額度或接入專案已完成整合，也不授權呼叫模型、發 token 或改服務。

## 固定版完整手冊索引

| 入口 | 要讀什麼 |
|---|---|
| [Broker README](https://github.com/momonong/api-quota-broker/blob/d03ee867c04bb7ed7039183db0b2ac4374ff5f91/README.md) | 2.0.0 狀態、來源與新舊介面分工 |
| [開發者 API／SDK 2.0.0](https://github.com/momonong/api-quota-broker/blob/d03ee867c04bb7ed7039183db0b2ac4374ff5f91/docs/developer-api.md) | **首次接入主入口**：安裝、設定、Python 使用、政策、恢復及限制 |
| [範例執行說明](https://github.com/momonong/api-quota-broker/blob/d03ee867c04bb7ed7039183db0b2ac4374ff5f91/examples/project_client/README.md)／[client.py](https://github.com/momonong/api-quota-broker/blob/d03ee867c04bb7ed7039183db0b2ac4374ff5f91/examples/project_client/client.py) | 可複製到獨立專案的 catalog／explain／submit／wait／result 範例 |
| [constraints-linux-py312.txt](https://github.com/momonong/api-quota-broker/blob/d03ee867c04bb7ed7039183db0b2ac4374ff5f91/examples/project_client/constraints-linux-py312.txt) | 該版 Linux Python 3.12 消費端已驗證的相依版本 |
| [OpenAPI](https://github.com/momonong/api-quota-broker/blob/d03ee867c04bb7ed7039183db0b2ac4374ff5f91/docs/openapi.json) | 機器契約：加密外層、內層工作與錯誤結構；不能當 OpenAI API |
| [加密 API 管理契約](https://github.com/momonong/api-quota-broker/blob/d03ee867c04bb7ed7039183db0b2ac4374ff5f91/docs/encrypted-local-api.md) | 管理端政策、標準封裝、金鑰、持久工作及下游精確查回 |
| [HP 加密 API 維運](https://github.com/momonong/api-quota-broker/blob/d03ee867c04bb7ed7039183db0b2ac4374ff5f91/docs/hp-encrypted-api-operations.md) | 金鑰保管、自動維護、私人 worker 路徑與復原界線；一般應用不執行管理步驟 |
| [加密 HTTPS／4090 驗收](https://github.com/momonong/api-quota-broker/blob/d03ee867c04bb7ed7039183db0b2ac4374ff5f91/docs/encrypted-local-api-acceptance.md) | 2026-11-14 真實文字、單圖及回覆遺失恢復證據；與下方歷史段、未驗收範圍分開 |
| [SDK 1.3 歷史文件](https://github.com/momonong/api-quota-broker/blob/d03ee867c04bb7ed7039183db0b2ac4374ff5f91/docs/developer-api-legacy.md)／[直接 Gateway 舊契約](https://github.com/momonong/api-quota-broker/blob/d03ee867c04bb7ed7039183db0b2ac4374ff5f91/docs/client-integration.md) | 僅供辨識舊 JSON／legacy 共用 token 與遷移，不能取代新版入口 |

該版 OpenAPI 的 `info.description` 尚留 `not deployed` 開發文字；部署證據以同版驗收文件的 **2026-11-14 正式案例**為準。舊共用 Gateway token 沒有專案 ACL 的限制，不可泛指新版 project-scoped API；新版依 server-owned project、scope 與政策控制存取。

## 交給新專案的材料

正式 API root：`https://momonong.me/quota/api/v1`。Python SDK：`api-quota-broker==2.0.0`，匯入 `quota_broker.client.ProjectClient`。這是 Quota 自有契約，不能只把 OpenAI／Gemini SDK 或 Node／OpenCode 的 `base_url` 指向它。

向 Quota 維護者取得固定同版接入包 `quota-sdk-2.0.0-linux-x86_64-20261114.zip`；此包是個別交付產物，**沒有 PyPI 或 GitHub Release 下載入口**，不要求讀者存取維護者的本機路徑。已交付包 SHA-256：

```text
80799efa949aa8a8aef93202537456277486d7e1aca4b4f48bc795300895d317
```

包內應有以下非秘密檔案；先核對包與 `SHA256SUMS`，再核對文件／範例版本：

- `api_quota_broker-2.0.0-py3-none-any.whl` 與 `quota_broker_ohttp-0.1.0-cp312-abi3-manylinux_2_34_x86_64.whl`。
- `constraints-linux-py312.txt`、公開 `trust-profile.json`、文件及 `examples/project_client` 範例。
- **不含 token 或解密私鑰**；token 另發，公開 profile 的根信任仍須經獨立可信管道核對。

目前消費端只驗收 Linux x86_64、Python 3.12、glibc ≥2.34；沒有 JS／瀏覽器 SDK。其他 OS／ARM 不以自行編譯或純 HTTP 範例冒充支援。

## 專案 token 申請

目前由 Quota 管理端登錄獨立 project、政策及限制後，經已驗證的私人管道發放，沒有自助申領流程。申請只需提供下列非秘密需求：

```text
專案名稱／建議 project ID：
資料是否敏感、允許送往哪些執行端：
需要 local_only、cloud_only，或非敏感專案允許兩者：
能力／輸入型態（例如文字、單張圖片）：
預期負載（頻率、輸入大小、輸出上限、同時工作數、等待期限）：
```

一般接入使用 `read`／`plan`／`execute`；配額、模型能力與工作限制由管理端設定，不授予一般應用 admin 權限。網站密碼、Owner token、legacy 共用 token、provider key、worker key 都不能當本專案 token。現有 `private-development` 僅准本地加密，新專案應申請自己的 token；本文件不代表已發放。

token 放後端受保護的憑證檔（檔案 0600、父目錄 0700），或已批准且符合資料界線的秘密管理方式。不得放入前端、Git、URL、指示詞、聊天、命令列參數或日誌；敏感專案也不能透過會暴露它的外部秘密服務取得。

## 本地與雲端政策

兩者都用相同 SDK、專案 token 與 HTTPS；SDK 將 token、內容及內層操作封裝在 OHTTP 內，回應也加密。`trust-profile.json` 必須從獨立可信管道取得並核對 audience／root／epoch，不能信任公開 API 自稱的新 root。持久 trust state 放受保護目錄並保留，以拒絕版本回退；不靠刪除狀態排除信任錯誤，root／epoch 變更依維護者的獨立復原流程處理。

| execution_policy | 行為及必要條件 |
|---|---|
| `local_only` | 只在已登錄的自有本地模型執行。敏感專案由伺服器同時鎖 `allowed_execution=["local_only"]`、`default_execution="local_only"`、`encryption_required=true`；客戶端不能放寬 |
| `cloud_only` | 僅在專案與資料都允許外送時使用。仍加密到自有 HP，但 HP 之後會把推論必要明文交給雲端 provider；token 必須獲准雲端執行 |

沒有 `auto`；省略 policy 採專案預設，正式整合宜明確指定。本地離線、OOM、滿載、timeout／unknown 均不能改送雲端；改 policy 是另一個新工作決策，不能當舊工作重試。

SDK／HP 處理日常加解密及金鑰維護，應用不持有解密私鑰、不需要 USB。HP 與 worker 仍是可信明文端點；Cloudflare 仍可見 IP、時間、流量大小等 metadata。應用自己的 log、telemetry 與其他外部服務也須遵守資料界線。

## 安裝與最小呼叫

在解壓後的接入包根目錄，以已確認的 Linux／Python 3.12 驗證環境執行：

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --constraint ./constraints-linux-py312.txt \
  ./quota_broker_ohttp-0.1.0-cp312-abi3-manylinux_2_34_x86_64.whl \
  './api_quota_broker-2.0.0-py3-none-any.whl[encrypted]'
```

正式整合沿用原專案依賴工具並鎖定同版，不複製其他環境的 `.venv`。不需啟動自己的 Broker、下載權重或持有供應商 key。

由受保護憑證安全注入 `QUOTA_PROJECT_TOKEN`；以下只設定非秘密位置，路徑換成執行端實際原生絕對路徑：

```bash
export QUOTA_BASE_URL=https://momonong.me/quota/api/v1
export QUOTA_TRUST_PROFILE=/absolute/managed/trust-profile.json
export QUOTA_TRUST_STATE=/absolute/private-state/quota-trust.sqlite
```

trust state 檔案須為 0600、父目錄 0700，由應用帳號管理並持久保存。**先把 request_key、政策及業務工作關聯保存到應用紀錄，再提交**；`QUOTA_REQUEST_KEY` 表示應用已保存的原 key，不在每次重試重新產生。key 為 1–120 個 `[A-Za-z0-9._~-]` 字元，不含秘密或業務正文。

以下為首次提交片段；只有取得該專案資料／模型呼叫授權後才執行 `run`。完整可執行命令及 PNG 範例使用索引中的 Broker 範例，不把接入文件當實際呼叫授權。

```python
import os
from quota_broker.client import ClientError, ProjectClient

client = ProjectClient(
    os.environ["QUOTA_BASE_URL"],
    os.environ["QUOTA_PROJECT_TOKEN"],
    trust_profile=os.environ["QUOTA_TRUST_PROFILE"],
    trust_state=os.environ["QUOTA_TRUST_STATE"],
)
request_key = os.environ["QUOTA_REQUEST_KEY"]
task = {
    "request_key": request_key,
    "execution_policy": "local_only",
    "capability": "text_generation",
    "input": {"messages": [{"role": "user", "content": "只回答 OK。"}]},
    "max_output_tokens": 32,
}
catalog = client.catalog()       # 不推論
plan = client.explain(task)      # 不推論、不保留新配額
if plan["selected_target_id"] is None:
    raise RuntimeError("目前沒有合格路由；保留原工作並檢查 explain reasons")
try:
    outcome = client.run(task, wait_timeout=650)  # 提交一次並等待，會執行
    answer = outcome["result"]["text"]
except ClientError as exc:
    problem = exc.detail        # 依資料政策保存分類與原 key，不自動重送
    raise
```

允許雲端的**新工作**可指定 `cloud_only`；既有工作沿用原 policy／key。省略 provider／model 讓 Broker 選合格路由；需固定模型時用 catalog 實際值並 explain。catalog 的能力／用量證據不是即時設備健康、帳戶官方餘額或品質保證，派送仍會重新檢查。

## 斷線、未知結果與取消

逾時、`transport_unknown`、404 都不能單獨證明未執行；不再次 `run`／`submit`，不換 key、provider、endpoint 或 instance。重新啟動應用後，使用同 project 的有效 token 與原 key 恢復，不需保留原 OHTTP 上下文：

```python
status = client.status(request_key)
outcome = client.wait(request_key, wait_timeout=120)
# 已有結果時也可使用 client.result(request_key)
```

wait 只查原工作；等待期限不是取消或執行 deadline。查不到、`unknown` 或信任錯誤交維護者核對，不清除 trust state／帳本，也不以換 key 逃過 conflict。派送後 `cancel` 僅是要求，直到下游證實停止前不能當作已停止或釋放容量。

本地完成結果保存 **1 小時**，需要長期保存就及時取回到已授權儲存；正文逾期不解除原 key 的防重派。`pending/storage_failed`／`unknown` 保留恢復身分。取得答案、內容完整／業務品質及用量結算分別判讀，缺失用量不能轉成零。

## 接入驗收與目前能力

接入專案先離線核對 adapter、payload／scope、輸出及錯誤映射，再依該專案已授權資料與資源做有界 live 驗收：catalog／explain、一次非敏感文字提交、新程序沿原 key 取回結果，以及敏感專案拒絕 `cloud_only`。不得把要求 Quota 文件當作該專案的 live 授權；本次 Playbook 更新沒有執行這些模型呼叫。

2026-11-14 Broker 驗收只涵蓋 RTX 4090 固定 `Qwen/Qwen3.5-4B`、文字／單張 inline PNG（≤1 MiB、寬高各 ≤1024）、輸出 ≤1024 tokens 及回覆遺失恢復。冷啟動含模型載入與 warmup；逾時仍查原 key。Spark 128 GB、ASR／embedding／rerank、串流、其他模型／OS、雙併發品質、整機重啟自動恢復、異機災難復原與長期 SLA 均不在完成聲明內；詳情以固定驗收手冊為準。

Calcifer 或其他 Node／代理框架日後接入需有自己的 adapter、輸入輸出與 scope 映射及驗收；設定 `base_url` 不會直接完成。這份共用交接**不表示 Calcifer 已接入**，不開發其 adapter、不改 Codex／agy 訂閱路由，也不變更其既有 Phase 0。

Codex 查閱入口與跨專案操作界線見[服務指南](../guides/service-integration.md#api-配額與供應商路由api-quota-broker)；本文件會隨固定指南 Markdown 快照安裝，SDK、token 與服務不由 Playbook 安裝器配送。
