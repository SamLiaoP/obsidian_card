## 1. 初始化 (Init)
開始一個新的 Git 儲存庫，或是複製現有的儲存庫。
- `git clone [repository-url]`
	- 從遠端儲存庫複製一份到本地，這樣你就可以在自己的機器上開始工作。
![[截圖 2024-04-22 下午5.22.05.png]]
## 2. 建立功能分支 (Feature Branch)
為了開發新功能或修正錯誤，從主分支(main)上分割出新的分支。(這樣才不會讓主分支無法工作)
- `git checkout -b my-feature`
	- 建立並切換到一個新的分支叫做 `my-feature`。
![[截圖 2024-04-22 下午5.22.22.png]]
## 3. 修改程式碼 (Code Changes)
進行實際的程式碼修改或新增。
- `git diff`
	- 顯示自從最後一次提交後，程式碼有哪些變更。
![[截圖 2024-04-22 下午5.22.56.png]]
## 4. 上交更改到遠端儲存庫 (Commit and Push)
將修改後的程式碼儲存並推送到遠端儲存庫。
- `git add <changed_file>`
	- 將變更過的檔案加入到暫存區，盡量不要使用 git add .
- `git commit -m "commit message"`
	- 將加入暫存區的檔案提交到儲存庫，並附加提交訊息。
- `git push origin my-feature`
	- 將本地分支的更新推送到遠端儲存庫。

### 處理分支上的更新
如果在你工作時主分支有了更新，需要將這些更新合併到你的分支上。
- `git checkout main`
	- 切換回主分支。
- `git pull origin master`
	- 從遠端同步最新的主分支到本地。
- `git checkout my-feature`
	- 切換回你的功能分支。
- `git rebase main`
	- 將主分支的更新重新套用到你的功能分支上。如果遇到衝突，需要手動解決。
	- rebase 基本上是 先把 main 抓下來，接著嘗試把這次的改動放到main中，創造分支。跟merge 直接合併後創造新分支有所不同。
	- `rebase` 重新定位分支上的提交，創造乾淨、線性的歷史；而 `merge` 保留了分支的歷史，通過創建一個新的合併提交來整合兩個分支。`rebase` 更適合私人分支以簡化歷史，`merge` 則適合公共分支以保留完整的合作痕跡。![[截圖 2024-04-22 下午5.24.45.png]]
- `git push -f origin my-feature`
	- 使用 `-f` 強制推送更新到遠端功能分支，尤其是在 rebase 之後。![[截圖 2024-04-22 下午5.25.21.png]]

## 5. 建立拉取請求 (Pull Request)
當功能開發完成後，建立一個拉取請求 (PR)，請求將功能分支合併回主分支。
- 在 GitHub 上建立 Pull Request，選擇 `Squash and merge` 以整合提交記錄。
	- Squash and Merge
		- 將功能分支的多個提交記錄壓縮為一個，以保持主分支的提交記錄清晰。

## 6. 刪除分支 (Delete Branch)
功能合併後，刪除功能分支。
- 在 GitHub 上刪除 `my-feature` 分支。
- `git branch -D my-feature`
	- 在本地刪除功能分支。
- `git pull origin master`
	- 更新本地的主分支。


資料來源：https://www.youtube.com/watch?v=uj8hjLyEBmU
