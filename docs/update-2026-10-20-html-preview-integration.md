# 2026-10-20 私人 HTML 預覽正式接入

## 已確認的交付與授權

使用者已確認標準流程：「產生 HTML → 上傳指定成品 → 取得 HTTPS 網址及到期時間 → 瀏覽器核對顯示 → 在原對話交付連結及原始檔位置。」日常操作在已設定權限內完成，不要求每次手動部署、修改 Caddy 或輸入 sudo。

此流程只涵蓋使用者授權範圍內、本次產生並作私人預覽交付的明確單份 HTML；不授權掃描 repo、歷史文件或聊天，不批次上傳其他私人資料。已有本次交付授權且通道已配置可用時直接完成，不逐份重問；任意生成 HTML 的要求不等於無範圍的永久上傳授權。

核心只保留簡短原則及必讀入口；詳細規則放既有工程／服務指南，使用固定接入契約，不維護新的 skill，不客製 `answer-me-with-html` 或修改模型設定。

## 固定來源與驗收邊界

正式契約為 `momonong/html-preview` commit `13d83daac04b7a47a6c2ed1046242f89d51373f9` 的 [docs/client-integration.md](https://github.com/momonong/html-preview/blob/13d83daac04b7a47a6c2ed1046242f89d51373f9/docs/client-integration.md)，由已合併來源引用；本 playbook 不複製完整 API、命令、帳號或部署設定。

服務目標於 2026-10-20 完成正式 HTTPS、原生表單登入／登出／重新登入、互動圖表／主題、五項 sandbox 探測、原稿 bytes/hash、真實五分鐘到期、重按／重整／離開／服務重啟不延長、到期即拒讀及實體清理。另一份文件與本機原稿保持不變；證據與限制見同版本的[正式驗證紀錄](https://github.com/momonong/html-preview/blob/13d83daac04b7a47a6c2ed1046242f89d51373f9/docs/deployment-verification-2026-10-20.md)。這是啟用既有通道的工程證據；第二裝置的登入／可達性及使用者最終人工接受仍待本人確認，未宣稱已完成。

這取代[先前決策](update-2026-10-20-html-delivery.md)中的服務待啟用狀態，不回寫當時紀錄，也不將歷史驗證當成後續版本或每台裝置的健康證明。

## 需求映射與保留限制

| 已確認需求 | 主要落點 |
|---|---|
| 當前裝置能閱讀渲染頁面，附原稿，不依賴執行端 localhost | [核心](../instructions/codex.md#驗證與回報)、[工程指南](../guides/engineering.md#html-交付) |
| 已授權的本次單份成品走既有 HTTPS 通道，不逐份要求部署／sudo | [工程標準流程](../guides/engineering.md#html-交付)、[服務入口](../guides/service-integration.md#私人-html-預覽html-preview) |
| 不掃歷史或批次上傳；憑證分離、不進 URL／聊天／日誌 | [服務指南](../guides/service-integration.md#私人-html-預覽html-preview)、固定接入契約 |
| 保留原 operation／收據，未知結果先查，不換 key 當重試 | [服務指南](../guides/service-integration.md#私人-html-預覽html-preview)、固定接入契約 |
| 七天保存、提前到期只縮短、服務端計時清理、不刪本機原稿 | [服務指南](../guides/service-integration.md#私人-html-預覽html-preview)、固定服務契約 |
| 不為互動相容性放寬隔離，工程成功與人工接受分開 | [服務指南](../guides/service-integration.md#私人-html-預覽html-preview)、[工程指南](../guides/engineering.md#html-交付) |
| 短核心、詳細指南、固定契約、不改上游 skill／模型配置 | 核心只新增必要入口；工程／服務指南維持單一主要落點 |

Astra Ultra／Sol 6.1 Ultra 分工、分類分支、操作授權、正式批准、未提交工作與共用服務保護均保留。歷史原文 `archive/original-2026-09-30.md` 位元組不變，SHA-256 仍為 `def91c5512b3ae5a79380eb1d38501c5394461137f0fb56a9ac9296b8a67ad9a`。

核心由 8,942 bytes 至 8,993 bytes，增加 51 bytes，只補足首次行動前必需的共用 HTTPS 與 localhost 界線。工程指南移除與既有通道重複的臨時／同機開啟分支，操作、認證、重試與到期細節集中服務契約；不把服務網址或命令常駐核心。指南變更先提交，再由核心的 `guides-commit` 與固定 URL 指向真實指南 commit。

本輪以既有 installer checks、UTF-8、本地連結／錨點、需求映射、固定來源／核心 pin、核心大小、歷史原文 hash 及 diff／staging 核對驗證。提交、推送、PR／合併及固定版本安裝各依實際結果回報；本紀錄不宣稱已完成後續 Git 交付或本機安裝。
