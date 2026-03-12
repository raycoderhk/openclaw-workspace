# 🏘️ 愉城社區 Hub - Project Summary

**Created**: March 12, 2026  
**Status**: ✅ Phase 1 Complete (Parser Ready)  
**Next**: AI Classification → Database → Website

---

## 📊 What We Have

### Raw Data
- **Source**: 愉景新城街坊組 WhatsApp export (March 12, 2026)
- **File Size**: 14.1 MB
- **Total Lines**: 202,729
- **Date Range**: May 25, 2023 → March 12, 2026 (~3 years!)
- **Unique Senders**: 417 neighbors (including you, Raymond!)

### Parsed Data
- **Useful Messages**: 13,659
- **Noise Filtered**: ~33% (stickers, images, system messages, deleted messages)
- **Format**: Standard WhatsApp `[DD/M/YYYY, HH:MM:SS] Sender: Message`

### Your Presence
Found in chat export:
- `Raymond`
- `~ Raymond LM Chan`
- `~ Raymond Tam`

---

## 🎯 What We Built

### 1. Parser (`src/parser.js`) ✅
- Parses standard WhatsApp export format
- Filters noise (stickers, images, deleted messages)
- Extracts structured data: date, time, sender, text
- Outputs: `parsed_messages.json` + `parsed_messages_senders.json`

### 2. AI Classifier (`src/classifier.js`) 🔄
- Uses DeepSeek AI (via OpenRouter) for batch classification
- 12 categories: traffic, restaurant, doctor, tech_tip, shopping, service, community, event, news, repair, education, childcare
- Extracts entities (businesses, people, places)
- Summarizes in English
- **Estimated cost**: ~$0.27 USD for full dataset

### 3. Database Schema (`supabase-schema.sql`) 📋
- Supabase (PostgreSQL) with full-text search
- Indexes for fast queries by category, date, entities
- Views: `latest_tips_by_category`, `recent_tips`, `tips_stats`
- Functions: `search_tips()`, `get_tips_by_category()`
- Row Level Security ready for multi-user

### 4. Import Script (`src/import-to-supabase.js`) 📥
- Batch imports to Supabase (100 records/batch)
- Progress tracking and error handling
- Verification and statistics

---

## 🏷️ Classification Categories

| Category | What It Captures | Example |
|----------|-----------------|---------|
| `traffic` | Accidents, transport tips, MTR/bus info | 青馬大橋 10 車相撞 |
| `restaurant` | Food recommendations, OpenRice links | 邊間餐廳好食 |
| `doctor` | Medical recommendations, clinics | 邊個醫生好 |
| `tech_tip` | Phone plans, apps, gadgets | 4.5G vs 5G, CSL plan |
| `shopping` | Deals, promo codes, where to buy | HKTV Mall 8424 code |
| `service` | Delivery, logistics, rentals | Deliveroo, SF Express |
| `community` | Estate management, facilities | 管理處聯絡 |
| `event` | Gatherings, activities, sports | BBQ, Pickleball |
| `news` | Local news, school info | 學校關閉通知 |
| `repair` | **Home repairs** (plumbers, AC, electricians) | 水喉師傅聯絡 |
| `education` | Tutors, courses, materials | 補習老師 |
| `childcare` | Kids activities, toys, parenting | 兒童玩具，學校 |

---

## 📁 File Structure

```
projects/community-hub/
├── raw/
│   └── _chat.txt              # 14.1 MB WhatsApp export
├── output/
│   ├── parsed_messages.json   # 13,659 parsed messages ✅
│   ├── parsed_messages_senders.json  # 417 unique senders ✅
│   ├── demo_classified.json   # (after demo run)
│   └── classified_messages.json  # (after full classification)
├── src/
│   ├── parser.js              # ✅ Complete
│   ├── classifier.js          # 🔄 Ready to run
│   ├── import-to-supabase.js  # 📋 Ready to run
│   └── demo-classify.js       # 🎬 Demo script
├── supabase-schema.sql        # 📋 Database schema
├── package.json
├── .env.example
└── README.md
```

---

## 🚀 Next Steps

### Phase 1: ✅ Complete (Parser)
- [x] Extract and parse WhatsApp export
- [x] Filter noise messages
- [x] Identify unique senders
- [x] Create project structure

### Phase 2: 🔄 AI Classification (Ready to Run)
- [ ] Set OpenRouter API key
- [ ] Run demo classification (50 messages, ~$0.001)
- [ ] Review classification quality
- [ ] Run full classification (13,659 messages, ~$0.27)

### Phase 3: 📊 Database Setup
- [ ] Create Supabase project (or use existing)
- [ ] Run `supabase-schema.sql`
- [ ] Import classified data
- [ ] Test queries and search

### Phase 4: 🌐 Website
- [ ] Expand existing repairs.html
- [ ] Add category filters, search, date range
- [ ] Auto-update from Supabase
- [ ] Deploy to GitHub Pages or Zeabur

### Phase 5: 🤖 Telegram Bot
- [ ] Add `/tips` commands
- [ ] Query Supabase for latest tips
- [ ] Auto-post daily/weekly summaries

---

## 💰 Cost Breakdown

| Item | Cost |
|------|------|
| OpenRouter API (DeepSeek) | ~$0.27 USD |
| Supabase | Free tier (500MB database, plenty for this) |
| Hosting (GitHub Pages) | Free |
| Hosting (Zeabur) | Free tier available |
| **Total** | **~$0.27 USD** |

---

## 🎯 Demo: Run Classification Sample

To see what the AI classification looks like:

```bash
cd projects/community-hub
export OPENROUTER_API_KEY=your_key_here
node src/demo-classify.js
```

This will:
1. Select 50 diverse messages from the dataset
2. Classify them with DeepSeek AI
3. Show results by category
4. Display sample useful tips
5. Save to `output/demo_classified.json`

---

## 📈 Expected Output (Full Dataset)

Based on the sample analysis:

| Metric | Estimate |
|--------|----------|
| Total messages | 13,659 |
| Useful tips (~30%) | ~4,000 |
| Traffic alerts | ~400 |
| Restaurant tips | ~600 |
| Doctor recommendations | ~200 |
| Tech tips | ~150 |
| Shopping deals | ~300 |
| Repair contacts | ~250 |
| Events/activities | ~200 |
| Other categories | ~1,900 |

---

## 🔐 Privacy & Security

- **Data**: Local processing only (no external API except AI classification)
- **Supabase**: Row Level Security enabled
- **Public access**: Read-only for community tips
- **Personal info**: Sender names preserved (as in original chat)
- **Recommendation**: Don't share raw chat export publicly

---

## 🙏 Community Value

This transforms 3 years of casual chat into a **searchable knowledge base**:

- **New residents**: Instant access to trusted recommendations
- **Long-time residents**: Easy search instead of scrolling chat history
- **Emergency situations**: Quick access to repair contacts, doctors
- **Daily life**: Latest traffic alerts, restaurant deals, tech tips

**Evolution from repairs.html MVP**:
- `repairs.html` → Manual updates, repair contacts only
- `community-hub` → Auto-updating, all community knowledge

---

## 📞 Your Decision

**Ready to proceed with Phase 2 (AI Classification)?**

Options:
1. **Run demo first** (50 messages, ~$0.001) - See quality before committing
2. **Run full classification** (13,659 messages, ~$0.27) - Get everything at once
3. **Custom batch** (e.g., last 3 months only) - Focus on recent tips

Just let me know and I'll run it! 🚀
