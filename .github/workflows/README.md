# GitHub Actions Workflows

## 📋 Workflows 概覽

### 1. Deploy to GitHub Pages (`deploy.yml`)

**用途**：自動生成 API 並部署到 GitHub Pages

**觸發條件**：
- Push 到 `main` 或 `master` 分支
- 手動觸發（workflow_dispatch）

**執行步驟**：
1. Checkout 程式碼
2. 設定 Python 3.11
3. 執行 `generate_tree.py` 生成 API 檔案
4. 驗證 JSON 格式和必要欄位
5. 配置 GitHub Pages
6. 上傳並部署

**查看狀態**：
```
https://github.com/your-username/your-repo/actions
```

### 2. Test API Generation (`test.yml`)

**用途**：在 PR 時測試 API 生成

**觸發條件**：
- Pull Request 到 `main` 或 `master`
- 手動觸發（workflow_dispatch）

**執行步驟**：
1. Checkout 程式碼
2. 設定 Python 3.11
3. 執行 `generate_tree.py`
4. 驗證生成的檔案
5. 上傳測試結果 artifact（保留 7 天）

## 🚀 使用方式

### 自動觸發

**部署**：
```bash
git add .
git commit -m "Update notes"
git push origin main
# → 自動觸發 deploy.yml
```

**測試**：
```bash
git checkout -b feature/new-notes
git add .
git commit -m "Add new notes"
git push origin feature/new-notes
# 創建 PR → 自動觸發 test.yml
```

### 手動觸發

1. 前往 GitHub Actions 頁面
2. 選擇要運行的 workflow
3. 點擊 "Run workflow"
4. 選擇分支
5. 點擊綠色的 "Run workflow" 按鈕

## 📊 查看結果

### 部署 Workflow

**成功的日誌示例**：
```
🚀 開始生成 API 檔案...
✅ 成功生成 tree.json
📁 共找到 235 個 Markdown 檔案
✅ 生成完成！
📄 index.json: 6.8K
📄 search.json: 50K
📁 api/files/: 235 個檔案
🔍 驗證 API 檔案格式...
✅ 所有驗證通過！
```

**查看部署結果**：
```bash
curl https://your-username.github.io/your-repo/index.json
```

### 測試 Workflow

**下載測試結果**：
1. 前往 Actions 頁面
2. 點擊測試的 run
3. 滾動到底部的 "Artifacts"
4. 下載 `test-results`

## 🐛 故障排除

### 問題 1: Python 腳本失敗

**檢查**：
1. 查看 Actions 日誌
2. 找到 "Generate API files" 步驟
3. 檢查錯誤訊息

**常見原因**：
- Markdown 檔案格式錯誤
- Python 語法錯誤
- 檔案權限問題

### 問題 2: JSON 驗證失敗

**檢查**：
1. 查看 "Validate API files" 步驟
2. 哪個 JSON 檔案驗證失敗？

**解決**：
```bash
# 本地測試
python3 -m json.tool index.json
python3 -m json.tool search.json
python3 -m json.tool tree.json
```

### 問題 3: 部署失敗

**檢查**：
1. GitHub Pages 是否已啟用？
2. Settings > Pages > Source 是否設為 "GitHub Actions"？
3. 權限是否正確？

**解決**：
- 確認 deploy.yml 中的 permissions 設定
- 檢查倉庫是否為 public（免費帳號）

### 問題 4: Workflow 沒有觸發

**檢查**：
1. 分支名稱是否正確？（main vs master）
2. Workflow 檔案是否在正確位置？
3. YAML 格式是否正確？

**驗證 YAML**：
```bash
# 使用線上工具驗證
https://www.yamllint.com/
```

## ⚙️ 自訂配置

### 修改 Python 版本

編輯 workflow 檔案：
```yaml
- name: Setup Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.12'  # 修改版本
```

### 修改觸發分支

```yaml
on:
  push:
    branches:
      - main
      - develop  # 添加其他分支
```

### 添加通知

在 workflow 末尾添加：
```yaml
- name: Notify on success
  if: success()
  run: |
    echo "✅ 部署成功！"
    # 可以添加 Slack/Discord 通知
```

## 📈 監控建議

### 定期檢查

- 每週查看 Actions 頁面
- 確認沒有失敗的 runs
- 檢查部署時間是否正常

### 設定通知

1. GitHub 設定 > Notifications
2. 啟用 "Actions" 通知
3. 選擇通知方式（Email/Web/Mobile）

## 📚 相關資源

- [GitHub Actions 文檔](https://docs.github.com/actions)
- [GitHub Pages 文檔](https://docs.github.com/pages)
- [Python setup action](https://github.com/actions/setup-python)

---

**需要幫助？**查看主專案的 [GPT_SETUP_GUIDE.md](../../GPT_SETUP_GUIDE.md)

