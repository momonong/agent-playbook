# 2026-10-22 跨裝置開發環境與技能同步

使用者要求補齊共用技能、核心與指南的同步機制，使另一台裝置取得 repo 後能依明確流程安裝同一套內容；每台有一個 agent-playbook 對話承接該裝置開發環境及已確認習慣同步。本次原對話沿用，其他裝置先沿用既有對話；新建仍由使用者明確要求。已授權本輪實作、必要核對、Git 合併推送與本機同步，各步實際完成證據分開回報，不由決策文件宣稱完成。

## 已確認方案與需求映射

| 需求 | 主要落點 |
|---|---|
| 新機與更新共用一套來源，保留原核心安裝介面 | `scripts/install.py`；[安裝文件](installation.md) 的固定完整 commit、preview → apply → check；`--with-skills` 明確選入 |
| 五份共用個人技能完整登錄，不再只裝單台 | [skills/manifest.json](../skills/manifest.json)、`skills/packages/`、[來源與授權](../skills/README.md) |
| 不覆蓋其他設定／技能／dirty worktree | 固定 Git blobs、逐檔 hash、來源乾淨檢查、位置歧義拒絕、雙 CAS、receipt、備份及失敗處理 |
| 每台有唯一承接對話與可重用開場 | [裝置同步契約](device-sync.md)；[合作指南](../guides/collaboration.md#裝置的環境同步對話) 只留必要規則與路由 |
| 新技能及核心更新在已授權交付內接續本機同步 | [工程指南](../guides/engineering.md#跨裝置環境與技能同步)，不每次用技能詢問同步 |
| 不把檔案成功當完整環境 | `--check` 分檔案／receipt／停用／runtime，客戶端發現、功能與人工接受另核對 |

技能來源固定為當前確認版本，不升級功能：answer-me-with-html 0.5.5、taste v2 固定內容、grill-me 與必要 grilling 原版入口、career-profile-builder 既有適配包。原 54 檔功能 bytes 不變，四包補 MIT LICENSE，HTML 補完整第三方授權；只對精確原樹允許 `adoption_files` 採用並先備份，不建立一般 subset 覆寫例外。插件／內建技能不 vendor 或複製 cache，其他裝置按實際客戶端核對功能及連線，不承諾版本同步。

## 授權與保護保留

來源、核心 pin、逐檔 SHA-256 與裝置目的地分開追溯；不追 latest、不執行上游程式、不安裝全域 runtime。Git 只取得來源，安裝仍需明確執行。完整設定、憑證、聊天及技能歷史不進 repo 或同步。不同裝置可以維護共用來源，但不自動傳訊、接管、建立未連線裝置對話或排程；Git、全域安裝與新外部操作仍核對具體授權。

維持 Astra Ultra 決策／推進／最後核對、Sol 6.1 Ultra subagent 實作，保留其他模型與設定。原核心的 override、備份、原子替換、指南快照、正式批准及資料／服務保護均保留；技能新增完整 preflight、目標狀態 digest、本機改動拒絕與回復。核心與技能不是整批原子交易，失敗明報 partial，細節只有安裝文件維護。

核心只在原工程必讀觸發列新增「裝置同步」，以便首次執行前找到完整規則；其餘契約在既有指南及文件。UTF-8 大小由 9,011 → 9,026 bytes，增加 15 bytes；常駐理由是跨裝置工作需要先定位適用工程保護。指南先提交、核心再重新釘選，保留原歷史檔。實際測試平台、CI、Git、全域安裝與人工接受另核對回報。
