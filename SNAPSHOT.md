# SNAPSHOT - 專案變更記錄

## 2024-11-26 - 優化 GitHub Actions Workflows

### 📝 變更內容

**優化 deploy.yml**：
- ✅ 添加詳細的生成日誌
- ✅ 顯示檔案大小和數量統計
- ✅ 添加 JSON 格式驗證步驟
- ✅ 檢查必要欄位是否存在

**新增 test.yml**：
- ✅ 在 PR 時自動測試
- ✅ 驗證 `generate_tree.py` 運行正常
- ✅ 上傳測試結果 artifact（保留 7 天）
- ✅ 支援手動觸發測試

### 🎯 改進目標

1. **更好的可見性** - 在 Actions 日誌中清楚看到生成結果
2. **及早發現錯誤** - PR 階段就測試，避免壞的程式碼合併
3. **自動驗證** - 確保生成的 JSON 格式正確
4. **除錯友善** - 提供測試 artifact 供下載檢查

### 📊 Workflow 架構

```
Push to main
    ↓
deploy.yml
    ├── Checkout
    ├── Setup Python
    ├── Generate API files（顯示統計）
    ├── Validate（驗證格式）
    ├── Setup Pages
    └── Deploy
    
Pull Request
    ↓
test.yml
    ├── Checkout
    ├── Setup Python
    ├── Test generate_tree.py
    ├── Validate files
    └── Upload artifacts
```

### 💡 使用方式

**自動觸發**：
- Push → 自動部署
- PR → 自動測試

**手動觸發**：
```
Actions > 選擇 workflow > Run workflow
```

### 📝 示例日誌輸出

```
🚀 開始生成 API 檔案...
正在掃描 Markdown 檔案...
✅ 成功生成 tree.json
📁 共找到 235 個 Markdown 檔案
✅ 成功生成 index.json (輕量級索引 - 只有分類摘要)
✅ 成功生成 search.json (完整檔案列表，按分類，包含 file_id)
✅ 成功生成 235 個檔案內容 JSON

✅ 生成完成！檢查結果：
📄 index.json: 6.8K
📄 search.json: 50K
📄 tree.json: 214K
📁 api/files/: 235 個檔案
💾 總大小: 976K

🔍 驗證 API 檔案格式...
✓ index.json 格式正確
✓ search.json 格式正確
✓ tree.json 格式正確
✓ index.json 包含 base_url
✓ index.json 包含 total_files
✓ search.json 包含 file_id
✅ 所有驗證通過！
```

---

## 2024-11-26 - 文件整理與統整

### 📝 變更內容

**刪除重複和過時的文件**：
- ❌ `API_UPGRADE_SUMMARY.md` - 一次性升級說明（已記錄在 SNAPSHOT）
- ❌ `GPT_CONFIG_SUMMARY.md` - 與 GPT_SETUP_GUIDE 重複
- ❌ `API_TEST_EXAMPLES.md` - 測試範例（已合併到 README）
- ❌ `DEPLOY_GUIDE.md` - 部署指南（已合併到 README）

**更新主要文件**：
- ✅ `README.md` - 重寫為綜合主文檔
- ✅ `GPT_SETUP_GUIDE.md` - 簡化為實用指南
- ✅ `QUICK_START.md` - 保持不變（最重要）

**最終文件結構**：
```
核心文件（必需）：
├── README.md               - 主文檔（API 說明、使用範例、FAQ）
├── QUICK_START.md          - 快速開始（3 步驟配置）
├── SNAPSHOT.md             - 變更記錄

GPT 配置文件：
├── GPT_ACTIONS_SCHEMA.yaml - OpenAPI Schema（複製到 GPT）
├── GPT_INSTRUCTIONS.md     - 系統提示詞（複製到 GPT）
└── GPT_SETUP_GUIDE.md      - 詳細設定指南

生成腳本與配置：
├── generate_tree.py        - 生成腳本
├── index.html              - API 說明頁
└── .github/workflows/      - CI/CD
```

### 🎯 整理目標

1. **減少冗餘** - 刪除 4 個重複文件
2. **清晰結構** - 每個文件有明確用途
3. **易於使用** - README 成為主要入口
4. **快速上手** - QUICK_START 保持簡潔

### 📊 文件用途

| 文件 | 用途 | 目標讀者 |
|------|------|----------|
| `README.md` | 專案概覽、API 說明、完整範例 | 所有用戶 |
| `QUICK_START.md` | 3 步驟快速配置 GPT | 想快速開始的用戶 |
| `GPT_SETUP_GUIDE.md` | 詳細設定步驟、故障排除 | 需要深入了解的用戶 |
| `GPT_ACTIONS_SCHEMA.yaml` | API 定義 | 直接複製使用 |
| `GPT_INSTRUCTIONS.md` | 系統提示詞 | 直接複製使用 |

