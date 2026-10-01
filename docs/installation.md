# 跨裝置安裝與更新

每台執行 Codex 的環境各自安裝。Windows 原生、WSL、macOS、Linux、SSH 主機及容器都獨立解析；同步來源 repo 即可，不跨機複製已渲染的 AGENTS.md、.venv 或設定目錄。

## 定位與前置條件

- 已安裝 Git、uv；Python 3.11 以上由既有相容環境或 uv 提供。程式只使用標準函式庫，沒有額外套件。
- repo 位置由這次指定的位置／已登錄專案決定。安裝程式從自己的檔案位置找到 repo，不依賴 cwd、PROJECTS_ROOT 或固定磁碟。
- 安裝目的地優先序：明確 `--codex-home` → 執行端 `CODEX_HOME` → Python 原生 `Path.home()` 下的 `.codex`。Windows 主目錄由作業系統環境解析，不假定 C 槽；已指定目的地必須是原生絕對路徑，可含空白及中文。
- `PROJECTS_ROOT` 只協助找專案，不決定 Codex home。GUI App 與終端的環境可能不同，執行前核對 App 實際使用的目錄；必要時用 `--codex-home` 明確指定。不修改系統變數。
- 不接受含未展開變數的相對路徑、Windows drive-relative 路徑或在 POSIX 上使用 Windows 路徑。UNC 可由 Windows 原生解析，但網路檔案系統的權限／替換行為需另外驗證。

## 一次安裝流程

先進入已確認的 repo。核對 `git status --short`、`git remote -v` 及目前分支，確定沒有其他 task 正在使用；不要自動清掉修改或切換別人的分支。正式更新時，取得已合併的 main，核對預期 SHA，再執行。

macOS／Linux（Bash／Zsh）：

```sh
git fetch origin
git switch main
git merge --ff-only origin/main
playbook_commit="$(git rev-parse HEAD)"
uv run --locked python scripts/install.py --commit "$playbook_commit"
# 核對預覽的 target、source_commit、snapshot，將下方 SHA256_OR_missing 換成 current_sha256。
uv run --locked python scripts/install.py --commit "$playbook_commit" --expect-current-sha256 SHA256_OR_missing --apply
```

Windows（PowerShell）：

```powershell
git fetch origin
git switch main
git merge --ff-only origin/main
$playbookCommit = (git rev-parse HEAD).Trim()
uv run --locked python scripts/install.py --commit $playbookCommit
# 核對預覽後，將下方 SHA256_OR_missing 換成 current_sha256。
uv run --locked python scripts/install.py --commit $playbookCommit --expect-current-sha256 SHA256_OR_missing --apply
```

以上命令逐步檢查成功後才繼續；只在自己可用的乾淨目錄切換 main。`SHA256_OR_missing` 是要替換的佔位值。已獲安裝授權的代理可自行核對預覽、帶入 hash 並套用，不必再次詢問。

目的地不同時，兩次命令都加相同的 `--codex-home "實際絕對目錄"`。例如 PowerShell 可用 `--codex-home (Join-Path $HOME '.codex')`，Bash／Zsh 可用 `--codex-home "$HOME/.codex"`。不把範例當成已核對的 App 設定。

## 保護、驗證與限制

- 不加 `--apply` 只讀取並預覽，不寫 Codex 設定。uv 自身可能準備專案 Python 環境。
- 來源須乾淨、HEAD 等於指定完整 SHA；套用時還須在本機已取得的 `origin/main` 歷史中。不自行 fetch、切分支、合併或修改模型設定。先由操作者核對遠端可信度及版本。
- `AGENTS.override.md` 存在或 config.toml（含 profiles）另有指示來源時停止，交由操作者查明；不刪除或繞過它。App 啟動參數／管理端政策仍需在實際客戶端核對。
- 首次安裝支援不存在的 AGENTS.md；更新時將原檔完整備份到 `backups/`。以固定 commit 建立 Markdown 快照，核心嵌入此裝置的快照絕對路徑。既有同名快照不同就停止。
- 安裝使用排他鎖防止本安裝程式互撞；替換前再次核對原檔與指示來源，使用同目錄暫存檔及 `os.replace`。不要同時用其他編輯器修改 AGENTS.md；一般檔案 API 無法保證對不合作外部寫入者的絕對原子比較交換。
- 同版本、同目錄、同內容重跑不產生新備份；若快照損壞仍停止。備份與舊快照保留，清理另行授權。
- 不跟隨受管理檔案、快照或備份目錄的 symlink／junction；Windows 對受管理位置的 reparse point 一律停止，Python 3.11／3.12 都適用。不處理作業系統 ACL 遷移：POSIX 保留 mode，Windows 使用目的地目錄繼承權限；有特殊 ACL 時先人工核對。
- 安裝程式核對落地內容，沒有修改 Codex 指示容量限制。核心約 8 KB，實際有效上限及其他專案指示仍由使用中的客戶端決定。
- 成功後新開工作階段，確認讀到來源 SHA、快照位置及模型指南。既有對話不保證自動重載；既有模型／effort 設定不會因此切換。

## 回復與測試

回復依 [README](../README.md#回復)。使用舊 commit 重裝時，先在可用的乾淨 repo checkout 已確認的舊版本，再用該版本自己的安裝方式；安裝程式不是任意版本自動遷移器。

```sh
uv run --locked python -m unittest discover -s tests -v
```

CI 對 Linux、macOS、Windows 執行相同測試。這驗證原生檔案操作及臨時 Codex home，不代表在三種平台的 Codex App 都完成實際載入，也不保證所有 UNC／網路掛載行為。
