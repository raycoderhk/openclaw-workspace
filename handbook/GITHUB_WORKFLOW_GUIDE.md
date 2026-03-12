# 🦞 OpenClaw GitHub 工作流指南

**如何用 AI 輔助完成整個 GitHub 開發流程 - 一行 code 都唔使寫！**

---

## 🎯 學習目標

完成呢個指南後，你可以：
- ✅ Clone 任何 OpenClaw 項目
- ✅ 用 AI 理解項目結構
- ✅ 用 AI 修改功能
- ✅ 本地測試
- ✅ Git Commit + Push
- ✅ 創建 Pull Request

---

## 📋 前置條件

### 需要安裝：

```bash
# Git
brew install git  # macOS
sudo apt install git  # Linux

# Node.js (大部分 OpenClaw 項目需要)
brew install node  # macOS
sudo apt install nodejs npm  # Linux

# GitHub CLI (可選，用於創建 PR)
brew install gh  # macOS
sudo apt install gh  # Linux

# 登入 GitHub
gh auth login
```

### OpenClaw 配置：

```bash
# 確保有 coding agent
openclaw config get agents

# 如果無，參考 Handbook 第 3 章配置
```

---

## 🚀 快速開始 (5 分鐘)

### Step 1: Clone 項目

```bash
# 搵到想修改嘅項目
# 例如：https://github.com/raycoderhk/kanban-board

cd ~/.openclaw/workspace
git clone https://github.com/raycoderhk/kanban-board.git
cd kanban-board
```

**或者用 AI 幫手：**
```bash
openclaw agent --profile coding "幫我 clone 呢個 repo: https://github.com/raycoderhk/kanban-board"
```

---

### Step 2: 用 AI 分析項目

```bash
openclaw agent --profile coding "
幫我分析呢個項目嘅結構：
1. 主要文件係咩
2. 點樣運行
3. 點樣修改功能
"
```

**預期輸出：**
```
📁 項目結構：
- index.html: 主界面
- server.js: 後端 API
- package.json: 依賴配置
- public/: 靜態文件

🚀 運行方法：
npm install && npm start

🔧 修改建議：
- 改 CSS: public/style.css
- 改功能：server.js
- 加功能：創建新文件
```

---

### Step 3: 用 AI 修改功能

**示例 1: 加優先級顏色**

```bash
openclaw agent --profile coding "
我想喺 Kanban Board 加優先級顏色：
- urgent: 紅色邊框 (#ef4444)
- high: 橙色邊框 (#f97316)
- medium: 黃色邊框 (#eab308)
- low: 綠色邊框 (#22c55e)

幫我修改 CSS 同 JavaScript。
"
```

**示例 2: 加搜索功能**

```bash
openclaw agent --profile coding "
我想加搜索功能：
1. 搜索框喺頂部
2. 可以搜索任務標題同描述
3. 實時過濾結果

幫我實現呢個功能。
"
```

**示例 3: 改 UI 配色**

```bash
openclaw agent --profile coding "
我想改 UI 配色：
- 背景：深藍色 (#1e3a8a)
- 卡片：白色 + 陰影
- 文字：白色/淺灰色

幫我修改 CSS。
"
```

---

### Step 4: 本地測試

```bash
# 安裝依賴
npm install

# 啟動服務
npm start

# 瀏覽器打開：http://localhost:3000
```

**或者用 AI 幫手：**
```bash
openclaw agent --profile coding "
幫我測試呢個項目：
1. 安裝依賴
2. 啟動服務
3. 檢查有無錯誤
"
```

---

### Step 5: Git Commit + Push

```bash
# 查看變更
git status
git diff

# 添加文件
git add .

# Commit
git commit -m "feat: 添加優先級顏色顯示"

# Push
git push origin main
```

**或者用 AI 幫手：**
```bash
openclaw agent --profile coding "
幫我 commit 同 push 呢啲修改：
- Commit message: feat: 添加優先級顏色顯示
- Push 到 main branch
"
```

---

### Step 6: 創建 Pull Request

**方法 A: GitHub CLI (推薦)**

```bash
# 創建 PR
gh pr create \
  --title "feat: 添加優先級顏色顯示" \
  --body "## 修改內容
- 添加優先級顏色 (urgent/high/medium/low)
- 修改 CSS 樣式
- 更新卡片渲染邏輯

## 測試
✅ 本地測試通過
✅ 無破壞性變更

## 截圖
![截圖](link-to-screenshot.png)"
```

**方法 B: GitHub 網站**