### 💡 建議的閱讀順序

1. **快速開始** → `QUICK_START.md`（3 分鐘）
2. **完整了解** → `README.md`（10 分鐘）
3. **詳細配置** → `GPT_SETUP_GUIDE.md`（需要時）
4. **變更歷史** → `SNAPSHOT.md`（需要時）

---

## 2024-11-26 - 添加直接訪問 Markdown 內容的 API（解決 Web Browsing 限制）

### 📝 問題

GPT 的 Web Browsing 功能無法直接訪問 GitHub Pages 上的 Markdown 檔案：
- Web Browsing 對靜態檔案支援有限
- 無法可靠地獲取 .md 檔案內容
- 需要複雜的 URL encoding 處理

### 🔧 解決方案

**為每個 Markdown 檔案生成對應的 JSON 檔案**，通過 GPT Actions 直接訪問：

#### 新增功能

1. **檔案 ID 系統**
   - 為每個 MD 檔案生成唯一的 8 位 ID（MD5 hash 前 8 位）
   - 範例：`1. 個人知識管理/file.md` → file_id: `a1b2c3d4`

2. **檔案內容 JSON**（`api/files/{file_id}.json`）
   - 包含完整的 Markdown 內容
   - 包含檔案元資訊（名稱、路徑、大小、行數）
   - 總共 235 個檔案，總大小 976KB

3. **新增 API 端點**：`/api/files/{file_id}.json`
   - 直接通過 file_id 獲取內容
   - 不需要 URL encoding
   - 平均回應大小：~4KB

#### 修改的檔案

**generate_tree.py**：
- 新增 `generate_file_id()` 函數
- 新增 `generate_file_contents()` 函數
- 修改 `generate_search_index()` 添加 file_id 欄位
- 自動生成 `api/files/` 目錄和所有 JSON 檔案

**search.json**：
- 每個檔案增加 `file_id` 欄位
- 現在包含：name, path, file_id

**GPT_ACTIONS_SCHEMA.yaml**：
- 新增 `/api/files/{file_id}.json` 端點
- 定義 `getFileContent` operation
- 新增 `FileContent` schema

**GPT_INSTRUCTIONS.md**：
- 更新工作流程，使用 file_id 而非 Web Browsing
- 移除 URL encoding 說明
- 添加 getFileContent 使用範例

**GPT_CONFIG_SUMMARY.md**：
- 更新 API 端點列表
- 修改測試檢查清單
- 更新效能指標
- Web Browsing 不再需要 ❌

### 📊 新的 API 架構

```
用戶查詢流程：

1. getKnowledgeBaseIndex
   ↓ 返回分類摘要
   
2. searchKnowledgeBase（如需要）
   ↓ 返回檔案列表 + file_id
   
3. getFileContent(file_id)
   ↓ 返回完整內容
   
4. GPT 整合回答
```

### 📁 新增的檔案結構

```
api/
└── files/
    ├── a1b2c3d4.json  (檔案內容 + 元資訊)
    ├── b2c3d4e5.json
    ├── ...
    └── (總共 235 個檔案)
```

### 💡 優勢

1. **不依賴 Web Browsing**：使用純 Actions API
2. **簡化流程**：不需要 URL encoding
3. **穩定可靠**：標準 REST API 調用
4. **快速回應**：平均檔案大小 ~4KB
5. **易於除錯**：可以直接測試 file_id

### 🔄 使用範例

#### 舊方式（Web Browsing - 有問題）
```
1. 從 search 獲取路徑
2. 進行複雜的 URL encoding
3. 使用 Web Browsing 訪問
4. 可能失敗或無法訪問
```

#### 新方式（Actions - 推薦）✨
```
1. 從 search 獲取 file_id: "a1b2c3d4"
2. 調用 getFileContent(file_id="a1b2c3d4")
3. 立即獲得完整內容
```

### 📈 統計資訊

- **檔案數量**：235 個 Markdown 檔案
- **JSON 檔案總大小**：976KB
- **平均檔案大小**：~4KB
- **file_id 長度**：8 個字符（16^8 = 約 43 億種組合，無碰撞）

### ⚙️ 配置變更

**GPT Settings 需要修改**：
- ❌ Web Browsing：不再需要
- ✅ Actions：必須配置三個端點
  1. getKnowledgeBaseIndex
  2. searchKnowledgeBase
  3. getFileContent（新增）

