# 2026-10-22 受限部署判斷與 grill-me

使用者確認補入文件與提示詞、安裝作者原版 `grill-me`，核對後合併推送並同步本機 Codex。以下保存決策與界線，實際 Git、技能安裝及本機同步結果另行查證，不以本紀錄宣稱完成。

## 受限部署的來源與判斷

[服務指南](../guides/service-integration.md#家用伺服器selfhost-servers)維護共通權限判斷與文件入口；具體能力矩陣、唯讀 preflight、日常操作與 root gate 留在 `momonong/selfhost-servers` 的 `docs/two-host-deployment.md`，依既有文件定位規則取得當次固定版本，不將未發布草稿或歷史現況當契約。

Doppler 憑證、SSH／API 能力、使用者授權及 Codex 沙箱分別核對。已授權且通道涵蓋者直接完成；失敗先核對實際工具、路徑、金鑰及通道並分類，真正超出通道 scope 才準備最小 root gate。這補足先前「需人工時提供指令」的判斷前提，不新增通用 sudo、不以換身分 fallback，也不授權新的伺服器操作。

## 原版技能與討論界線

固定作者來源為 `mattpocock/skills` commit `5beb35b040e3de97e54fa9e386d7e42d15c295c2` 的 [skills/productivity/grill-me](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/productivity/grill-me) 與 [skills/productivity/grilling](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/productivity/grilling)。前者是使用者主動呼叫入口，原文要求載入後者，因此安裝兩個必要入口，保留作者原文，不擴張安裝其他技能或改動既有 taste。

[合作指南](../guides/collaboration.md#使用-grill-me-深問方案)只維護本人的使用規則：Astra 在原對話承接明確要求的方案深問，先查事實、沿用已決策並依共識或停止要求收束；本地技能載入可讀必要 `SKILL.md` 全文，不虛構作者所稱的 Skill 工具。問答完成不構成工程、部署、Git 或新增任務的授權。

## 精簡與保留

README 只留兩個入口；核心由 8,993 → 9,011 bytes（UTF-8，增加 18 bytes），只在既有必讀表補 `grill-me 討論` 觸發，讓單純討論也在技能使用前讀到界線；詳細規則留既有指南，不增常駐段落或主流程分工。指南先提交再由核心釘選真實 commit；歷史原文、模型分工、操作授權、正式批准、未提交工作及共用服務保護均保留。文件驗證與技能實際載入、現場部署及人工接受分開回報。
