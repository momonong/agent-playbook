# 跨裝置安裝與更新

以同一個已合併、固定完整 commit，將核心、指南快照與可選的個人技能安裝到每台執行環境。`git clone`／`git pull` 只取得來源，**不會自動套用**。只需要核心文字時，仍可直接複製 [instructions/codex.md](../instructions/codex.md) 到 Codex 個人指示。

每台裝置的承接對話、同步範圍與可複製開場指示見[裝置同步契約](device-sync.md)。本文是安裝命令與保護規則的唯一完整入口；文件本身不授權 Git、全域安裝或外部操作。

## 定位與前置條件

- 需要 Git、Python 3.11 以上；安裝器只用標準函式庫。既有環境建議 uv 與 lock，新裝置也可將下方 `uv run --locked python` 換成已確認的 `python`／`python3`。缺 Git／Python 先回報並由裝置對話依授權處理；不自動安裝全域 runtime、npm 套件或執行技能程式。
- 沿用已確認／登錄的 repo。安裝器由自身位置找到 repo，不依賴 cwd；來源必須乾淨、HEAD 等於指定的完整 40 字元 SHA，apply 還要求它位於本機已取得的 `origin/main` 歷史中。不自行 fetch 或選 latest。
- Codex home：明確 `--codex-home` → 執行端 `CODEX_HOME` → 原生 `Path.home()/.codex`。先核對客戶端實際位置；GUI 與終端可能不同。`PROJECTS_ROOT` 不決定設定位置。
- 技能位置：明確 `--skills-home` 優先；否則核對原生主目錄下 `.agents/skills` 與目前 Codex home 下 `skills`。已有個人技能時沿用該位置；兩處都有個人技能就停止，要求明確選擇。全新環境採官方 `.agents/skills`。不重複安裝或搬移舊位置。
- 明確路徑須為執行端原生絕對路徑，可含空白／中文；不接受相對路徑、未展開變數或把 Windows 路徑交給 POSIX。Windows、WSL、SSH、容器各自解析，不複製整個 `.codex`、`.agents` 或 `.venv`。

## 一次安裝流程

先核對 `git status --short --branch`、`git remote -v`、實際 HEAD 與使用中的任務。只在自己可用的乾淨目錄切換 main；不清除其他人的變更。新裝置先在已授權位置 clone `https://github.com/momonong/agent-playbook.git`，再進入 repo；既有裝置沿用原目錄。

以下同時安裝核心、指南與七份受管技能。要只沿用舊的核心安裝介面，移除三次命令的 `--with-skills` 及 apply 的 `--expect-skills-sha256` 即可。Superpowers 官方插件另依下方逐裝置核對，不由這些命令安裝。

macOS／Linux（Bash／Zsh）：

```sh
git fetch origin
git switch main
git merge --ff-only origin/main
playbook_commit="$(git rev-parse HEAD)"
uv run --locked python scripts/install.py --commit "$playbook_commit" --with-skills
# 核對預覽，將 CORE_SHA256_OR_missing 換成 core.current_sha256；
# SKILLS_STATE_SHA256 換成 skills.skills_state_sha256。
uv run --locked python scripts/install.py --commit "$playbook_commit" --with-skills --expect-current-sha256 CORE_SHA256_OR_missing --expect-skills-sha256 SKILLS_STATE_SHA256 --apply
uv run --locked python scripts/install.py --commit "$playbook_commit" --with-skills --check
```

Windows（PowerShell）：

```powershell
git fetch origin
git switch main
git merge --ff-only origin/main
$playbookCommit = (git rev-parse HEAD).Trim()
uv run --locked python scripts/install.py --commit $playbookCommit --with-skills
# 核對預覽後，帶入 core.current_sha256 與 skills.skills_state_sha256。
uv run --locked python scripts/install.py --commit $playbookCommit --with-skills --expect-current-sha256 CORE_SHA256_OR_missing --expect-skills-sha256 SKILLS_STATE_SHA256 --apply
uv run --locked python scripts/install.py --commit $playbookCommit --with-skills --check
```

每一步檢查成功才繼續；兩個大寫 hash 名稱是命令佔位值。已獲安裝授權的代理自行核對預覽並帶入實際 hash，不再要求相同批准。目的地不同時，三次安裝器命令帶相同 `--codex-home`／`--skills-home`。可使用 shell 已展開的原生絕對目錄，例如 PowerShell 的 `(Join-Path $HOME '.agents/skills')` 或 Bash 的 `"$HOME/.agents/skills"`；先核對客戶端，不將範例當成實際位置。

