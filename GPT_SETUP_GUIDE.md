# 🤖 GPT Actions 設定指南

## 快速設定步驟

### 1️⃣ 創建 GPT

前往 ChatGPT > Explore GPTs > Create

### 2️⃣ 基本資訊

**名稱**：
```
CARD 知識庫助手
```

**描述**：
```
專門訪問 Sam 的個人知識庫（236 個筆記），涵蓋卡片盒筆記、軟體開發、AI、投資等主題。能根據問題找到相關筆記並提供詳細回答。
```

### 3️⃣ Instructions

**方式 A：從檔案複製**
- 打開 `GPT_INSTRUCTIONS.md`
- 複製全部內容
- 貼到 Instructions 欄位

**方式 B：精簡版（如果字數限制）**
```markdown
你是 CARD 知識庫助手，協助訪問 236 個 Markdown 筆記（10 大分類）。

## 工作流程
1. 首次調用 getKnowledgeBaseIndex 獲取概覽
2. 根據問題定位相關分類
3. 需要時調用 searchKnowledgeBase 搜索
4. 使用 Web Browsing 訪問檔案（路徑需 URL encode）
5. 整合內容回答，標註來源

## 主要分類
1. 個人知識管理 (11)
2. 海外工作計畫 (15)
3. 人生的價值觀 (28)
4. 軟體開發 (69) - OOP, K8s, DDD
5. 科普新知 (17)
6. 意識與大腦 (21)
7. 決策科學 (12)
8. 人工智能 (54) - RAG, Agent, XAI
9. 專案管理 (4)
10. 投資 (4)

## URL 構建
```python
from urllib.parse import quote
base = "https://samliaop.github.io/obsidian_card"
path = "分類/子分類/檔案.md"
url = base + "/" + "/".join(quote(p, safe='') for p in path.split('/'))
```

## 回答格式
- 繁體中文
- 引用來源筆記
- 標註分類
- 提供相關主題
```

### 4️⃣ 配置 Actions

#### 步驟 1: 創建 Action

點擊 "Create new action"

#### 步驟 2: 導入 Schema

**方式 A：導入檔案**
- 如果支援，直接導入 `GPT_ACTIONS_SCHEMA.yaml`

**方式 B：手動貼上**
- 打開 `GPT_ACTIONS_SCHEMA.yaml`
- 複製全部內容
- 貼到 Schema 欄位

#### 步驟 3: 設定 Authentication

選擇：**None**（公開 API，無需驗證）

#### 步驟 4: 測試 Actions

點擊 "Test" 按鈕測試：

**測試 1: getKnowledgeBaseIndex**
```json
{}
```
預期結果：返回分類摘要（6.7KB）

**測試 2: searchKnowledgeBase**
```json
{}
```
預期結果：返回完整檔案列表（42KB）

### 5️⃣ 配置 Capabilities

- ✅ **Web Browsing**（必須！用於訪問 Markdown 檔案）
- ⚠️ **Code Interpreter**（可選，用於 URL encoding）
- ❌ **DALL·E**（不需要）

### 6️⃣ Conversation Starters

添加以下建議問題：

```
1. 知識庫裡有哪些主題？給我一個概覽
2. 什麼是卡片盒筆記法？我該如何開始？
3. 如何優化 RAG 系統的效能？
4. 告訴我關於 DDD 領域驅動設計的內容
5. 有哪些關於海外工作的建議？
```

### 7️⃣ 儲存並測試

點擊右上角 **Save** 或 **Update**

## 🧪 測試你的 GPT

### 測試 1: 基本查詢
```
Q: 知識庫裡有哪些主題？
預期: GPT 調用 getKnowledgeBaseIndex，列出 10 大分類和統計
```

### 測試 2: 概念查詢
```
Q: 什麼是卡片盒筆記？
預期: GPT 找到相關筆記，訪問內容，提供答案並引用來源
```

### 測試 3: 技術查詢
```
Q: 如何優化 RAG？
預期: GPT 在「8. 人工智能」分類找到相關筆記，整合回答
```

