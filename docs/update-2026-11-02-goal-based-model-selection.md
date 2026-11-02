# 依目標調配模型與推理深度

使用者指出不能再把 reset 視為寬裕資源，要求配置必須針對目標；在「按目標調配，取消固定分工」與「保留 Astra／Sol，只調深度」之間，明確選擇前者。已確認的一般起點為 Sol 6.1 Medium，在原對話承接完整工作，按難度、風險及驗證方式調整。

## 決策與取代範圍

- [模型指南](../guides/model-selection.md)為完整規則的主要來源，取代 2026-10-18 的固定 Astra Ultra 決策／Sol Ultra 實作與 Ultra 日常預設。原目標對話仍負責整合、驗證及交付，不依模型另建對話。
- 確定性操作先用既有工具；一般目標採 Sol 6.1 Medium。困難實作與除錯可採 Sol High，高不確定研究或重大取捨可採 Astra High；需要更深配置時須有具體盲點、範圍、驗證及停止條件。明顯困難的目標可直接選足夠配置，不為形式逐級試錯。
- 派工須有獨立收益，避免完整歷史複製、無必要代理與重複驗證。高配階段結束後，後續按實際目標重新選型；不因剩餘額度升級，也不預支未取得的 reset。
- 這台電腦的新工作階段與未指定配置之 subagent 起點均為 `gpt-6.1-sol`／`medium`。本次本機設定範圍只有 `model`、`model_reasoning_effort`、`agents.default_subagent_model`、`agents.default_subagent_reasoning_effort`；只備份必要欄位及 hash，不複製完整 config 或秘密。
- 既有聊天配置、暫停狀態、其他設定、插件及其他裝置保留。工具、任務建立、Git、外部供應商與額外付費的授權不擴張；主對話實際切換仍由使用者決定，不宣稱改文字或新預設就已切換目前執行的模型。

## 文件與驗證

核心只保留目標導向選型、一般起點、原對話責任與設定界線；完整升降、上下文及成本控制集中模型指南。核心由 9,220 → 9,255 bytes（UTF-8，增加 35 bytes），增量用於首次配置前必需的選型原則；合作指南、README 及裝置同步入口一併消除固定角色摘要，舊決策保持原文供追溯。

指南先提交為完整 SHA，再由核心更新 `guides-commit` 與固定 URL；發布及本機同步沿用乾淨固定來源、預覽、CAS、備份與 check。核對模型配置時只輸出允許的欄位，確認其餘 TOML 值不變；不建立額外 benchmark、呼叫模型 API、使用 reset 或改動研究驗收。Git、指示安裝、新預設落盤及既有聊天載入分開回報。

OpenAI 的[推理深度說明](https://developers.openai.com/api/docs/guides/reasoning#reasoning-effort)支持按任務取捨深度；[subagent 設定](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents)說明預設與顯式配置的優先序。這些文件不提供本帳號的 reset 配額，也不代表本政策已量測固定節省比例；實際模型與 effort 仍核對當台支援。
