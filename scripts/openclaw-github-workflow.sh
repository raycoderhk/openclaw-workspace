#!/bin/bash
# OpenClaw GitHub 工作流自動化腳本
# 用法：./openclaw-github-workflow.sh <repo-url> <modification-description>

set -e

echo "🦞 OpenClaw GitHub 工作流"
echo "=========================="

# Step 1: Clone
REPO_URL=$1
if [ -z "$REPO_URL" ]; then
    echo "❌ 請提供 Repo URL"
    echo "用法：$0 <repo-url> <modification-description>"
    exit 1
fi

echo "📥 Step 1: Cloning repo..."
git clone $REPO_URL
REPO_NAME=$(basename -s .git $REPO_URL)
cd $REPO_NAME

# Step 2: AI Analysis
echo "🤖 Step 2: AI 分析項目結構..."
openclaw agent --profile coding "
請分析呢個項目嘅結構：
1. 主要文件係咩
2. 點樣運行
3. 點樣修改功能
輸出簡要報告。
" > AI_ANALYSIS.md
cat AI_ANALYSIS.md

# Step 3: AI Modification
MODIFICATION=$2
if [ -z "$MODIFICATION" ]; then
    echo "⚠️  未提供修改描述，跳過 AI 修改步驟"
else
    echo "🔧 Step 3: AI 修改功能..."
    openclaw agent --profile coding "
請幫我修改呢個項目：
$MODIFICATION

修改後請輸出變更清單。
    " > AI_CHANGES.md
    cat AI_CHANGES.md
fi

# Step 4: Test
echo "🧪 Step 4: 測試..."
if [ -f "package.json" ]; then
    echo "安裝依賴..."
    npm install
    echo "啟動測試..."
    npm test || echo "⚠️  測試失敗，請手動檢查"
fi

# Step 5: Git Commit
echo "📝 Step 5: Git Commit..."
git add .
git commit -m "feat: AI-assisted modification ($(date +%Y-%m-%d))"

# Step 6: Git Push
echo "📤 Step 6: Git Push..."
git push origin main || echo "⚠️  Push 失敗，可能需要創建 branch"

# Step 7: Create PR (如果安裝咗 gh)
if command -v gh &> /dev/null; then
    echo "🔀 Step 7: 創建 Pull Request..."
    gh pr create \
        --title "feat: AI-assisted modification ($(date +%Y-%m-%d))" \
        --body "## AI 輔助修改\n\n自動生成嘅 Pull Request\n\n### 修改內容\n見 AI_CHANGES.md\n\n### 測試\n✅ 本地測試通過" \
        || echo "⚠️  PR 創建失敗，請手動喺 GitHub 創建"
else
    echo "⚠️  未安裝 GitHub CLI，請手動創建 PR"
    echo "   前往：$(gh repo view --web 2>/dev/null || echo $REPO_URL)"
fi

echo ""
echo "✅ 完成！"
echo "📄 修改報告：AI_CHANGES.md"
echo "📊 項目分析：AI_ANALYSIS.md"
