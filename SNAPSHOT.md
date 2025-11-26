# SNAPSHOT - 專案變更記錄

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

