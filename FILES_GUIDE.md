# 📂 文件導覽

## 🚀 快速開始（選一個）

| 如果你想... | 看這個文件 | 時間 |
|------------|-----------|------|
| 最快配置 GPT | [`QUICK_START.md`](QUICK_START.md) | 3 分鐘 |
| 了解整個專案 | [`README.md`](README.md) | 10 分鐘 |
| 詳細設定步驟 | [`GPT_SETUP_GUIDE.md`](GPT_SETUP_GUIDE.md) | 20 分鐘 |

## 📁 文件結構

### 1️⃣ 用戶文檔（閱讀用）

```
README.md                   ⭐ 從這裡開始
├── 專案介紹
├── API 架構說明
├── 快速開始（3 種方案）
├── 使用範例（cURL, Python, JavaScript）
├── 進階配置
├── 常見問題
└── 維護更新

QUICK_START.md              ⭐ 最快上手
├── 3 步驟配置 GPT
├── 測試方法
└── 部署指南

GPT_SETUP_GUIDE.md          📖 詳細指南
├── 完整設定步驟
├── 測試檢查清單
├── 常見問題排查
├── 優化建議
└── 進階功能

SNAPSHOT.md                 📝 變更記錄
└── 所有版本變更歷史
```

### 2️⃣ GPT 配置文件（複製用）

```
GPT_ACTIONS_SCHEMA.yaml     📋 複製到 GPT Actions
└── OpenAPI 3.1 定義
    ├── getKnowledgeBaseIndex
    ├── searchKnowledgeBase
    └── getFileContent

GPT_INSTRUCTIONS.md         📋 複製到 GPT Instructions
└── 系統提示詞（290 行）
    ├── 角色定位
    ├── 工作流程
    ├── 搜索技巧
    └── 回答格式
```

### 3️⃣ 核心腳本（系統用）

```
generate_tree.py            🔧 生成 API 檔案
├── 掃描 Markdown 檔案
├── 生成 file_id
├── 生成 index.json
├── 生成 search.json
└── 生成 api/files/*.json

index.html                  🌐 API 說明頁
└── 線上查看 API 文檔

.github/workflows/deploy.yml
└── 自動部署到 GitHub Pages
```

## 🎯 使用情境

### 情境 1：我想快速配置 GPT

```
1. 閱讀 QUICK_START.md（3 分鐘）
2. 複製 GPT_ACTIONS_SCHEMA.yaml
3. 複製 GPT_INSTRUCTIONS.md
4. 完成！
```

### 情境 2：我想了解整個專案

```
1. 閱讀 README.md（10 分鐘）
   ├── 了解 API 架構
   ├── 查看使用範例
   └── 學習部署方法
2. 有問題？查看 GPT_SETUP_GUIDE.md
```

### 情境 3：我遇到問題

```
1. 查看 README.md > 常見問題
2. 查看 GPT_SETUP_GUIDE.md > 常見問題排查
3. 查看 SNAPSHOT.md > 了解最新變更
```

### 情境 4：我想修改配置

```
1. 查看 README.md > 進階配置
2. 編輯 generate_tree.py
3. 重新生成：python3 generate_tree.py
```

## 📊 文件大小與內容

| 文件 | 大小 | 主要內容 |
|------|------|----------|
| `README.md` | 8.5KB | 專案總覽、範例、FAQ |
| `QUICK_START.md` | 4.0KB | 3 步驟快速配置 |
| `GPT_SETUP_GUIDE.md` | 6.9KB | 詳細設定、故障排除 |
| `GPT_ACTIONS_SCHEMA.yaml` | 5.2KB | OpenAPI 定義 |
| `GPT_INSTRUCTIONS.md` | 7.9KB | 系統提示詞 |
| `SNAPSHOT.md` | 13KB | 完整變更歷史 |
| `generate_tree.py` | 10KB | 生成腳本 |
| `index.html` | 6.0KB | API 說明頁 |

