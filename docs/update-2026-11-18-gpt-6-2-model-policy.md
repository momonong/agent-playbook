# 全面採用 GPT-6.2 與 High／XHigh

使用者在本次 agent-playbook 更新中要求「至少要用 high, xhigh 會好一點」，並補充「然後全面改用 6.2」。因此更新現行模型及深度政策，取代先前提出的 Sol 6.2 Medium 方案，以及 2026-11-02 的 Sol 6.1 Medium 一般起點；按目標調配與原對話完整承接仍保留。

## 決策與範圍

- 現行 Codex 選型採 `gpt-6.2-sol` 與 `gpt-6.2-astra`。一般工作、新工作階段與未明示配置之 subagent 以 Sol 6.2 High 為起點；複雜實作、除錯與整合採 Sol 6.2 XHigh，高不確定研究、重大架構與跨領域推理採 Astra 6.2 XHigh。這是依使用者選定的 6.2／High 以上原則制定的選型起點，不固定模型角色，也不要求逐級試錯。
- 未另有使用者明確指定時，不用 Low／Medium 作預設或自動降級，不保留舊模型的自動 fallback。確定性工作優先工具／腳本；可回到 6.2 High 收尾，不為小操作另派模型。
- Max／Ultra 須有具體額外收益、驗證與停止條件，非日常預設。Standard 速度保留；Ultra effort 與 Ultrafast 速度分開，不因模型升級自行提高速度或付費。
- 全面更新指現行 Codex 選型政策；歷史決策保留原文。既有聊天、目前執行模型、裝置 config、其他裝置、外部供應商及應用後端模型不由文件更新自動切換。Git 提交、合併、推送與全域安裝仍依當次授權分別處理。

## 依據與限制

2026-11-18 已核對 OpenAI 的[模型說明](https://learn.chatgpt.com/docs/models)、[GPT-6.2 Codex 指南](https://learn.chatgpt.com/guides/prompting-gpt-6-2-astra)及[速度說明](https://learn.chatgpt.com/docs/agent-configuration/speed)，並以當台模型清單確認兩個 6.2 ID 及 `high`／`xhigh` 可用。官方將 Sol 定位於日常工作、Astra 用於較困難的工作，並建議依調查深度選 effort；這些資訊支持版本及能力定位，不代表官方要求所有工作至少 High。

High 下限來自本次使用者偏好。尚未以本人的代表性工作量測 6.2 的品質、時間或用量差異，不宣稱固定節省或效能提升；訂閱用量與 API 價格不混算。官方可用功能與當台工具實際暴露的參數分開核對，不把本機清單寫成所有裝置的保證。

## 文件與驗證

完整規則集中[模型指南](../guides/model-selection.md)；[核心](../instructions/codex.md#模型設定)、[README](../README.md#一個對話一個目標)與[裝置入口](device-sync.md#同步範圍與責任)只同步摘要，[遷移記錄](migration-2026-09-30.md#2026-11-18-gpt-62-與-highxhigh)保存取代範圍。沿用本輪已確認目錄與文件分支，不新增工作樹、測試框架或 benchmark。

驗證涵蓋現行入口無舊模型／較低深度預設、High／XHigh 與 Standard 的一致性、本地連結與 anchors、UTF-8、diff 格式、歷史原文 hash、核心大小及六份指南的固定版本。核心由 9,293 → 9,331 bytes（UTF-8，增加 38 bytes），只補足首次選型前必需的全面 6.2 與 High 下限；完整表格、速度及升降細節留在模型指南。

使用者在審閱上述草稿後確認提交、合併推送，並同步這台的指示與新工作預設。先提交指南，再將核心 `guides-commit` 與遠端固定 URL 釘選到該真實完整 SHA；合併後依固定來源、預覽、CAS、備份及 check 同步核心／指南。本機 config 僅更新 `model`、`model_reasoning_effort`、`agents.default_subagent_model`、`agents.default_subagent_reasoning_effort` 為 Sol 6.2 High；保存必要欄位與 hash，保留其餘設定，不同步技能或其他裝置。

使用者另要求針對專案裡的對話「主要把模型改到適合的模型和推理深度即可」。這是本輪既有專案對話的設定授權：按各自目標選擇 6.2／High 或 XHigh，核對可用介面及更新結果，保留名稱、歸屬、內容、暫停與封存狀態，不啟動原工作。對話清單、個別配置及本機備份留在本機，不寫入共用 repo；工具限制或未完成項目另行回報。本次授權不改變日後更新既有聊天仍須核對當次範圍的規則，Git、安裝與設定的實際結果不由本記錄預稱完成。