若 uv cache 所在位置因沙箱而唯讀，可將 `UV_CACHE_DIR` 指向當次允許的暫存目錄；這只處理 uv 的 cache，不更動安裝目的地，也不繞過目的地批准。

## 預覽、check 與狀態

沒有 `--apply` 不寫安裝目的地；`--check` 是唯讀核對，不修復任何內容。uv 自身可能準備專案 Python 環境。兩者都不執行技能 payload；runtime 只允許固定的 `node/python/uv/git --version` 探測。

核心輸出來源 `source_commit`、指南 `guides_commit`、目標、當前／預期 SHA-256 及 `snapshot_status`。check 只有核心 bytes 與完整指南快照均相符才將核心列為 matching；快照遺失或損壞不能當完成。

| 技能狀態 | 意義與處理 |
|---|---|
| `missing` | 目的地不存在，apply 可新增 |
| `matching` | 檔案與 receipt 均已受管且吻合 |
| `adopt` | 未受管同名技能的完整內容恰好等於目標；apply 僅登錄 receipt |
| `adopt_with_licenses` | 完整內容恰好等於 manifest 核對過的舊原版，只補指定頂層授權文字，先備份 |
| `update` | 受管內容仍等於上次 receipt，apply 可備份後更新 |
| `conflict` | 未受管內容不同，或受管內容被本機修改；全部 preflight 後停止，不覆蓋 |
| `unmanaged` | 其他技能只列名稱，保留原內容；內建／插件不納管 |
| `disabled` | 該技能在本機 `skills.config` 明確停用；檔案可安裝，但環境未完成 |
| `requires: missing/too_old/unknown` | 必需 runtime 缺少、版本不足或無法確認；可先安裝檔案，不能宣稱可執行 |

`--check` 回傳 0 表示本次範圍的檔案、receipt、已知 enable 狀態與必需 runtime 相符；回傳 2 表示還有上述差異，回傳 1 表示來源／保護檢查失敗。apply 回傳 2 表示檔案步驟已完成，但停用／runtime 條件未滿足；看輸出再處理，不盲目重跑。`client_discovery: pending_client_verification` 永遠另列：檔案成功不代表客戶端已發現、能呼叫技能或已通過人工驗收。`allow_implicit_invocation: false` 是上游明確呼叫設定，不等於 disabled。

成功 apply／check 的重點欄位如下（省略版本、hash、備份與其他技能；實際輸出均會保留）：

```json
{"mode":"apply","status":"installed","core":{"verified":true},"skills":{"verified":true,"ready":true,"client_discovery":"pending_client_verification"}}
{"mode":"check","core":{"matching":true,"snapshot_status":"matching"},"skills":{"ready":true,"skills":[{"name":"grill-me","status":"matching","disabled":false}],"client_discovery":"pending_client_verification"}}
```

## 技能來源與能力界線

[skills/manifest.json](../skills/manifest.json) 固定七包來源 commit、適配狀態、每檔 SHA-256、授權及必需依賴，內容位於 `skills/packages/`；套用只讀指定 Git commit，不信任工作樹草稿，也不抓上游 latest。套件完整性與授權說明見[技能清單](../skills/README.md)。新增可共用技能的已授權安裝任務，須把來源、版本、授權、依賴、快照與 manifest 一起交付；只做本機實驗時明示不納管。

六項學術技能的本機獨立安裝另見[學術技能文件](academic-research-skills.md)，尚未納入上述 manifest；本安裝器不安裝、更新或核驗它們。其獨立 manifest／receipt 不能當成安裝器受管狀態，`--with-skills --check` 也不證明六包完整性、客戶端發現或功能。未來共用納管仍須完成相應交付，不放寬現有 `100644`、完整樹、CAS 或衝突檢查。

| 技能 | 必需／額外能力 |
|---|---|
| answer-me-with-html | 基本 HTML 需要 Node 20+；影片需要 Node 22+ 與 Chrome／Chromium／Edge，MP4 另需 ffmpeg |
| design-taste-frontend | 完整 inspect／scenes 需要 Node 22+ 與上述瀏覽器；draw／lint／assets 的上游最低版本是 Node 18，但共用完整工作流採 22+ |
| grill-me、grilling | 無額外 runtime；前者依賴後者，保留上游 metadata |
| career-profile-builder | 無額外 runtime；保留目前已確認適配，不納入履歷或私人職涯資料 |
| ui-ux-pro-max | Python 標準函式庫及隨包資料；完整 payload 靜態下限 3.9，共用安裝環境仍為 3.11+；純查詢可離線，不需 pip／API key |
| caveman | 基本純文字技能，無額外 runtime／兄弟技能依賴；只同步 README、SKILL 與三份授權文字 |

