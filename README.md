# 🗂️ CARD Knowledge Base API

這是一個可以部署在 GitHub Pages 的靜態 API，用於訪問 Obsidian 知識庫中的所有 Markdown 檔案，特別優化給 GPT Actions 使用。

## 🌟 特色

- ✅ **完全靜態** - 無需伺服器，GitHub Pages 免費託管
- ✅ **GPT Actions 優化** - 支援通過 file_id 直接訪問內容
- ✅ **自動生成索引** - 235 個 Markdown 檔案自動建立索引
- ✅ **支援中文** - 完整支援中文路徑和檔名
- ✅ **自動部署** - GitHub Actions CI/CD

## 📊 API 架構

| 端點 | 大小 | 用途 |
|------|------|------|
| `/index.json` | 6.8KB | 分類摘要（首次調用）|
| `/search.json` | 50KB | 完整檔案列表 + file_id |
| `/api/files/{file_id}.json` | ~4KB | 檔案完整內容 |
| `/tree.json` | 214KB | 完整樹狀結構 |

## 🚀 快速開始

### 方案 A：配置 GPT Actions（推薦）

**最快方式**：查看 [`QUICK_START.md`](QUICK_START.md)

簡要步驟：
1. 複製 `GPT_ACTIONS_SCHEMA.yaml` 到 GPT Actions
2. 複製 `GPT_INSTRUCTIONS.md` 到 GPT Instructions
3. 關閉 Web Browsing 功能

### 方案 B：本地測試

```bash
# 生成 API 檔案
python3 generate_tree.py

# 啟動本地伺服器
python3 -m http.server 8000

# 訪問
open http://localhost:8000
```

### 方案 C：部署到 GitHub Pages

```bash
# 1. 修改 base_url（generate_tree.py 第 142 行）
base_url = "https://your-username.github.io/your-repo"

# 2. 提交並推送
git add .
git commit -m "Deploy to GitHub Pages"
git push origin main

# 3. 啟用 GitHub Pages
# Settings > Pages > Source: GitHub Actions

# 4. 等待 1-2 分鐘部署完成
```

## 🔌 API 使用範例

### 使用 GPT Actions

```yaml
# GPT 會自動調用這些端點
getKnowledgeBaseIndex()  # 獲取分類摘要
searchKnowledgeBase()     # 搜索檔案
getFileContent(file_id)   # 獲取內容
```

### 使用 cURL

```bash
# 獲取索引
curl https://samliaop.github.io/obsidian_card/index.json

# 搜索檔案（獲取 file_id）
curl https://samliaop.github.io/obsidian_card/search.json

# 獲取檔案內容
curl https://samliaop.github.io/obsidian_card/api/files/02f15f5d.json
```

### 使用 Python

```python
import requests

BASE_URL = "https://samliaop.github.io/obsidian_card"

# 1. 獲取索引
index = requests.get(f"{BASE_URL}/index.json").json()
print(f"總共 {index['total_files']} 個檔案")

# 2. 搜索檔案
search = requests.get(f"{BASE_URL}/search.json").json()
first_file = search['categories'][0]['files'][0]
print(f"檔案: {first_file['name']}, ID: {first_file['file_id']}")

# 3. 獲取內容
content = requests.get(f"{BASE_URL}/api/files/{first_file['file_id']}.json").json()
print(f"內容: {content['content'][:100]}...")
```

### 使用 JavaScript

```javascript
const BASE_URL = 'https://samliaop.github.io/obsidian_card';

// 獲取索引並顯示分類
fetch(`${BASE_URL}/index.json`)
  .then(res => res.json())
  .then(index => {
    console.log(`共有 ${index.total_files} 個檔案`);
    index.categories.forEach(cat => {
      console.log(`${cat.category}: ${cat.count} 個`);
    });
  });
```

## 📖 完整文檔

| 文檔 | 說明 |
|------|------|
| [QUICK_START.md](QUICK_START.md) | ⭐ 快速配置 GPT（3 步驟）|
| [GPT_ACTIONS_SCHEMA.yaml](GPT_ACTIONS_SCHEMA.yaml) | OpenAPI Schema |
| [GPT_INSTRUCTIONS.md](GPT_INSTRUCTIONS.md) | GPT 系統提示詞 |
| [GPT_SETUP_GUIDE.md](GPT_SETUP_GUIDE.md) | 詳細設定指南 |
| [SNAPSHOT.md](SNAPSHOT.md) | 變更記錄 |

## 🔧 進階配置

### 修改 Base URL

編輯 `generate_tree.py` 第 142 行：

```python
base_url = "https://your-username.github.io/your-repo"
```

⚠️ **注意**：URL 必須全小寫（OpenAI 要求）

### 忽略特定檔案

編輯 `generate_tree.py` 第 16-20 行：

```python
ignore_patterns = {
    '.git', '.github', 'api',
    'your-folder-to-ignore',
    # ...
}
```

### 更新內容

```bash
# 編輯 Markdown 檔案後
python3 generate_tree.py  # 重新生成
git add .
git commit -m "Update content"
git push                   # 自動部署
```

## 📁 專案結構

