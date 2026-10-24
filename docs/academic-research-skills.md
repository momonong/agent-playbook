# 六項學術研究技能

2026-10-24 已在一台原生 Windows 環境完成六項技能的固定來源獨立安裝及有界離線檢查。本回合 Codex 提供的技能清單已列出六個名稱，確認該客戶端已發現；UI 選單人工驗收、真實研究品質及完整 ARS 流程仍未完成。

這批技能**尚未加入共用安裝器**：[skills/manifest.json](../skills/manifest.json) 仍是七包、138 檔，`--with-skills` 不會安裝或更新下列六包。本次只將來源、用途、授權、依賴及既有證據寫入文件；完整快照與逐檔 manifest 留在本機獨立交付，不把約 40 MB payload、裝置 receipt 或設定放進 Git。跨裝置納管仍待另行完成，不放寬現有 manifest 的普通 `100644` 檔案、完整樹及衝突保護。

## 固定來源與用途

三個來源均固定完整 commit，不追蹤 `main`／latest：

| 來源 | 完整 commit | 根授權原文 |
|---|---|---|
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills/tree/593377bb048752abb0152deab9fbb1083a6087df) | `593377bb048752abb0152deab9fbb1083a6087df` | [MIT，LICENSE.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/593377bb048752abb0152deab9fbb1083a6087df/LICENSE.md) |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs/tree/773a52944ba4747a18bd4ae9ade53fff041adcbc) | `773a52944ba4747a18bd4ae9ade53fff041adcbc` | [MIT，LICENSE](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/LICENSE) |
| [Imbad0202/academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex/tree/71528d9349bcdacfbe94111f06d9e2d82215a44d) | `71528d9349bcdacfbe94111f06d9e2d82215a44d` | [CC BY-NC 4.0，LICENSE](https://github.com/Imbad0202/academic-research-skills-codex/blob/71528d9349bcdacfbe94111f06d9e2d82215a44d/LICENSE) |

下表子目錄均位於對應固定 commit；檔數含每包追加的一份同 commit 根授權原樣副本，原內嵌授權及註記全部保留。

| 技能 | 主要用途 | 固定來源子目錄 | 檔數 |
|---|---|---|---:|
| scientific-critical-thinking | 檢查研究設計、偏差、統計解讀與證據強度 | K-Dense：[`skills/scientific-critical-thinking`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/593377bb048752abb0152deab9fbb1083a6087df/skills/scientific-critical-thinking) | 10 |
| scientific-writing | 科學稿件草擬／修訂、報告規範、作者責任與本機一致性檢查 | K-Dense：[`skills/scientific-writing`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/593377bb048752abb0152deab9fbb1083a6087df/skills/scientific-writing) | 32 |
| citation-management | 文獻資料檢索、引用核驗及 BibTeX 整理 | K-Dense：[`skills/citation-management`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/593377bb048752abb0152deab9fbb1083a6087df/skills/citation-management) | 23 |
| brainstorming-research-ideas | 以結構化框架發想、篩選可檢驗的研究方向 | Orchestra：[`21-research-ideation/brainstorming-research-ideas`](https://github.com/Orchestra-Research/AI-Research-SKILLs/tree/773a52944ba4747a18bd4ae9ade53fff041adcbc/21-research-ideation/brainstorming-research-ideas) | 2 |
| ml-paper-writing | ML 論文論證、段落、引用工作流與會議模板 | Orchestra：[`20-ml-paper-writing/ml-paper-writing`](https://github.com/Orchestra-Research/AI-Research-SKILLs/tree/773a52944ba4747a18bd4ae9ade53fff041adcbc/20-ml-paper-writing/ml-paper-writing) | 52 |
| academic-research-suite（ARS-Codex 3.23.1） | 研究問題、規劃、文獻、寫作、修訂及審查的路由入口 | ARS：[`skills/academic-research-suite`](https://github.com/Imbad0202/academic-research-skills-codex/tree/71528d9349bcdacfbe94111f06d9e2d82215a44d/skills/academic-research-suite) | 2,640 |

重建來源時只取上述完整子樹及同版根授權，不複製上游整個設定目錄。K-Dense 三包各補 `LICENSE.md`，Orchestra 兩包及 ARS 各補 `LICENSE`；`ml-paper-writing` 的會議模板仍適用其內嵌原授權，不能用根 MIT 取代。安裝前核對完整 Git tree、逐檔 blob／SHA-256、原始 mode 及目的地衝突；實際套用仍須該裝置的安裝授權。

## 依功能核對 runtime

六項核心文字指引以讀取 `SKILL.md` 及必要參考為主，不要求先執行全部程式或連接服務。程式化功能另按所選路徑核對：

| 技能／功能 | runtime、依賴與界線 |
|---|---|
| scientific-critical-thinking、brainstorming-research-ideas | 核心文字工作無額外 runtime；前者提到的 `scientific-schematics` 圖表能力是另選技能及外部服務，本輪未安裝／啟用。 |
| scientific-writing 本機 CLI | Python 3.11+ 標準函式庫；隨包 CLI 無網路或 API key 需求。 |
| citation-management | helper 宣告 Python 3.9+、`requests`；部分 Google Scholar 路徑另需 `scholarly`。OpenAlex、Crossref、PubMed、DOI 等線上核驗需要網路；服務識別、配額或 key 按實際供應商核對。離線整理成功不證明文獻存在。 |
| ml-paper-writing | 上游宣告 `semanticscholar`、`arxiv`、`habanero`、`requests`；它們用於選定的程式化檢索／引用路徑，非本次文字演練的前置。Exa MCP 為建議的可選搜尋方式；編譯模板另需合適 TeX 工具，Overleaf 為可選外部服務。 |
| ARS 選定 helper | 依腳本核對 Python／uv；PDF 結構 preflight 可需 `pypdf`，明確選用的內容分類器需 `pdf-inspector==0.2.6`。開發／測試依賴列在 `ars/requirements-dev.txt`，未在本次安裝；外部模型、書目 API、hooks 及完整 runtime 均未啟用。 |

本次原生 Windows 使用 PowerShell 7.6.5、Python 3.14.0；既有 Python 有 `requests`，未新增套件，`scholarly`、`semanticscholar`、`arxiv`、`habanero` 未安裝。這不是 Python 3.9／3.11 或其他 OS 的執行證據。所有 Python 呼叫使用實際技能路徑與 `python -B`，避免在技能目錄產生 bytecode；上游 33 個 `100755` mode 已記在獨立 manifest，Windows 不宣稱重建 POSIX 執行權限。

ARS 只將 root `SKILL.md` 註冊為技能；`ars/**/WORKFLOW.md` 由 router 按需讀取，不額外註冊為數十個技能。未複製 repo 根 `.codex/config.toml`，未改模型、effort、插件或持久環境。上游對原生 Windows 僅列 best-effort，CI 為 Ubuntu；inquiry ledger alpha 明確不支援 Windows，本次未執行。詳見[同版 ARS README](https://github.com/Imbad0202/academic-research-skills-codex/blob/71528d9349bcdacfbe94111f06d9e2d82215a44d/README.md)。

## 已有證據與未驗證範圍

本機獨立交付含 `packages/`、`manifest.json`、`installation-receipt.json`、`INSTALLATION.md`、`synthetic-guidance-checks.md`、`cli-smoke/report.md` 與逐命令 `smoke-results.json`／stdout／stderr；這些裝置資料不屬本 repo。可分享的內容識別為：

- 六包共 **2,759 檔、40,331,844 bytes**：2,753 原檔加六份根授權副本。
- 獨立 manifest SHA-256：`4afda93a07fb3c4e4f68f5c3e780ab826f53ed4a7dc54fd91c94038011a1c5d1`。
- 套件集合內容摘要：`41d34b5fcf76676da7bb6191c30636c672653b2a3d9b660f714d1a3ff2bea66e`。
- 六包完整檔案集合、SHA-256 與固定 Git blob 安裝後及測試後核對一致，無新增快取。當輪受保護的既有設定、核心、技能、receipt 及固定指南共 247 檔，前後 hash 不變；不公開其本機檔案清單。

| 驗證層 | 已核對內容 | 限制 |
|---|---|---|
| 三項文字演練 | critical-thinking 的合成證據評讀、brainstorming 的三個可證偽方向、ml-paper-writing 的缺口及段落 | 從固定來源磁碟讀取規則；不是研究有效性、novelty、真實引文核驗或 TeX／PDF 編譯證據。 |
| 原生 Windows CLI | 實際安裝路徑、含中文／空白 cwd；**10 個命令、69 個斷言通過** | scientific-writing 4 次、citation-management 3 次、ARS planner 3 次；包括未完成稿、重複寫入及無效引用的預期非零拒絕，未執行真實 DOI／搜尋服務。 |
| ARS 入口 | `ars-plan`、`ars-outline`、`ars-citation-check` 的離線路由及必要檔案；另完成合成 `ars-plan` 演練 | planner 為 planned-only；quality gates、team dispatch、hooks、full runtime 均未執行，文字演練停在人工設定確認。 |
| 客戶端發現 | 本次對話的 Codex 技能清單已列出六個 root 名稱 | 更新發現判定，原收據保留當時的 pending 狀態；不代表 UI 選單人工接受、自動觸發品質、其他裝置或完整研究工作流通過。 |

上述測試全部使用明確合成資料，沒有真實研究資料或未發表稿件；未呼叫外部 API／模型、啟用 hooks、訓練或啟動研究。安裝檔案、客戶端發現、局部功能、研究品質與人工接受須分開回報。

## 明確使用入口

在需要的原目標對話中明確指定技能與停止點，例如：

| 目的 | 可用提示 |
|---|---|
| 評讀證據 | `使用 $scientific-critical-thinking，檢查以下研究設計的偏差、獨立觀測單位與尚缺證據。` |
| 修稿 | `使用 $scientific-writing，逐項列出這份方法段落的缺件，先不要整篇改寫。` |
| 整理引用 | `使用 $citation-management，先離線整理這份 BibTeX；把需要線上核驗的項目另列待辦。` |
| 發想方向 | `使用 $brainstorming-research-ideas，根據已提供的失敗案例提出三個可證偽方向，標示未核對文獻。` |
| ML 論文 | `使用 $ml-paper-writing，依現有證據整理貢獻、論證與缺口，不補造引用。` |
| ARS 規劃 | `使用 $academic-research-suite，ars-plan 幫我整理研究問題與缺少的證據，先停在規劃。` |

ARS 的 plain alias 可避免客戶端攔截 slash command；`ars-plan` 等不是額外安裝的原生 `/ars-*` 指令。這些例子不自動授權新實驗、外部供應商、私人稿件上傳、全域依賴或跨裝置同步；執行時沿用既有目標與當次授權。

## 授權對研究用途的差別

五項 MIT 技能允許商業使用；分發副本或重要部分時，保留版權及授權聲明。內附模板或其他第三方內容仍依各自原授權。[MIT 官方原文](https://opensource.org/license/mit)

ARS 使用 CC BY-NC 4.0，可在非商業目的下重製、分享及改作；公開分享受授權內容時，保留適當署名、授權連結與修改標示。NC 判斷看實際使用是否主要為商業利益或金錢報酬，**不只看使用者是大學還是公司**。[CC 正式條款第 1、2、3 節](https://creativecommons.org/licenses/by-nc/4.0/legalcode.en)、[CC 官方 NC FAQ](https://creativecommons.org/faq/#does-my-use-violate-the-noncommercial-clause-of-the-licenses)

實務上，以非商業學術目的進行學位研究、論文草擬或投稿，通常較符合 NC；企業委託、產學合作、收費研究服務或商品研發，須檢查具體目的與契約，不能因隸屬大學或成果會公開就直接判定可用。這是條文解讀，未替個別計畫作法律判定；不明確時向 ARS 權利人確認額外授權，或請校方法務確認。[CC 官方 NC FAQ](https://creativecommons.org/faq/#does-my-use-violate-the-noncommercial-clause-of-the-licenses)

僅使用工具不會自動要求公開私人研究資料、論文或程式，也不會使所有產出自動改為 CC BY-NC。若將 ARS 受保護文字／模板直接複製或改作進產出，則須按受授權內容及分享方式檢查條件；安裝成功不代表未來所有用途都已取得授權。[CC 正式條款的適用範圍與改作定義](https://creativecommons.org/licenses/by-nc/4.0/legalcode.en)
