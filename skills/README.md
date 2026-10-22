# 共用個人技能快照

這裡保存六份已確認的可重用技能；`manifest.json` 是安裝器的唯一技能清單，`packages/` 是固定內容。安裝命令及衝突處理只在[跨裝置安裝文件](../docs/installation.md)維護。不含私人履歷、設定、憑證、聊天、快取或技能歷史；內建／插件技能由各客戶端核對，不 vendor。

| 技能 | 固定來源 | 本次內容 |
|---|---|---|
| answer-me-with-html | [QingYunA，7e71bc08](https://github.com/QingYunA/answer-me-with-html/tree/7e71bc08f3df214af10fe4636fd00f95294ec3e9/skills/answer-me-with-html) | v0.5.5 原始五檔，追加 root LICENSE／THIRD_PARTY_NOTICES |
| design-taste-frontend | [Leonxlnx，6010f91a](https://github.com/Leonxlnx/taste-skill/tree/6010f91a9935f1c167dfc500fb1a475681892e6b/skills/taste-skill) | 原始 38 檔，以本地技能名稱保存，追加 LICENSE |
| grill-me、grilling | [mattpocock，5beb35b0](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/productivity) | 兩個原版入口各兩檔，保留 explicit invocation metadata，各追加 LICENSE |
| career-profile-builder | [vignzpie，d21f62ec](https://github.com/vignzpie/resume-agent-skills/tree/d21f62ec07966a6f9b7963c5d1d8c736265d8393) | 已確認本機適配七檔，保留原 LICENSE、upstream 原文、問答及編輯指南 |
| ui-ux-pro-max | [nextlevelbuilder，076a2b3a](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/076a2b3a31394ad788afaa71f55d0bf789e7b3ec/.claude/skills/ui-ux-pro-max) | 上游技能子目錄 73 檔，加同 commit 根目錄 LICENSE，共 74 檔原樣保存，含資料及測試快照 |

2026-10-22 核對的原始 54 檔共 3,436,700 bytes，功能內容維持原樣；四包補 LICENSE，HTML 再補完整第三方授權文字，共 59 檔。taste 的固定 commit 與當前 38 檔 Git blob 完全相符，但不推定它就是當初安裝來源。career 完整原樹以 manifest `source.revision` 的 `sha256:` 內容摘要識別，`upstream_revision` 只標上游來源，不把適配包稱作上游原版。每個落地檔案仍由 `files` 的 SHA-256 逐一核對。

2026-10-23 納入既有 `ui-ux-pro-max` 的 74 個可共用檔案，共 3,584,054 bytes；逐檔與上述固定上游及 LICENSE 比對，保留全部 bytes，不改 SKILL、程式或資料。原五包與其 manifest 項目不變，現為六包、133 檔。原技能目錄的第 75 檔 `INSTALL_SOURCE.json` 是本機歷史安裝收據，不進共享快照或 manifest，也不由安裝器忽略或刪除；既有裝置的保存及採用流程見[安裝文件](../docs/installation.md#備份衝突與回復)。

## 授權與完整性

五個上游均為 MIT，完整授權附在各包 `LICENSE`。HTML 保留原 `licenses/OFL-Bangers.txt` 及 `am.mjs` 內嵌註記，並在 `THIRD_PARTY_NOTICES` 完整附上以下文字與來源，不修改程式：

- [HTML 上游 MIT](https://github.com/QingYunA/answer-me-with-html/blob/7e71bc08f3df214af10fe4636fd00f95294ec3e9/LICENSE)。
- [Dagre 固定 commit 的 LICENSE](https://github.com/dagrejs/dagre/blob/c3ed0802cd98de74c21cff1f754689ebbb0f8dae/LICENSE) 與 [bundle LEGAL](https://github.com/dagrejs/dagre/blob/c3ed0802cd98de74c21cff1f754689ebbb0f8dae/dist/dagre.esm.js.LEGAL.txt)。
- [Graphlib 固定 commit 的 LICENSE](https://github.com/dagrejs/graphlib/blob/d3a0cf36f55ebd75f28b6acf7a436a54e1b990dc/LICENSE)。
- [固定 HTML bundle 內的 Temml MIT／Apache parts 註記](https://github.com/QingYunA/answer-me-with-html/blob/7e71bc08f3df214af10fe4636fd00f95294ec3e9/skills/answer-me-with-html/scripts/am.mjs#L12409) 及完整 [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)。

其餘授權原文來源為 [taste MIT](https://github.com/Leonxlnx/taste-skill/blob/6010f91a9935f1c167dfc500fb1a475681892e6b/LICENSE)、[mattpocock MIT](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/LICENSE)、[career MIT](https://github.com/vignzpie/resume-agent-skills/blob/d21f62ec07966a6f9b7963c5d1d8c736265d8393/LICENSE)。taste 的外部圖片／字型清單是引用，實際取得素材的授權與署名仍按素材來源核對。

`ui-ux-pro-max` 的 [MIT LICENSE](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/076a2b3a31394ad788afaa71f55d0bf789e7b3ec/LICENSE) 取自同一 commit 的 repo 根目錄；`data/data-provenance.json` 與 `data/google-font-licenses.json` 原樣保存資料來源與字型授權中繼資料。查詢回傳的是建議與素材引用；實際使用外部字型或圖示仍核對其來源授權。

## Manifest 契約

`schema_version: 1` 的 `skills` 列表每項含：

- `name`、`path: skills/packages/<name>`、`source: {url, revision, license, ...}`。Git 原包用完整 commit；明示 `kind: locally-adapted` 的包用固定原樹 `sha256:` 加 `upstream_revision`。
- `files: {相對POSIX路徑: SHA256}` 宣告完整檔案集合。只接受普通 `100644` 檔案、跨平台路徑，拒絕 symlink、穿越、大小寫碰撞及未宣告檔案；本次沒有需 executable bit 的檔案，不默默移除執行位元。
- `requires: [{command, min_version}]` 僅列必需 runtime，安裝器只做固定工具 `--version`；`depends_on` 指向同 manifest 的另一技能。
- 可選 `adoption_files` 是已審核舊完整原樹 hash 白名單；目標只能保留全部原檔並新增指定頂層授權文字，不是任意 subset 覆寫入口。

新增共用技能的已授權安裝任務須把來源、固定版本、授權、必要依賴與完整檔案集一起登錄，並驗證後再發布；本機實驗明示例外。來源升級另作明確任務，不在 clone／pull 或安裝過程追 latest。

## 能力與未驗證範圍

HTML 基本功能需要 Node 20+；影片另外需要 Node 22+ 與 Chrome／Chromium／Edge，MP4 另需 ffmpeg。taste 完整 inspect／scenes 流程採 Node 22+ 與瀏覽器，assets 需要網路。安裝器不自動安裝上述工具，不跑 npm 或技能 payload；grill-me／grilling 與 career 無額外 runtime。

`ui-ux-pro-max` 的查詢與設計系統程式只用 Python 標準函式庫、本地 CSV／JSON，不需 pip、API key 或網路；完整隨包程式的靜態下限為 Python 3.9（`validate_data.py` 使用 `str.removesuffix`），共用安裝器仍要求 Python 3.11+。這不是原生 Python 3.9 驗證。隨包測試是完整來源快照，其中部分依賴上游 repo 根目錄的維護腳本，不能把技能目錄當成可獨立執行全部上游測試的專案。純查詢使用 `python -B` 與實際技能絕對路徑，詳見[跨平台呼叫範例](../docs/installation.md#ui-ux-pro-max-的本機查詢)；不產生技能目錄內的 bytecode 快取。

`ui-ux-pro-max` 與 `design-taste-frontend` 可互補：前者提供可查詢的 UI／UX、無障礙與技術棧建議，後者提供視覺方向及瀏覽器檢視。兩者均沿用專案既有、已確認的設計決策，按當次需求取用；納管不新增全域風格優先序，也不要求每次把兩套流程全部重跑。

上游 HTML 可能做更新檢查，影片旁白的 auto 模式可能使用已存在的外部供應商憑證；安裝／check 不執行這些功能，也不授權外部呼叫或讀取其秘密。插件、瀏覽器、客戶端發現、影片及素材網路須依實際場景另核對。本次 vendor 與檔案測試不代表原生 Windows／macOS Codex App 或技能工作流已測，也不代表人工接受。
