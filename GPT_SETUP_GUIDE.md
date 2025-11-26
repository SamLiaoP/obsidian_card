# 🤖 GPT Actions 完整設定指南

## 📋 設定清單

- [ ] 複製 OpenAPI Schema
- [ ] 複製 Instructions  
- [ ] 配置 Capabilities
- [ ] 測試 Actions
- [ ] 測試對話

## 1️⃣ 配置 Actions

### 步驟 1: 創建或編輯 GPT

前往：ChatGPT > Explore GPTs > Create（或編輯現有 GPT）

### 步驟 2: 複製 Schema

1. 打開 `GPT_ACTIONS_SCHEMA.yaml`
2. 複製**全部內容**（176 行）
3. 前往 Configure > Actions
4. 點擊 "Create new action"
5. 貼到 Schema 欄位
6. Authentication: **None**
7. Save

### 步驟 3: 測試 Actions

點擊每個 Action 旁的 "Test"：

**Test 1: getKnowledgeBaseIndex**
```json
{}
```
預期：返回 10 個分類摘要（~6.8KB）

**Test 2: searchKnowledgeBase**
```json
{}
```
預期：返回所有檔案列表（~50KB）

**Test 3: getFileContent**
```json
{
  "file_id": "02f15f5d"
}
```
預期：返回檔案完整內容

## 2️⃣ 配置 Instructions

### 完整版（推薦）

1. 打開 `GPT_INSTRUCTIONS.md`
2. 複製全部內容（290 行）
3. 貼到 Configure > Instructions

### 精簡版（如果字數限制）

```markdown
你是 CARD 知識庫助手，管理 235 個筆記（10 大分類）。

工作流程：
1. 首次調用 getKnowledgeBaseIndex 獲取分類概覽
2. 定位相關分類
3. 需要時調用 searchKnowledgeBase 獲取 file_id
4. 調用 getFileContent(file_id) 獲取內容
5. 繁體中文回答，標註來源

分類：
1. 個人知識管理 (11) - 卡片盒筆記
2. 海外工作計畫 (15) - 簽證、履歷
3. 人生的價值觀 (28) - 價值觀、認知
4. 軟體開發 (69) - OOP, K8s, DDD
5. 科普新知 (17)
6. 意識與大腦 (21)
7. 決策科學 (12)
8. 人工智能 (54) - RAG, Agent, XAI
9. 專案管理 (4)
10. 投資 (4)

範例流程：
用戶問「什麼是卡片盒筆記？」
→ getKnowledgeBaseIndex（定位分類）
→ searchKnowledgeBase（找到 file_id）
→ getFileContent(file_id)（獲取內容）
→ 整合回答並引用來源

回答格式：
## [主題]
[內容]

📚 來源：
- 📝 [筆記名稱]（[分類]）

🔗 相關主題：[列出相關筆記]
```

## 3️⃣ 配置設定

### 基本資訊

**Name**: CARD 知識庫助手

**Description**: 
```
訪問 Sam 的 235 個筆記（卡片盒、軟體開發、AI、投資等），
根據問題找到相關筆記並提供詳細回答。
```

### Capabilities

- ❌ **Web Browsing**: 關閉（不需要）
- ❌ **Code Interpreter**: 關閉
- ❌ **DALL·E**: 關閉

### Conversation Starters

```
知識庫裡有哪些主題？
什麼是卡片盒筆記法？
如何優化 RAG 系統？
告訴我 DDD 的內容
有關海外工作的建議
```

## 4️⃣ 測試 GPT

### 測試 1: 基本功能
```
Q: "知識庫裡有哪些主題？"
```
**預期**：
- 調用 getKnowledgeBaseIndex
- 列出 10 個分類和數量

### 測試 2: 內容訪問
```
Q: "什麼是卡片盒筆記？請引用具體內容"
```
**預期**：
- 定位到「個人知識管理」分類
- 調用 searchKnowledgeBase
- 調用 getFileContent
- 引用筆記內容回答

### 測試 3: 搜索功能
```
Q: "有哪些關於 RAG 優化的筆記？"
```
**預期**：
- 在「人工智能」分類搜索
- 列出相關檔案

### 測試 4: 深度查詢
```
Q: "詳細解釋 DDD 的聚合根概念"
```
**預期**：
- 找到 DDD 相關筆記
- 獲取多個檔案內容
- 整合回答

## 🐛 常見問題排查

### 問題 1: ResponseTooLargeError

