# 🚀 快速開始指南

## ✨ 新功能：直接訪問 Markdown 內容

你的知識庫 API 已經升級！現在 GPT 可以通過 Actions 直接訪問檔案內容，不再需要 Web Browsing。

## 📋 三步完成配置

### 步驟 1：複製 OpenAPI Schema

1. 打開 `GPT_ACTIONS_SCHEMA.yaml`
2. 複製**全部內容**
3. 前往 ChatGPT > GPTs > 你的 GPT > Configure > Actions
4. 點擊 "Create new action"（或編輯現有的）
5. 貼上到 Schema 欄位
6. Authentication 選擇：**None**
7. 點擊 Save

### 步驟 2：複製 Instructions

1. 打開 `GPT_INSTRUCTIONS.md`
2. 複製**全部內容**
3. 前往 Configure > Instructions
4. 貼上到 Instructions 欄位
5. 點擊 Save

### 步驟 3：配置設定

1. 前往 Configure > Capabilities
2. 確保設定：
   - ❌ Web Browsing：關閉（不需要了！）
   - ❌ Code Interpreter：關閉
   - ❌ DALL·E：關閉

3. 添加 Conversation Starters：
```
知識庫裡有哪些主題？
什麼是卡片盒筆記法？
如何優化 RAG 系統？
告訴我 DDD 的內容
有關海外工作的建議
```

## 🧪 測試你的 GPT

### 測試 1：基本查詢
```
Q: "知識庫裡有哪些主題？"
```
**預期**：GPT 列出 10 大分類和檔案數量

### 測試 2：獲取內容
```
Q: "什麼是卡片盒筆記？請引用具體內容"
```
**預期**：GPT 調用 API 獲取內容並回答

### 測試 3：搜索
```
Q: "有哪些關於 RAG 的筆記？"
```
**預期**：GPT 找到相關檔案並列出

## 🔗 新的 API 架構

```
GET /index.json
→ 分類摘要（首次調用）

GET /search.json  
→ 所有檔案 + file_id

GET /api/files/{file_id}.json
→ 檔案完整內容 ✨ 新增！
```

## 📊 工作流程

```
用戶提問
  ↓
1. getKnowledgeBaseIndex
   返回：分類概覽
  ↓
2. searchKnowledgeBase（如需要）
   返回：檔案列表 + file_id
  ↓
3. getFileContent(file_id) ← 新功能！
   返回：完整 Markdown 內容
  ↓
4. GPT 整合回答
```

## ✅ 測試 Actions（可選）

在 GPT Actions 設定頁面：

**Test 1: getKnowledgeBaseIndex**
```json
{}
```
應返回：分類摘要

**Test 2: searchKnowledgeBase**
```json
{}
```
應返回：所有檔案（含 file_id）

**Test 3: getFileContent**
```json
{
  "file_id": "02f15f5d"
}
```
應返回：檔案完整內容

## 🚀 部署到 GitHub Pages

```bash
cd /Users/user/Desktop/Projects/Obsidian/CARD

# 查看變更
git status

# 提交
git add .
git commit -m "Add file content API for GPT Actions"
git push

# 等待 1-2 分鐘讓 GitHub Actions 部署
```

驗證部署：
```bash
curl https://samliaop.github.io/obsidian_card/index.json
curl https://samliaop.github.io/obsidian_card/api/files/02f15f5d.json
```

## 📚 更多資源

| 檔案 | 用途 |
|------|------|
| `GPT_ACTIONS_SCHEMA.yaml` | 複製到 GPT Actions |
| `GPT_INSTRUCTIONS.md` | 複製到 GPT Instructions |
| `GPT_CONFIG_SUMMARY.md` | 快速配置參考 |
| `API_UPGRADE_SUMMARY.md` | 升級詳細說明 |
| `API_TEST_EXAMPLES.md` | API 測試範例 |
| `GPT_SETUP_GUIDE.md` | 詳細設定指南 |

## 💡 關鍵變更

### ✅ 新增功能
- file_id 系統（每個檔案 8 位 ID）
- getFileContent API（直接獲取內容）
- 235 個 JSON 內容檔案

### ❌ 不再需要
- Web Browsing 功能
- URL encoding 處理
- 複雜的路徑處理

## 🎯 優勢

| 項目 | 舊方式 | 新方式 |
|------|--------|--------|
| 訪問方式 | Web Browsing | Actions API |
| 複雜度 | 需要 URL encode | 直接用 file_id |
| 穩定性 | 經常失敗 | 標準 API |
| 速度 | ~500ms | ~150ms |

## ⚠️ 重要提示

1. **URL 必須全小寫**
   ```
   ✅ https://samliaop.github.io/obsidian_card
   ❌ https://SamLiaoP.github.io/obsidian_card
   ```

2. **不需要 Web Browsing**
   - 在 GPT Capabilities 中關閉

3. **使用 file_id 而非路徑**
   - 從 search 獲取 file_id
   - 調用 getFileContent(file_id)

## 🎉 完成！

按照上面的三個步驟，你的 GPT 就準備好了！

有任何問題，查看 `GPT_SETUP_GUIDE.md` 的「常見問題排查」章節。

---

**測試你的 GPT，享受新功能！** 🚀