### 🎯 完成狀態

- ✅ 為每個 MD 檔案生成 file_id
- ✅ 生成 235 個檔案內容 JSON
- ✅ 更新 search.json 包含 file_id
- ✅ 添加 getFileContent API 端點
- ✅ 更新 OpenAPI Schema
- ✅ 更新 GPT Instructions
- ✅ 更新配置文件

---

## 2024-11-26 - 優化 GPT Actions API（解決 ResponseTooLargeError）

### 📝 問題

GPT Actions 調用 `/tree.json` 時返回 `ResponseTooLargeError`：
- tree.json 大小：214KB，2937 行
- 包含完整的樹狀結構和所有 URL encoded 路徑
- 超過 OpenAI GPT Actions 的回應大小限制

### 🔧 解決方案

創建多層級 API 架構，提供不同詳細程度的端點：

#### 新增檔案

1. **index.json** - 輕量級索引（6.7KB，200 行）
   - 只包含分類摘要
   - 每個分類顯示總數和 3 個範例檔案
   - 專門為 GPT Actions 優化
   - 包含使用說明

2. **search.json** - 按分類搜索（42KB，1015 行）
   - 按分類列出所有檔案
   - 不包含完整 URL（節省空間）
   - 用於詳細搜索

3. **tree.json** - 完整樹狀結構（214KB，2937 行）
   - 保留原有的完整資訊
   - 包含樹狀結構和扁平列表
   - 用於其他用途

#### 修改檔案

**generate_tree.py**：
- 新增 `generate_lightweight_index()` 函數
- 新增 `generate_search_index()` 函數
- 更新忽略規則
- 修正 URL 為全小寫：`https://samliaop.github.io/obsidian_card`

#### 新增配置檔案

1. **GPT_ACTIONS_SCHEMA.yaml** - OpenAPI Schema
   - 定義兩個端點：`/index.json` 和 `/search.json`
   - 詳細的 schema 定義
   - 使用範例

2. **GPT_INSTRUCTIONS.md** - GPT 系統提示詞
   - 完整的工作流程說明
   - 搜索策略和技巧
   - 回答格式範本
   - 特殊情況處理

### 📊 檔案大小對比

| 檔案 | 大小 | 行數 | 用途 |
|------|------|------|------|
| index.json | 6.7KB | 200 | GPT Actions 主要端點 ✅ |
| search.json | 42KB | 1015 | 詳細搜索 |
| tree.json | 214KB | 2937 | 完整結構 |

### 🎯 API 使用流程

1. **首次調用**：`getKnowledgeBaseIndex` → 獲取分類概覽
2. **詳細搜索**（如需要）：`searchKnowledgeBase` → 獲取分類內所有檔案
3. **獲取內容**：使用 Web Browsing + URL encode 訪問檔案

### 💡 優化亮點

1. **分層設計**：根據需求選擇合適的端點
2. **節省頻寬**：只傳輸必要的資訊
3. **快速回應**：index.json 只有 6.7KB
4. **向後兼容**：保留完整的 tree.json

### 🔄 URL 修正

同時修正了 GitHub Pages URL 格式：
- 錯誤：`https://SamLiaoP.github.io/...`（大小寫混合）
- 正確：`https://samliaop.github.io/...`（全小寫）

OpenAI GPT Actions 要求 URL 必須嚴格匹配實際的 origin。

---

## 2024-11-26 - 修正 GitHub Pages URL

### 📝 問題修正

**問題**：設定了錯誤的 base_url 導致 API 端點返回 404

**原因**：混淆了 GitHub 倉庫 URL 和 GitHub Pages URL

**修正**：
- 錯誤：`https://github.com/SamLiaoP/obsidian_card`（倉庫 URL）
- 正確：`https://SamLiaoP.github.io/obsidian_card`（GitHub Pages URL）

**影響檔案**：
- `generate_tree.py` - 修正 base_url
- `tree.json` - 重新生成（236 個檔案）

---

## 2024-11-26 - 創建 GitHub Pages 靜態 API

### 📝 變更描述

建立了一個可以部署在 GitHub Pages 的靜態 API 系統，用於提供 Obsidian 知識庫中所有 Markdown 檔案的訪問接口。

### 🎯 實作目標

1. **根目錄返回完整樹狀結構 JSON**：透過 `/tree.json` 端點提供所有 md 檔案的結構化資訊
2. **所有 md 檔案可被 GET 請求訪問**：每個 Markdown 檔案都可以直接透過其路徑訪問
3. **作為 API 使用**：無前端設計，純粹作為資料接口

