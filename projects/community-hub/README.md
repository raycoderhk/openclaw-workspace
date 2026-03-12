# 🏘️ 愉城社區 Hub - WhatsApp Chat Extractor

Extract useful community knowledge from WhatsApp group chat exports and build a searchable knowledge base.

## 📊 Current Stats

- **Source**: 愉景新城街坊組 WhatsApp export
- **Date Range**: May 2023 → March 2026 (~3 years)
- **Total Messages**: 202,729 lines
- **Parsed Messages**: 13,659 useful messages
- **Unique Senders**: 417 neighbors
- **Noise Filtered**: ~33% (stickers, images, system messages)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Set Environment Variables

```bash
# For classification (OpenRouter API - supports DeepSeek)
export OPENROUTER_API_KEY=your_key_here

# For database import (Supabase)
export SUPABASE_URL=https://your-project.supabase.co
export SUPABASE_ANON_KEY=your_anon_key
```

### 3. Run the Pipeline

```bash
# Step 1: Parse WhatsApp export
npm run parse

# Step 2: Classify messages with AI (cost: ~$0.30 for full dataset)
npm run classify

# Step 3: Import to Supabase
npm run import

# Or run everything at once
npm run full
```

## 📁 Output Files

| File | Description |
|------|-------------|
| `output/parsed_messages.json` | All parsed messages (13,659) |
| `output/parsed_messages_senders.json` | List of unique senders (417) |
| `output/classified_messages.json` | All messages with AI classification |
| `output/classified_messages_useful.json` | Only useful tips (~4,000 expected) |

## 🏷️ Categories

Messages are classified into these categories:

| Category | Description | Examples |
|----------|-------------|----------|
| `traffic` | Traffic & Transport | 青馬大橋 accidents, bus routes, MTR tips |
| `restaurant` | Restaurants & Food | OpenRice links, restaurant recommendations |
| `doctor` | Doctors & Medical | Clinic recommendations, health tips |
| `tech_tip` | Tech Tips | Phone plans, apps, gadget comparisons |
| `shopping` | Shopping & Deals | Promo codes, where to buy things |
| `service` | Services | Delivery, logistics, rentals |
| `community` | Community & Estate | Management office, facilities |
| `event` | Events & Activities | BBQ, gatherings, sports |
| `news` | News & Articles | Local news, school info |
| `repair` | Home Repairs | Plumbers, electricians, AC repair |
| `education` | Education | Tutors, courses, materials |
| `childcare` | Childcare & Kids | Toys, schools, parenting tips |

## 🗄️ Database Schema

See `supabase-schema.sql` for the full schema. Key features:

- Full-text search across all messages
- Category-based filtering
- Date range queries
- Entity extraction (businesses, people, places)
- Automatic statistics views

## 📡 API Endpoints (Future)

Once deployed, you can query via:

```bash
# Get latest restaurant tips
GET /api/tips/restaurant

# Search for "pizza"
GET /api/search?q=pizza

# Get tips by category with pagination
GET /api/tips?category=shopping&page=1&size=20

# Get recent tips (last 7 days)
GET /api/tips/recent
```

## 🤖 Telegram Bot Commands (Future)

```
/tips restaurant     - Latest restaurant recommendations
/tips traffic        - Recent traffic alerts
/tips doctor         - Doctor recommendations
/tips repair         - Home repair contacts
/tips search pizza   - Search for "pizza"
/tips today          - All tips from today
```

## 💰 Cost Estimate

Using DeepSeek via OpenRouter:

- **Dataset**: 13,659 messages
- **Batch size**: 25 messages/batch
- **Total batches**: ~547
- **Cost per batch**: ~$0.0005
- **Total cost**: ~$0.27 USD

## 📝 Sample Output

```json
{
  "date": "2026-03-12",
  "time": "08:44:48",
  "sender": "~ Angus Ma",
  "text": "青馬橋入東涌方向，嚴重交通事故，中線快線九架私家車連環相撞。現場嚴重交通癱瘓。",
  "category": "traffic",
  "useful": true,
  "summary": "Severe accident on Tsing Ma Bridge towards Tung Chung, 9-car pileup, major traffic disruption",
  "entities": ["青馬橋", "東涌"],
  "language": "zh"
}
```

## 🔧 Development

### Project Structure

```
community-hub/
├── raw/                    # Raw chat exports
│   └── _chat.txt
├── output/                 # Processed data
│   ├── parsed_messages.json
│   └── classified_messages.json
├── src/
│   ├── parser.js          # WhatsApp format parser
│   ├── classifier.js      # AI classification
│   └── import-to-supabase.js
├── supabase-schema.sql    # Database schema
└── package.json
```

### Add New Categories

Edit `src/classifier.js` and add to the `CATEGORIES` object:

```javascript
const CATEGORIES = {
  // ... existing categories
  new_category: 'Description of what belongs here',
};
```

## 📄 License

MIT - Built for 愉城社區 neighbors

## 🙏 Credits

- Data: 愉景新城街坊組 WhatsApp group members
- Classification: DeepSeek via OpenRouter
- Database: Supabase
- Inspiration: Existing 愉城社區 repairs.html MVP