### 測試 4: 搜索功能
```
Q: 有哪些關於 K8s 的筆記？
預期: GPT 使用 searchKnowledgeBase 搜索，列出相關檔案
```

## ⚠️ 常見問題排查

### 問題 1: ResponseTooLargeError

**原因**：使用了錯誤的端點（tree.json 太大）

**解決**：確保 Actions 使用的是 `/index.json`，不是 `/tree.json`

### 問題 2: 404 Not Found

**可能原因 A**：URL 格式錯誤

**檢查**：
```
❌ https://SamLiaoP.github.io/... (大小寫錯誤)
✅ https://samliaop.github.io/... (全小寫)
```

**可能原因 B**：路徑未 URL encode

**檢查**：GPT 是否正確 encode 了中文路徑

### 問題 3: 找不到檔案

**原因**：GPT 沒有正確使用 URL encoding

**解決**：在 Instructions 中強調使用 Python 的 `urllib.parse.quote`

### 問題 4: GPT 不調用 Actions

**原因**：Instructions 不夠明確

**解決**：在 Instructions 開頭明確說明「首次必須調用 getKnowledgeBaseIndex」

### 問題 5: Web Browsing 失敗

**原因**：Capabilities 中未啟用 Web Browsing

**解決**：在 GPT 設定中啟用 Web Browsing

## 📊 效能優化建議

### 1. 分層查詢策略

```
用戶問概覽性問題
  → 只調用 getKnowledgeBaseIndex (6.7KB)
  
用戶問特定分類的詳細內容
  → 調用 searchKnowledgeBase (42KB)
  
用戶問具體筆記內容
  → Web Browsing 訪問 .md 檔案
```

### 2. 快取策略

在 Instructions 中建議 GPT：
- 首次調用後記住分類結構
- 同一對話中不需重複調用 index

### 3. 批次訪問

如果需要多個筆記：
- 先列出相關筆記
- 詢問用戶想深入了解哪些
- 再批次訪問具體內容

## 🔄 更新流程

當知識庫內容更新後：

1. **本地重新生成**
```bash
cd /Users/user/Desktop/Projects/Obsidian/CARD
python3 generate_tree.py
```

2. **推送到 GitHub**
```bash
git add .
git commit -m "Update knowledge base"
git push
```

3. **等待部署**
- 前往 GitHub Actions
- 等待 "Deploy to GitHub Pages" 完成（1-2 分鐘）

4. **驗證更新**
```bash
curl https://samliaop.github.io/obsidian_card/index.json
```

5. **GPT 自動同步**
- 無需修改 GPT 設定
- GPT 下次調用時會獲取最新資料

## 📝 進階配置

### 添加自訂域名

1. 在倉庫根目錄創建 `CNAME` 檔案
```
api.yourdomain.com
```

2. 在 DNS 設定中添加 CNAME 記錄
```
CNAME  api  samliaop.github.io
```

3. 更新 `generate_tree.py` 中的 `base_url`
```python
base_url = "https://api.yourdomain.com"
```

### 添加訪問統計

在 `index.html` 中添加 Google Analytics：
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
```

### 添加 CORS 設定

創建 `_headers` 檔案：
```
/index.json
  Access-Control-Allow-Origin: *
  
/search.json
  Access-Control-Allow-Origin: *
```

## 🎓 最佳實踐

1. **定期測試**：每次更新知識庫後測試 GPT
2. **監控日誌**：在 ChatGPT 對話中觀察 API 調用
3. **收集反饋**：記錄 GPT 回答不準確的情況
4. **優化 Instructions**：根據使用經驗調整提示詞
5. **更新範例**：在 Conversation Starters 中添加新主題

## 📚 相關文件

- `GPT_INSTRUCTIONS.md` - 完整的系統提示詞
- `GPT_ACTIONS_SCHEMA.yaml` - OpenAPI Schema 定義
- `DEPLOY_GUIDE.md` - GitHub Pages 部署指南
- `README.md` - 專案總覽
- `SNAPSHOT.md` - 變更記錄

---

設定完成後，你就擁有了一個專屬的知識庫 AI 助手！🎉