**總計**：8 個核心文件，~61KB

## 🗂️ 完整目錄結構

```
CARD/
│
├── 📚 文檔（你需要閱讀的）
│   ├── README.md               ⭐ 主文檔
│   ├── QUICK_START.md          ⭐ 快速開始
│   ├── GPT_SETUP_GUIDE.md      📖 詳細指南
│   ├── SNAPSHOT.md             📝 變更記錄
│   └── FILES_GUIDE.md          📂 本文件
│
├── 🤖 GPT 配置（複製到 GPT）
│   ├── GPT_ACTIONS_SCHEMA.yaml
│   └── GPT_INSTRUCTIONS.md
│
├── 🔧 核心腳本（系統使用）
│   ├── generate_tree.py
│   └── index.html
│
├── 🌐 API 端點（自動生成）
│   ├── index.json              (6.8KB)
│   ├── search.json             (50KB)
│   ├── tree.json               (214KB)
│   └── api/
│       └── files/
│           └── *.json          (235 個檔案)
│
├── ⚙️ 自動部署
│   └── .github/
│       └── workflows/
│           └── deploy.yml
│
└── 📝 你的筆記（Markdown 檔案）
    ├── 1. 個人知識管理/
    ├── 2. 海外工作計畫/
    ├── 3. 人生的價值觀/
    └── ... (10 個分類，235 個檔案)
```

## 💡 推薦閱讀順序

### 第一次使用（總計 15 分鐘）

1. **QUICK_START.md** (3 分鐘)
   - 快速了解如何配置

2. **README.md** (10 分鐘)
   - 了解整體架構
   - 查看使用範例

3. **開始配置** (2 分鐘)
   - 複製 Schema 和 Instructions

### 遇到問題時

1. **README.md > 常見問題** (2 分鐘)
2. **GPT_SETUP_GUIDE.md > 故障排查** (5 分鐘)
3. **SNAPSHOT.md** (了解最新變更)

### 深入學習（需要時）

1. **GPT_SETUP_GUIDE.md** (20 分鐘)
   - 完整設定流程
   - 優化建議
   - 進階功能

2. **generate_tree.py** (10 分鐘)
   - 了解如何生成 API
   - 自訂配置

## 📖 常見問題

### Q: 文件太多，該看哪個？

**A**: 只需要看 2 個！
1. `QUICK_START.md` - 配置 GPT
2. `README.md` - 了解使用方法

### Q: 我只想複製貼上，不想看文檔

**A**: 
1. 複製 `GPT_ACTIONS_SCHEMA.yaml` → GPT Actions
2. 複製 `GPT_INSTRUCTIONS.md` → GPT Instructions
3. 完成！

### Q: 檔案會不會過時？

**A**: 
- `SNAPSHOT.md` 記錄所有變更
- 每次更新都會標註日期
- 舊的說明會被刪除或合併

### Q: 我可以刪除某些文件嗎？

**A**: 
| 可以刪除 | 不能刪除 |
|---------|---------|
| SNAPSHOT.md（如果不需要歷史）| README.md |
| GPT_SETUP_GUIDE.md（如果已配置好）| QUICK_START.md |
| FILES_GUIDE.md（本文件）| GPT_ACTIONS_SCHEMA.yaml |
| | GPT_INSTRUCTIONS.md |
| | generate_tree.py |

## 🎯 下一步

根據你的目標選擇：

**🚀 我想立即使用**
→ 打開 [`QUICK_START.md`](QUICK_START.md)

**📚 我想先了解**
→ 打開 [`README.md`](README.md)

**🔧 我想深入配置**
→ 打開 [`GPT_SETUP_GUIDE.md`](GPT_SETUP_GUIDE.md)

**📝 我想看變更歷史**
→ 打開 [`SNAPSHOT.md`](SNAPSHOT.md)

---

**找到你需要的文件，開始使用！** 🎉

