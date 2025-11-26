# 🚀 GPT Actions 配置總結

## ✅ 已完成的優化

### 問題解決

❌ **原問題**：`tree.json` 太大（214KB）導致 `ResponseTooLargeError`

✅ **解決方案**：創建輕量級 `index.json`（6.8KB），減少 97% 的回應大小

### 檔案結構

```
專案根目錄/
├── 📄 index.json          (6.8KB)  ← GPT Actions 主要端點
├── 📄 search.json         (42KB)   ← 詳細搜索端點
├── 📄 tree.json           (214KB)  ← 完整結構（保留）
├── 📄 generate_tree.py              ← 生成腳本
├── 📄 index.html                    ← API 說明頁
│
├── 📋 GPT_ACTIONS_SCHEMA.yaml      ← 複製到 GPT Actions
├── 📋 GPT_INSTRUCTIONS.md          ← 複製到 GPT Instructions
├── 📋 GPT_SETUP_GUIDE.md           ← 設定步驟指南
└── 📋 GPT_CONFIG_SUMMARY.md        ← 本檔案
```

## 📋 複製清單

### 1️⃣ OpenAPI Schema（複製到 GPT Actions）

**檔案**：`GPT_ACTIONS_SCHEMA.yaml`

**位置**：GPT Builder > Configure > Actions > Create new action > Schema

**內容預覽**：
```yaml
openapi: 3.1.0
servers:
  - url: https://samliaop.github.io/obsidian_card
paths:
  /index.json: ...
  /search.json: ...
```

### 2️⃣ Instructions（複製到 GPT Instructions）

**檔案**：`GPT_INSTRUCTIONS.md`（完整版）

**位置**：GPT Builder > Configure > Instructions

**或使用精簡版**（如果字數限制）：

```markdown
你是 CARD 知識庫助手，管理 237 個筆記（10 大分類）。

工作流程：
1. 首次調用 getKnowledgeBaseIndex 獲取概覽
2. 分析問題，定位相關分類
3. 需要時調用 searchKnowledgeBase 詳細搜索
4. 使用 Web Browsing 訪問 Markdown 檔案（記得 URL encode）
5. 整合內容，標註來源，繁體中文回答

分類：個人知識管理(11)、海外工作(15)、價值觀(28)、軟體開發(69)、科普(17)、意識大腦(21)、決策科學(12)、AI(54)、專案管理(4)、投資(4)

URL 構建範例：
```python
from urllib.parse import quote
url = "https://samliaop.github.io/obsidian_card/" + "/".join(quote(p, safe='') for p in path.split('/'))
```

回答格式：標題 > 內容 > 📚來源（筆記名+分類）> 🔗相關主題
```

### 3️⃣ Conversation Starters

```
知識庫裡有哪些主題？
什麼是卡片盒筆記法？
如何優化 RAG 系統？
DDD 領域驅動設計是什麼？
有關海外工作的建議
```

### 4️⃣ Settings

| 設定項 | 值 |
|--------|-----|
| Name | CARD 知識庫助手 |
| Description | 訪問 Sam 的 237 個筆記（卡片盒、開發、AI、投資等） |
| Web Browsing | ✅ 啟用（必須） |
| Code Interpreter | ⚠️ 可選 |
| DALL·E | ❌ 不需要 |
| Authentication | None（公開 API） |

## 🔗 API 端點總覽

| 端點 | 大小 | 用途 | 何時使用 |
|------|------|------|----------|
| `/index.json` | 6.8KB | 分類摘要 | 首次調用、概覽查詢 |
| `/search.json` | 42KB | 完整列表 | 搜索特定檔案 |
| `/tree.json` | 214KB | 樹狀結構 | 其他用途（非 GPT） |
| `/{path}.md` | 各異 | 筆記內容 | Web Browsing 訪問 |

## 🧪 測試檢查清單

在發布前，測試以下情境：

- [ ] **測試 1**：「知識庫有哪些主題？」
  - 應調用 `getKnowledgeBaseIndex`
  - 列出 10 大分類和數量

- [ ] **測試 2**：「什麼是卡片盒筆記？」
  - 應找到相關筆記
  - 使用 Web Browsing 訪問內容
  - 引用來源

- [ ] **測試 3**：「有哪些 RAG 相關的筆記？」
  - 應定位到「8. 人工智能」
  - 可能調用 `searchKnowledgeBase`
  - 列出相關檔案

- [ ] **測試 4**：「詳細解釋 DDD 的聚合根」
  - 應找到 DDD 相關筆記
  - 訪問具體內容
  - 整合回答

- [ ] **測試 5**：URL Encoding
  - 確認中文路徑正確編碼
  - 檔案訪問成功