**原因**：可能在測試時使用了錯誤的端點

**解決**：
- 確保使用 `/index.json` 而非 `/tree.json`
- 檢查 Schema 中的端點路徑

### 問題 2: 404 Not Found

**檢查項目**：
1. URL 是否全小寫？
   ```yaml
   ✅ url: https://samliaop.github.io/obsidian_card
   ❌ url: https://SamLiaoP.github.io/obsidian_card
   ```

2. GitHub Pages 是否已部署？
   ```bash
   curl https://samliaop.github.io/obsidian_card/index.json
   ```

3. file_id 是否正確？
   ```bash
   # 檢查有效的 file_id
   curl .../search.json | grep "file_id"
   ```

### 問題 3: GPT 不調用 Actions

**可能原因**：
- Instructions 不夠明確
- 沒有強調「首次必調用 getKnowledgeBaseIndex」

**解決**：
在 Instructions 開頭加強說明：
```markdown
重要：每次對話開始時，必須先調用 getKnowledgeBaseIndex
了解知識庫結構。
```

### 問題 4: GPT 找不到內容

**檢查流程**：
1. GPT 是否調用了 searchKnowledgeBase？
2. 是否正確獲取了 file_id？
3. 是否調用了 getFileContent？

**除錯**：
在對話中查看 GPT 的 Actions 調用記錄

## 📊 優化建議

### 1. 加速回應

在 Instructions 中添加：
```markdown
優化策略：
- 首次調用後記住分類結構，同一對話中不需重複調用 index
- 如果用戶問題明確，直接調用 search 和 getFileContent
- 批次獲取相關檔案，一次性整合回答
```

### 2. 改善準確度

```markdown
搜索技巧：
- 檔案名稱包含主題關鍵字
- 數字編號表示層級關係
- Why? / How? / What? 表示筆記類型
```

### 3. 更好的回答

```markdown
回答原則：
1. 只根據筆記內容，不要編造
2. 明確引用來源（筆記名稱 + 分類）
3. 如果筆記內容不完整，誠實告知
4. 提供相關但未詳細讀取的筆記
```

## 🔄 維護與更新

### 更新 Instructions

根據使用經驗：
1. 觀察 GPT 常見的錯誤模式
2. 在 Instructions 中加強相關說明
3. 更新範例和格式

### 更新知識庫後

```bash
# 1. 修改 Markdown 檔案
vim "分類/檔案.md"

# 2. 重新生成
python3 generate_tree.py

# 3. 提交並推送
git add .
git commit -m "Update content"
git push

# 4. 等待 GitHub Actions 部署（1-2 分鐘）

# 5. GPT 自動獲取最新內容（無需修改設定）
```

### 添加新分類

1. 創建新資料夾和檔案
2. 重新生成（自動分配 file_id）
3. 在 `GPT_INSTRUCTIONS.md` 中更新分類列表
4. 更新 GPT Instructions

## 📈 效能監控

### 回應時間

- getKnowledgeBaseIndex: ~100ms
- searchKnowledgeBase: ~200ms  
- getFileContent: ~150ms
- 完整流程: ~4-5 秒

### 成功率

監控指標：
- Actions 調用成功率
- 檔案內容獲取成功率
- 用戶滿意度

## 🎯 進階功能

### 1. 添加搜索提示

在知識庫中創建索引檔案：
```markdown
# 主題索引.md

## RAG 相關筆記
- 8.2a Chunking 切分策略
- 8.2b Embedding 選擇
...
```

### 2. 創建常見問題

在 Instructions 中添加：
```markdown
常見問題快速索引：
- 卡片盒筆記 → 1. 個人知識管理
- RAG 優化 → 8.2 如何優化RAG服務
- DDD → 4.1e DDD
```

### 3. 添加標籤系統

修改 `generate_tree.py` 來提取標籤：
```python
# 從檔案內容中提取 #標籤
# 在 search.json 中添加 tags 欄位
```

## 📚 相關資源

- [QUICK_START.md](QUICK_START.md) - 快速開始
- [GPT_ACTIONS_SCHEMA.yaml](GPT_ACTIONS_SCHEMA.yaml) - OpenAPI Schema
- [GPT_INSTRUCTIONS.md](GPT_INSTRUCTIONS.md) - 完整提示詞
- [README.md](README.md) - 專案說明
- [SNAPSHOT.md](SNAPSHOT.md) - 變更記錄

---

**完成設定後，開始使用你的知識庫助手！** 🎉