```
CARD/
├── api/                        # API 端點
│   └── files/                  # 檔案內容 JSON
│       ├── 02f15f5d.json      # file_id.json
│       └── ... (235 個檔案)
│
├── .github/workflows/
│   └── deploy.yml             # 自動部署配置
│
├── index.json                 # 輕量級索引 (6.8KB)
├── search.json                # 搜索索引 (50KB)
├── tree.json                  # 完整結構 (214KB)
│
├── generate_tree.py           # 生成腳本
├── index.html                 # API 說明頁
│
├── GPT_ACTIONS_SCHEMA.yaml   # 複製到 GPT
├── GPT_INSTRUCTIONS.md        # 複製到 GPT
├── GPT_SETUP_GUIDE.md         # 設定指南
├── QUICK_START.md             # 快速開始
├── SNAPSHOT.md                # 變更記錄
└── README.md                  # 本文件
```

## 🎯 使用情境

### 情境 1：GPT 知識庫助手（主要用途）

1. 配置 GPT Actions（查看 `QUICK_START.md`）
2. GPT 自動訪問你的知識庫
3. 用戶可以問任何問題，GPT 從筆記中找答案

### 情境 2：個人知識庫 API

```python
# 從程式中訪問你的筆記
import requests

def get_note(keyword):
    search = requests.get(f"{BASE_URL}/search.json").json()
    for cat in search['categories']:
        for file in cat['files']:
            if keyword in file['name']:
                content = requests.get(
                    f"{BASE_URL}/api/files/{file['file_id']}.json"
                ).json()
                return content['content']
```

### 情境 3：分享知識庫

直接分享 URL，其他人可以：
- 瀏覽索引：`/index.json`
- 搜索主題：`/search.json`
- 閱讀內容：`/api/files/{file_id}.json`

## 🧪 測試

### 測試本地 API

```bash
# 測試索引
curl http://localhost:8000/index.json | python3 -m json.tool

# 測試搜索
curl http://localhost:8000/search.json | python3 -m json.tool | head -50

# 測試內容
curl http://localhost:8000/api/files/02f15f5d.json | python3 -m json.tool
```

### 測試部署後的 API

```bash
curl https://your-username.github.io/your-repo/index.json

# 檢查回應時間
time curl -o /dev/null -s https://your-username.github.io/your-repo/index.json
```

### 測試 GPT Actions

在 GPT Actions 設定頁面：

1. **getKnowledgeBaseIndex**: `{}`
2. **searchKnowledgeBase**: `{}`  
3. **getFileContent**: `{"file_id": "02f15f5d"}`

## ⚠️ 注意事項

### GitHub Pages 限制
- 單一檔案上限：100MB
- 總大小建議：< 1GB
- 免費帳號僅支援公開倉庫

### URL 格式
- ✅ 全小寫：`samliaop.github.io`
- ❌ 大小寫混合：`SamLiaoP.github.io`（OpenAI 不接受）

### 中文支援
- 路徑自動 URL encode
- 使用 file_id 訪問，不需要手動 encode

## 🔄 維護與更新

### 日常更新

```bash
# 1. 編輯 Markdown 檔案
vim "分類/檔案.md"

# 2. 重新生成（自動更新 file_id）
python3 generate_tree.py

# 3. 提交
git add .
git commit -m "Update notes"
git push
```

### 添加新分類

```bash
# 1. 創建新資料夾和檔案
mkdir "新分類"
echo "# 內容" > "新分類/新主題.md"

# 2. 重新生成
python3 generate_tree.py

# 3. 提交
git add .
git commit -m "Add new category"
git push
```

### 檢查部署狀態

```bash
# 查看 GitHub Actions
https://github.com/your-username/your-repo/actions

# 驗證部署
curl https://your-username.github.io/your-repo/index.json
```

## 💡 效能優化

| 指標 | 數值 |
|------|------|
| 索引回應時間 | ~100ms |
| 搜索回應時間 | ~200ms |
| 內容回應時間 | ~150ms |
| 完整查詢流程 | ~4-5 秒 |

## 🐛 常見問題

### Q1: GPT 無法訪問內容？

**檢查**：
1. Actions 是否配置 `getFileContent`？
2. URL 是否全小寫？
3. GitHub Pages 是否已部署？

### Q2: file_id 不存在？

```bash
# 重新生成所有檔案
python3 generate_tree.py

# 檢查 file_id
curl .../search.json | grep "file_id"
```

### Q3: 部署失敗？

```bash
# 查看 GitHub Actions 日誌
https://github.com/your-username/your-repo/actions

# 常見原因：
# - Python 腳本有錯誤
# - 權限設定問題
# - Pages 未啟用
```

## 📈 統計資訊

- **Markdown 檔案**：235 個
- **總分類**：10 個主要分類
- **JSON 檔案**：235 個內容檔案
- **總大小**：~1.2 MB（含所有 API 檔案）
- **平均檔案大小**：~4 KB

## 🤝 貢獻

歡迎提交 Issue 或 Pull Request！

## 📄 授權

MIT License

---

**開始使用**：查看 [`QUICK_START.md`](QUICK_START.md) 🚀