### 📦 新增檔案

#### 1. `generate_tree.py`
- **目的**：掃描專案中所有 Markdown 檔案並生成樹狀結構 JSON
- **功能**：
  - 遞迴掃描所有目錄
  - 忽略系統檔案和非 md 檔案
  - 生成樹狀結構和扁平檔案列表
  - 為每個檔案生成 URL（支援中文路徑的 URL encode）
- **輸出**：`tree.json`（235 個 Markdown 檔案）

#### 2. `index.html`
- **目的**：API 首頁，提供 API 說明和使用範例
- **功能**：
  - 顯示 API 文件
  - 提供 JavaScript、Python、cURL 使用範例
  - 自動載入並顯示檔案統計資訊
  - 連結到 `tree.json`
- **設計**：簡潔的響應式設計，無複雜前端功能

#### 3. `.github/workflows/deploy.yml`
- **目的**：自動化部署流程
- **觸發條件**：推送到 main/master 分支
- **工作流程**：
  1. Checkout 程式碼
  2. 設定 Python 環境
  3. 執行 `generate_tree.py` 生成最新的 `tree.json`
  4. 配置 GitHub Pages
  5. 上傳並部署到 GitHub Pages

#### 4. `README.md`
- **目的**：專案說明文件
- **內容**：
  - 快速開始指南
  - API 使用說明
  - 程式碼範例（JavaScript、Python、cURL）
  - 部署步驟
  - 設定說明

#### 5. `.gitignore`
- **目的**：忽略不需要版本控制的檔案
- **包含**：Python cache、IDE 設定、系統檔案、臨時檔案

#### 6. `tree.json`（自動生成）
- **目的**：API 資料檔案
- **內容**：
  - `base_url`: GitHub Pages 的基礎 URL
  - `total_files`: 總檔案數（235）
  - `tree`: 樹狀目錄結構
  - `files`: 扁平檔案列表

### 🔧 技術細節

#### 為什麼選擇這個架構？

1. **完全靜態**：不需要伺服器，GitHub Pages 免費託管
2. **自動更新**：透過 GitHub Actions 實現 CI/CD
3. **支援中文**：所有路徑都經過 URL encode 處理
4. **RESTful 設計**：標準的 HTTP GET 請求
5. **易於整合**：任何支援 HTTP 的程式語言都可以使用

#### URL Encoding 處理

中文檔案路徑範例：
- 原始路徑：`1. 個人知識管理/1.1 卡片盒筆記/檔案.md`
- 編碼後：`1.%20%E5%80%8B%E4%BA%BA%E7%9F%A5%E8%AD%98%E7%AE%A1%E7%90%86/...`

### 📊 統計資訊

- **總檔案數**：235 個 Markdown 檔案
- **主要分類**：
  - 個人知識管理
  - 海外工作計畫
  - 人生的價值觀
  - 軟體開發
  - 科普新知
  - 意識與大腦
  - 決策科學
  - 人工智能
  - 專案管理
  - 投資

### 🚀 如何部署

1. **修改基礎 URL**：編輯 `generate_tree.py` 中的 `base_url` 變數為你的 GitHub Pages URL
2. **推送到 GitHub**：`git push origin main`
3. **啟用 GitHub Pages**：在倉庫設定中啟用，選擇 "GitHub Actions" 作為來源
4. **等待部署**：GitHub Actions 會自動執行並部署

### 💡 使用範例

```bash
# 本地測試
python3 generate_tree.py
python3 -m http.server 8000

# 訪問
curl http://localhost:8000/tree.json
```

### ⚙️ 未來可能的改進

1. 添加搜索功能（客戶端 JavaScript）
2. 支援 Markdown 渲染預覽
3. 添加檔案標籤和分類系統
4. 提供 RSS feed
5. 添加 CORS 設定（如果需要跨域訪問）

### 🎯 完成狀態

- ✅ Python 腳本掃描 md 檔案並生成樹狀結構 JSON
- ✅ 創建 index.html 返回 JSON 結構和說明
- ✅ 創建 GitHub Actions workflow 自動構建
- ✅ 創建 README 說明部署方式
- ✅ 更新 SNAPSHOT.md
- ✅ 生成初始 tree.json（235 個檔案）

---

## 注意事項

1. **記得修改 `generate_tree.py` 中的 `base_url`**，改成你實際的 GitHub Pages URL
2. 所有 Markdown 檔案都會被公開訪問，確保沒有敏感資訊
3. GitHub Pages 有大小限制（建議不超過 1GB）
4. 免費版 GitHub Pages 僅支援公開倉庫