## 🎯 關鍵配置重點

### ✅ 必做項目

1. **URL 必須全小寫**
   ```yaml
   url: https://samliaop.github.io/obsidian_card
   ```

2. **啟用 Web Browsing**
   - 沒有這個功能無法訪問 .md 檔案

3. **Instructions 強調 URL encoding**
   - 中文路徑必須編碼

4. **首次必調用 index**
   - 在 Instructions 中明確說明

### ⚠️ 常見錯誤

| 錯誤 | 原因 | 解決 |
|------|------|------|
| ResponseTooLargeError | 使用 tree.json | 改用 index.json |
| 404 Not Found | URL 大小寫錯誤 | 全小寫 |
| 404 Not Found | 路徑未編碼 | URL encode |
| GPT 不調用 API | Instructions 不明確 | 加強說明 |

## 📊 效能指標

### API 回應時間（預估）

- `index.json`：~100ms（6.8KB）
- `search.json`：~200ms（42KB）
- `.md` 檔案：~150ms（平均 5KB）

### 完整查詢流程（預估）

```
用戶提問
  ↓ ~100ms
getKnowledgeBaseIndex (6.8KB)
  ↓ ~150ms
Web Browsing 訪問 2-3 個 .md 檔案
  ↓ ~5s
GPT 生成回答
  ↓
總計：~5-6 秒
```

## 🔄 維護流程

### 更新知識庫

```bash
# 1. 修改 Markdown 檔案
vim "path/to/file.md"

# 2. 重新生成索引
python3 generate_tree.py

# 3. 檢查生成結果
ls -lh *.json

# 4. 提交到 Git
git add .
git commit -m "Update: 描述變更內容"
git push

# 5. 等待 GitHub Actions 部署（1-2 分鐘）

# 6. 驗證
curl https://samliaop.github.io/obsidian_card/index.json | jq '.total_files'
```

### 優化 Instructions

根據使用經驗：
1. 觀察 GPT 常見的錯誤模式
2. 在 Instructions 中加強相關說明
3. 更新回答格式範本
4. 添加更多範例

### 添加新分類

1. 在知識庫中創建新資料夾
2. 添加 Markdown 檔案
3. 重新生成索引
4. 在 `GPT_INSTRUCTIONS.md` 中更新分類列表
5. 更新 GPT Instructions

## 📈 進階優化建議

### 1. 添加快取層

如果查詢量大，考慮：
- 使用 Cloudflare CDN
- 設定適當的 Cache-Control headers

### 2. 添加搜索功能

創建 `/api/search?q={keyword}` 端點：
- 需要額外的靜態生成腳本
- 或使用 GitHub Actions + Algolia

### 3. 添加統計分析

在 `index.html` 中整合：
- Google Analytics
- 查詢熱度追蹤
- 流行主題分析

### 4. 多語言支援

如果需要支援多語言：
- 生成 `index.en.json`
- GPT 根據用戶語言選擇端點

## 📞 支援與反饋

### 遇到問題？

1. 查看 `GPT_SETUP_GUIDE.md` 的「常見問題排查」
2. 檢查 GitHub Actions 的部署日誌
3. 驗證 API 端點是否可訪問
4. 檢查 GPT Actions 的測試日誌

### 改進建議

記錄在 `SNAPSHOT.md` 中：
- 效果良好的配置
- 需要改進的地方
- 用戶反饋

## 🎉 完成狀態

- ✅ 解決 ResponseTooLargeError
- ✅ 創建輕量級 index.json（6.8KB）
- ✅ 創建 search.json 搜索端點
- ✅ 修正 URL 為全小寫
- ✅ 編寫完整的 GPT Instructions
- ✅ 創建 OpenAPI Schema
- ✅ 撰寫設定指南
- ✅ 建立測試檢查清單
- ✅ 更新 SNAPSHOT.md

## 🚀 現在可以做什麼

1. **複製 Schema 到 GPT Actions**
   - 打開 `GPT_ACTIONS_SCHEMA.yaml`
   - 貼到 GPT Actions Schema 欄位

2. **複製 Instructions**
   - 打開 `GPT_INSTRUCTIONS.md`
   - 貼到 GPT Instructions 欄位

3. **配置設定**
   - 啟用 Web Browsing
   - 添加 Conversation Starters
   - 設定名稱和描述

4. **測試 GPT**
   - 使用測試檢查清單
   - 驗證所有功能正常

5. **發布使用**
   - 分享給需要的人
   - 收集使用反饋
   - 持續優化

---

一切就緒！你的知識庫 AI 助手已經準備好了 🎊