```
1. 去 GitHub repo 頁面
2. 點擊 "Pull requests" tab
3. 點擊 "New pull request"
4. 選擇你個 branch
5. 填寫：
   - Title: feat: 添加優先級顏色顯示
   - Description: 修改內容 + 測試結果
6. 點擊 "Create pull request"
```

**方法 C: AI 幫手**

```bash
openclaw agent --profile coding "
幫我創建一個 GitHub Pull Request：
- Title: feat: 添加優先級顏色顯示
- Body: 包括修改內容同測試結果
- Base: main
"
```

---

## 🛠️ 自動化腳本

我創建咗一個自動化腳本，可以一鍵完成成個流程：

```bash
# 下載腳本
curl -O https://raw.githubusercontent.com/raycoderhk/openclaw-knowledge/main/scripts/openclaw-github-workflow.sh
chmod +x openclaw-github-workflow.sh

# 使用
./openclaw-github-workflow.sh \
  "https://github.com/raycoderhk/kanban-board" \
  "添加優先級顏色顯示"
```

---

## 📊 完整工作流圖

```
┌─────────────────────────────────────────────────────────────┐
│              AI 輔助 GitHub 工作流                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1️⃣  Clone                                                │
│     git clone <repo-url>                                   │
│          ↓                                                  │
│  2️⃣  AI 分析                                               │
│     openclaw agent "分析項目結構"                           │
│          ↓                                                  │
│  3️⃣  AI 修改                                               │
│     openclaw agent "幫我改呢個功能..."                      │
│          ↓                                                  │
│  4️⃣  測試                                                   │
│     npm install && npm test                                │
│          ↓                                                  │
│  5️⃣  Git Commit                                            │
│     git add . && git commit -m "..."                       │
│          ↓                                                  │
│  6️⃣  Git Push                                              │
│     git push origin main                                   │
│          ↓                                                  │
│  7️⃣  Pull Request                                          │
│     gh pr create --title "..." --body "..."                │
│          ↓                                                  │
│  ✅  完成！                                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 💡 實用技巧

### 1. 用 Branch 開發

```bash
# 創建新 branch
git checkout -b feat/add-priority-colors

# 修改完後 push
git push origin feat/add-priority-colors

# 創建 PR
gh pr create --base main --head feat/add-priority-colors
```

### 2. AI 幫你寫 Commit Message

```bash
openclaw agent --profile coding "
根據呢啲變更，幫我寫一個 Git commit message：
$(git diff --stat)
"
```

### 3. AI 幫你寫 PR Description

```bash
openclaw agent --profile coding "
幫我寫一個 Pull Request description：
- 修改內容：$(git diff --name-only)
- 測試結果：通過
- 截圖：已附加
"
```

### 4. 代碼審查

```bash
# 叫 AI 幫你 review 自己嘅 code
openclaw agent --profile coding "
幫我 review 呢啲變更：
$(git diff)

有無潛在問題？可以點改進？
"
```

---

## ⚠️ 常見問題

### Q1: Git Push 失敗

```bash
# 可能原因：無權限 push 到 main
# 解決方法：創建 branch

git checkout -b feat/my-changes
git push origin feat/my-changes
gh pr create
```

### Q2: AI 修改錯嘢

```bash
# 用 Git 還原
git checkout HEAD -- <file-name>

# 或者還原所有
git reset --hard HEAD
```

### Q3: 測試失敗

```bash
# 叫 AI 幫你 debug
openclaw agent --profile coding "
測試失敗，錯誤訊息：
<粘贴錯誤訊息>

幫我 fix 呢個問題。
"
```

### Q4: 合併衝突

```bash
# 更新 main branch
git checkout main
git pull origin main

# 切換返你個 branch
git checkout feat/my-changes

# 合併
git merge main

# 如果有衝突，叫 AI 幫你 resolve
openclaw agent --profile coding "
有合併衝突，幫我 resolve：
<粘贴衝突內容>
"
```

---

## 📚 相關資源

- **GitHub Docs:** https://docs.github.com/
- **GitHub CLI:** https://cli.github.com/
- **OpenClaw Handbook:** (即將發布)
- **示例項目:** https://github.com/raycoderhk/kanban-board

---

## 🎯 下一步練習

1. **Clone 一個簡單項目** (例如：kanban-board)
2. **用 AI 加一個小功能** (例如：改顏色)
3. **本地測試**
4. **Git Push + 創建 PR**
5. **重複練習，直到熟練**

---

**記住：AI 係助手，你係決策者！** 🦞

**享受「一行 code 都唔使寫」嘅開發體驗！** 🚀
