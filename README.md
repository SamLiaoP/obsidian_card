# CARD Knowledge Base API

這是一個可以部署在 GitHub Pages 的靜態 API，用於訪問 Obsidian 知識庫中的所有 Markdown 檔案。

## 🌟 特色

- ✅ 完全靜態，無需伺服器
- ✅ 自動生成檔案樹狀結構
- ✅ 支援中文路徑和檔名
- ✅ RESTful API 風格
- ✅ 自動部署到 GitHub Pages

## 🚀 快速開始

### 本地測試

1. **生成檔案樹**

```bash
python generate_tree.py
```

2. **啟動本地伺服器**

```bash
python -m http.server 8000
```

3. **訪問 API**

- 瀏覽器打開: http://localhost:8000
- API 端點: http://localhost:8000/tree.json

### 部署到 GitHub Pages

1. **推送到 GitHub**

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **啟用 GitHub Pages**

- 進入倉庫的 Settings > Pages
- Source 選擇 "GitHub Actions"
- 等待自動部署完成

3. **訪問你的 API**

部署完成後，你的 API 將可以在以下網址訪問：
```
https://{username}.github.io/{repo-name}/
```

## 📖 API 使用說明

### 端點 1: 獲取完整檔案樹

```
GET /tree.json
```

**回應格式：**

```json
{
  "base_url": "https://username.github.io/CARD",
  "total_files": 123,
  "generated_at": "2024-11-26T12:00:00Z",
  "tree": {
    "name": "root",
    "type": "directory",
    "path": "",
    "children": [...]
  },
  "files": [
    {
      "name": "檔案名稱.md",
      "path": "資料夾/檔案名稱.md",
      "url": "https://..."
    }
  ]
}
```

### 端點 2: 訪問 Markdown 檔案

```
GET /{path-to-file}.md
```

直接返回 Markdown 檔案的原始內容。

## 💻 使用範例

### JavaScript

```javascript
// 獲取檔案樹
fetch('https://username.github.io/CARD/tree.json')
  .then(res => res.json())
  .then(data => {
    console.log(`共有 ${data.total_files} 個檔案`);
    console.log('所有檔案:', data.files);
  });

// 獲取特定檔案
fetch(data.files[0].url)
  .then(res => res.text())
  .then(markdown => console.log(markdown));
```

### Python

```python
import requests

# 獲取檔案樹
response = requests.get('https://username.github.io/CARD/tree.json')
data = response.json()

print(f"共有 {data['total_files']} 個檔案")

# 獲取第一個檔案
file_url = data['files'][0]['url']
content = requests.get(file_url).text
print(content)
```

### cURL

```bash
# 獲取檔案樹
curl https://username.github.io/CARD/tree.json

# 獲取特定檔案（需要 URL encode）
curl "https://username.github.io/CARD/path/to/file.md"
```

## 🔧 設定

### 修改基礎 URL

編輯 `generate_tree.py` 中的 `base_url` 變數：

```python
# 格式: https://{username}.github.io/{repo-name}
base_url = "https://your-username.github.io/CARD"
```

### 忽略特定檔案或資料夾

在 `generate_tree.py` 的 `should_ignore()` 函數中添加：

```python
ignore_patterns = {
    '.git', '.github', 'node_modules',
    '你想忽略的資料夾名稱',
    # ...
}
```

## 📁 專案結構

```
CARD/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions 部署設定
├── generate_tree.py            # 生成檔案樹的 Python 腳本
├── index.html                  # API 首頁和說明文件
├── tree.json                   # 自動生成的檔案樹（部署時生成）
├── README.md                   # 本文件
└── [你的 Markdown 檔案和資料夾]
```

## 🔄 自動更新

每次推送到 `main` 分支時，GitHub Actions 會自動：
1. 執行 `generate_tree.py` 生成最新的 `tree.json`
2. 部署所有內容到 GitHub Pages

## ⚠️ 注意事項

1. **檔案大小限制**: GitHub Pages 單一檔案上限為 100MB
2. **總大小限制**: 整個站點建議不超過 1GB
3. **中文路徑**: 所有的中文路徑都會自動 URL encode
4. **私有倉庫**: GitHub Pages 在免費帳號中僅支援公開倉庫

## 🤝 貢獻

歡迎提交 Issue 或 Pull Request！

## 📄 授權

MIT License

