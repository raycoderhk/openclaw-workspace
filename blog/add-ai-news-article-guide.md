# How to Add Articles to AI News Sub-Page

**URL:** https://gameworld.zeabur.app/magazine/ai-news/

## Folder Structure

```
magazine/ai-news/
├── index.html                              # Main listing page (add your card here)
├── 2026-03-24/
│   └── business-insider-alex-karp-...html # One article = one HTML file
├── 2026-03-06/
│   └── bloomberg-ai-china-welfare.html
└── 2026-02-26/
    └── bloomberg-productivity-panic.html
```

## Step 1: Create Article HTML

Create a new file at:
```
magazine/ai-news/YYYY-MM-DD/your-article-slug.html
```

Copy an existing article as template (e.g., `2026-03-24/business-insider-alex-karp-ai-neurodivergent.html`).

Key elements needed:
- `header` with gradient background (ai-blue → ai-purple)
- Article metadata (source, date, person)
- Original + Archive.ph links
- Summary content with quotes and key points

## Step 2: Add Card to index.html

Edit `magazine/ai-news/index.html`, find the `news-grid` section and add BEFORE the closing `</div>`:

```html
<a href="YYYY-MM-DD/your-article-slug.html" class="news-card">
    <div class="news-date">📅 YYYY 年 MM 月 DD 日</div>
    <div class="news-source">📰 Source Name</div>
    <h3 class="news-title">Your Article Title</h3>
    <p class="news-summary">Brief summary in Chinese (1-2 sentences).</p>
</a>
```

## Step 3: Push to GitHub

```bash
git add magazine/ai-news/
git commit -m "feat: Add AI news article - Article Title"
git push
```

Zeabur auto-deploys from GitHub main branch.
