# 🚀 快速部署指南

## 部署前準備

### 步驟 1: 修改基礎 URL

編輯 `generate_tree.py` 的第 78 行，將 `{username}` 替換為你的 GitHub 使用者名稱：

```python
base_url = "https://your-github-username.github.io/CARD"
```

例如：
- 如果你的 GitHub 帳號是 `john`，改成：`https://john.github.io/CARD`
- 如果倉庫名稱不是 `CARD`，也要相應修改

### 步驟 2: 本地測試（可選但建議）

```bash
# 生成 tree.json
python3 generate_tree.py

# 啟動本地伺服器
python3 -m http.server 8000

# 在瀏覽器打開
# http://localhost:8000
# http://localhost:8000/tree.json
```

## 部署到 GitHub Pages

### 方法一：命令列部署

```bash
# 1. 初始化 Git（如果還沒有的話）
git init
git add .
git commit -m "Initial commit: Static API for Obsidian notes"

# 2. 連接到 GitHub 倉庫
git remote add origin https://github.com/your-username/CARD.git

# 3. 推送到 GitHub
git branch -M main
git push -u origin main
```

### 方法二：GitHub Desktop

1. 開啟 GitHub Desktop
2. 選擇 File > Add Local Repository
3. 選擇此資料夾
4. Commit 所有變更
5. Publish repository

## 啟用 GitHub Pages

1. 進入你的 GitHub 倉庫頁面
2. 點擊 `Settings`（設定）
3. 在左側選單點擊 `Pages`
4. 在 `Source` 下拉選單中選擇 **`GitHub Actions`**
5. 儲存

## 等待部署完成

1. 點擊倉庫上方的 `Actions` 標籤
2. 你會看到一個正在執行的 workflow："Deploy to GitHub Pages"
3. 等待綠色勾勾出現（通常需要 1-2 分鐘）
4. 部署完成後，在 Settings > Pages 會看到你的網站 URL

## 驗證部署

訪問以下 URL 確認部署成功：

```
# 主頁
https://your-username.github.io/CARD/

# API 端點
https://your-username.github.io/CARD/tree.json

# 測試訪問一個 md 檔案
https://your-username.github.io/CARD/1.%20個人知識管理/...
```

## 測試 API

### 使用 cURL

```bash
# 獲取檔案樹
curl https://your-username.github.io/CARD/tree.json | jq '.'

# 獲取總檔案數
curl https://your-username.github.io/CARD/tree.json | jq '.total_files'

# 列出所有檔案
curl https://your-username.github.io/CARD/tree.json | jq '.files[].name'
```

### 使用 Python

```python
import requests
import json

# 獲取 API 資料
url = "https://your-username.github.io/CARD/tree.json"
response = requests.get(url)
data = response.json()

print(f"總共有 {data['total_files']} 個 Markdown 檔案")

# 訪問第一個檔案
first_file = data['files'][0]
print(f"\n第一個檔案：{first_file['name']}")
print(f"路徑：{first_file['path']}")

# 下載檔案內容
content = requests.get(first_file['url']).text
print(f"\n內容預覽：{content[:200]}...")
```

### 使用 JavaScript

```javascript
// 在瀏覽器 Console 中執行
fetch('https://your-username.github.io/CARD/tree.json')
  .then(res => res.json())
  .then(data => {
    console.log(`總共有 ${data.total_files} 個檔案`);
    console.log('檔案列表:', data.files);
    
    // 獲取第一個檔案
    return fetch(data.files[0].url);
  })
  .then(res => res.text())
  .then(content => console.log('檔案內容:', content));
```

## 更新內容

當你修改了 Markdown 檔案後：

```bash
# 1. Commit 變更
git add .
git commit -m "Update notes"

# 2. 推送到 GitHub
git push

# 3. GitHub Actions 會自動重新生成 tree.json 並部署
# 等待 1-2 分鐘即可看到更新
```

## 常見問題

### Q: 為什麼訪問中文路徑的檔案會 404？

A: 確保使用 tree.json 中提供的 URL，因為中文路徑已經過 URL encode。

### Q: 可以限制訪問權限嗎？

A: GitHub Pages 在免費版本中只能是公開的。如果需要私密訪問，需要升級到 GitHub Pro 或使用其他託管方案。

### Q: 檔案太多會不會有問題？

A: 目前有 235 個檔案，完全沒問題。GitHub Pages 建議總大小不超過 1GB。

### Q: 可以添加搜索功能嗎？

A: 可以！在 index.html 中添加客戶端 JavaScript 來實作搜索，因為所有資料都在 tree.json 中。

### Q: 如何追蹤 API 使用情況？

A: 可以整合 Google Analytics 或其他分析工具到 index.html 中。

## 進階功能

### 添加 CORS 支援

如果需要從其他網域訪問這個 API，可以在根目錄創建 `_headers` 檔案：

```
/*
  Access-Control-Allow-Origin: *
  Access-Control-Allow-Methods: GET, OPTIONS
  Access-Control-Allow-Headers: Content-Type
```

### 自訂網域

1. 在倉庫根目錄創建 `CNAME` 檔案
2. 內容為你的網域名稱，例如：`api.yourdomain.com`
3. 在你的 DNS 設定中添加 CNAME 記錄指向 `your-username.github.io`

### 添加快取控制

修改 `.github/workflows/deploy.yml`，在部署前添加 `_headers` 檔案來控制快取。

## 需要幫助？

- 查看 README.md 了解更多使用範例
- 查看 SNAPSHOT.md 了解系統架構
- 在 GitHub Issues 中提問

---

祝部署順利！🎉