安裝器的 runtime 探測不保證瀏覽器、外部字型／圖片網路、影片輸出、客戶端工具或服務可用；依實際使用場景另核對。HTML 技能上游有更新檢查及可選 TTS／影片行為，同步不執行或授權這些外部呼叫，不複製環境變數或憑證。

內建與插件技能不 vendor、不複製 cache、不承諾插件版本一致。每台裝置按已授權功能核對實際客戶端的插件／瀏覽器工具及連線狀態；若需新增、登入或接外部服務，依該次授權處理。

### Superpowers 官方插件

使用者已選擇採用 Superpowers，走 Codex 官方插件目錄；在當台客戶端的 Coding 分類或正式搜尋中核對 `superpowers`／顯示名稱 `Superpowers` 與作者來源，再在該機安裝授權內安裝。流程參照[作者的 Codex App 說明](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/README.md#codex-app)；此固定 commit 僅作相容性審查來源，不代表目錄提供或各機已裝的插件必為同版。

每台分別回報是否可取得、已安裝、已啟用、可取得的版本，以及客戶端實際技能入口；搜尋顯示可安裝、建議卡片或其他裝置裝好都不等於本機安裝完成。缺少入口或無法確認時明列未驗證，不複製其他裝置的插件 cache／hook 或改用手動 vendor 充當成功。本 repo 與安裝器不安裝插件；`--with-skills --check` 只核對七份檔案技能，不能驗證 Superpowers。

Superpowers 的工作流依[合作指南](../guides/collaboration.md#superpowers-與-caveman)接入既有授權、模型分工及驗證原則。它不授權額外服務、Git 操作、worktree 或清理，也不改本機模型／effort／插件設定。基本 Caveman 的聊天模式由使用者在所需對話呼叫，依上游會話規則持續至停止；同步不強制所有對話啟動，不安裝其 CLI、Proxy、Auto、hook、兄弟模式或改寫啟動設定。

### ui-ux-pro-max 的本機查詢

上游 `SKILL.md` 保留 Claude 的 `${CLAUDE_PLUGIN_ROOT}/.claude/...` 範例。Codex 執行時先從實際載入的 `SKILL.md` 所在目錄，或已核對安裝預覽的 `skills.skills_home` 定位 `ui-ux-pro-max`；不假設 Claude 變數存在，也不在專案建立 `.claude` 目錄。以下 `skills_home`／`skillsHome` 必須先設為該預覽輸出的原生絕對路徑，並使用本環境已確認的 Python 3.11+。

macOS／Linux（Bash／Zsh）：

```sh
skill_dir="$skills_home/ui-ux-pro-max"
test -f "$skill_dir/scripts/search.py" || exit 1
python3 -B "$skill_dir/scripts/search.py" "keyboard focus modal" --domain ux --json
```

Windows（PowerShell）：

```powershell
$skillDir = Join-Path $skillsHome 'ui-ux-pro-max'
$searchScript = Join-Path $skillDir 'scripts/search.py'
if (-not (Test-Path -LiteralPath $searchScript -PathType Leaf)) { throw '找不到已核對的技能腳本' }
python -B $searchScript 'keyboard focus modal' --domain ux --json
```

已確認使用 Python Launcher 的 Windows 可將 `python -B` 換成 `py -3 -B`。`-B` 防止 Python 在受管技能目錄產生 `__pycache__`；完整樹同步仍拒絕額外檔案，不新增忽略例外。資料依腳本自身位置解析，查詢可從任意 cwd 執行；無 `--persist` 時僅輸出結果，不寫設計稿、不連網。完整包的 3.9 靜態下限不代表已在原生 3.9 執行驗證。

需要保存設計稿時才加 `--design-system --persist --output-dir`，`--output-dir` 指向已授權專案的明確原生絕對路徑；先讀現有 `design-system/<project-slug>/MASTER.md`，未獲覆寫授權不加 `--force`。同步本身不執行保存、刷新資料或上游維護腳本。與 taste 的互補及既有專案設計決策見[技能能力說明](../skills/README.md#能力與未驗證範圍)，不要求每次重跑兩套完整流程。

## 備份、衝突與回復

- 保留原核心的 override／指示來源檢查、乾淨固定來源、原樣複製、快照驗證及 hash CAS。`AGENTS.override.md` 或 config（含 profiles）指定其他指示來源時停止，不刪除或繞過。
- 核心更新完整備份到 Codex home 的 `backups/`，同目錄暫存檔及 `os.replace` 安裝。指南按核心首行 commit 放 `agent-playbook/versions/<guides_commit>/`，已有不同內容就停止；技能 Markdown 不混入指南快照。
- 技能 receipt 在 Codex home 的 `agent-playbook/skills-receipt.json`，只含位置、來源與檔案 hash。技能更新／授權檔補齊前，先將所有受影響技能備份到 `agent-playbook/skill-backups/<UTC時間>/` 並驗證；原 receipt 也保存。核心與技能各有鎖，過期鎖需查明，不能自動刪除。
- 預覽後核心 bytes 或技能目錄／receipt／已知停用狀態變更，CAS 拒絕。未受管同名目錄只有完整 bytes 相符才採用；`adoption_files` 例外只允許精確核對過的原 tree，目標只新增頂層 `LICENSE`、`NOTICE`、`THIRD_PARTY_NOTICES`（可帶 `.txt`／`.md`）純文字。額外檔案、空目錄或任何原檔修改均為衝突。
- `ui-ux-pro-max` 新機為 `missing`；已有相同 74 檔且無額外內容時為 `adopt`，apply 只登錄受管 receipt；已有同版受管內容則為 `matching`。舊安裝的 `INSTALL_SOURCE.json` 是本機歷史資料，不是共享 payload；存在時仍為 `conflict`。裝置承接者須先核對並在相應授權內將該收據原樣原子移到技能目錄外的本機備份、驗證 hash，再重新預覽取得新的 CAS；不提交、同步、刪除或由安裝器自動排除。其他本機修改或額外檔案仍需個別處理，不能套用收據搬移作通用忽略規則。
- 受管更新也須先等於上次 receipt；本機修改保留並交由使用者決定如何納回來源。manifest 移除技能不刪目的地或歷史 receipt。未納管、system、插件、其他設定與執行狀態保持原狀。
- 受管檔案、技能、快照、receipt 與備份路徑不接受 symlink／junction；Windows 3.11／3.12 的 reparse point 都停止。不遷移 OS ACL，特殊 ACL／UNC／網路檔案系統需另行驗證。
- 核心與技能是分開的提交步驟，**不是整批原子交易**。全體衝突先檢查；核心已成功而技能失敗時明報 `status: partial`。receipt 提交前技能替換失敗會回復技能；回復本身失敗會保留復原目錄並明報。receipt 提交後的驗證失敗保留同版技能與 receipt，明報未完成驗證，不假稱全部回復。
- 檔案 API 與鎖不能保證對不合作外部寫入者的絕對原子 CAS；安裝時不要用其他編輯器修改受管目標。同版同內容重跑不增備份，備份／舊快照不自動清理。

回復取得當次授權後，先保存現況，再核對選定備份、receipt、版本及範圍。核心依 [README](../README.md#回復) 原子恢復；技能從已驗證的完整備份回復，或在乾淨 repo checkout 指定舊版本並依當版流程重裝，不把舊安裝器當任意版本遷移器。不在回復時移除其他規則、改模型或清理資料。

## 客戶端核對與測試

完成後新開工作階段核對指南 SHA、核心讀取、技能清單／明確呼叫入口及當次需要的瀏覽器能力。既有對話不保證重新載入；本機檔案、客戶端發現、功能執行與人工接受分別回報。主對話模型、effort、速度、插件設定及暫停狀態不由安裝器修改。

```sh
uv run --locked python -m unittest discover -s tests -v
```

既有 CI 在 Linux／macOS／Windows、Python 3.11／3.12 跑同組測試，含臨時目的地、CAS、備份、失敗回復、未納管內容、兩台一致及原生路徑保護。只回報實際通過 runner；本機或模擬測試不代表其他平台 Codex App、瀏覽器或人工驗收已完成。

直接貼上模式不需要 Python／uv／Git；離線安裝則須本機物件庫已取得核心、釘選指南及技能來源 commit。淺層 clone 缺歷史時先核對來源，再取得確切版本，不用 HEAD／main 指南取代。指南先提交、核心再釘選；快照內歷史核心不能覆蓋新的外層核心。
