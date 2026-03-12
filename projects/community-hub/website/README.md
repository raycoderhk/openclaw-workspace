# 🏘️ 愉城社區 Hub - Website MVP

靜態網站，展示從 WhatsApp 聊天提取的社區知識。

## 📊 當前數據

- **有用提示**: 130+ 條 (持續增加中)
- **分類**: 12 個類別
- **數據來源**: 愉景新城街坊組 WhatsApp
- **背景分類**: 🔄 進行中 (目標：13,659 條)

## 🚀 本地預覽

```bash
# 方法 1: Python
cd website
python3 -m http.server 8000
# 訪問：http://localhost:8000

# 方法 2: Node.js
npx serve website
```

## 🌐 部署到 GitHub Pages

```bash
# 1. 初始化 Git (如果未初始化)
cd /home/node/.openclaw/workspace/projects/community-hub
git init
git add .
git commit -m "Initial community hub website"

# 2. 創建 gh-pages 分支
git checkout --orphan gh-pages
git rm -rf .
git checkout main -- website/
mv website/* .
mv website/.* . 2>/dev/null || true
rm -rf website src raw output node_modules package.json
git add .
git commit -m "Deploy website to gh-pages"
git push origin gh-pages

# 3. 啟用 GitHub Pages
# Settings → Pages → Source: gh-pages branch
```

## 🌐 部署到 Zeabur

```bash
# 1. 安裝 Zeabur CLI
npm install -g zeabur

# 2. 登入
zeabur login

# 3. 部署
cd website
zeabur init
zeabur deploy
```

## 📁 文件結構

```
website/
├── index.html              # 主頁面
├── app.js                  # 前端邏輯
├── classified_messages_useful.json  # 分類數據
└── README.md
```

## 🎨 功能

- ✅ 分類篩選 (12 個類別)
- ✅ 全文搜索
- ✅ 響應式設計 (手機/桌面)
- ✅ 統計數據展示
- ✅ 自動排序 (最新優先)

## 🔄 更新數據

當背景分類完成後：

```bash
cd /home/node/.openclaw/workspace/projects/community-hub
cp output/classified_messages_useful.json website/
# 重新部署
```

## 📱 類別說明

| 類別 | 圖標 | 內容 |
|------|------|------|
| traffic | 🚗 | 交通、巴士、MTR、路况 |
| restaurant | 🍽️ | 餐廳推薦、美食 |
| doctor | 🏥 | 醫生、診所推薦 |
| repair | 🔧 | 水喉、冷氣、維修師傅 |
| tech_tip | 📱 | 科技貼士、APP、電話計劃 |
| shopping | 🛒 | 購物、優惠碼、邊度買 |
| service | 📦 | 服務、物流、租貸 |
| community | 🏠 | 社區、管理處、設施 |
| event | 📅 | 活動、聚會、運動 |
| news | 📰 | 新聞、學校通知 |
| education | 📚 | 教育、補習、課程 |
| childcare | 👶 | 親子、玩具、兒童活動 |

---

**MVP 版本**: 2026-03-12  
**開發者**: Jarvis (AI Assistant)  
**數據**: 愉景新城街坊組鄰居貢獻
