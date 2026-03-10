# 🛒 GitHub Actions Price Fetch - Setup Guide

## Problem

Consumer Council's CloudFront is blocking automated requests from:
- ❌ Node.js fetch
- ❌ curl from servers
- ❌ GitHub Actions (2048-game repo)

## Solution

Use **openclaw-knowledge** repo instead - it's the correct repo for this data!

---

## Setup Steps

### Step 1: Copy Workflow to openclaw-knowledge

```bash
# Clone the correct repo
git clone https://github.com/raycoderhk/openclaw-knowledge.git
cd openclaw-knowledge

# Create .github/workflows directory if needed
mkdir -p .github/workflows

# Copy workflow file from 2048-game
# Option A: Download directly
curl -o .github/workflows/fetch-prices-daily.yml \
  https://raw.githubusercontent.com/raycoderhk/2048-game/main/.github/workflows/fetch-prices-daily.yml

# Option B: Manual copy
# Download from: https://github.com/raycoderhk/2048-game/blob/main/.github/workflows/fetch-prices-daily.yml
# Save to: .github/workflows/fetch-prices-daily.yml

# Commit and push
git add .github/workflows/fetch-prices-daily.yml
git commit -m "🛒 Add daily price data fetch workflow"
git push origin main
```

---

### Step 2: Enable GitHub Actions

1. **Go to:** https://github.com/raycoderhk/openclaw-knowledge/actions
2. **Click:** "I understand my workflows, go ahead and enable them" (if prompted)
3. **You should see:** "Daily Price Data Fetch" workflow

---

### Step 3: Trigger First Manual Fetch

1. Click on **"Daily Price Data Fetch"** workflow
2. Click **"Run workflow"** button
3. Select branch: `main`
4. Click **"Run workflow"**
5. **Wait 1-2 minutes** for completion

---

### Step 4: Verify Success

**Check:**
- ✅ Green checkmark on workflow run
- ✅ File exists: https://github.com/raycoderhk/openclaw-knowledge/blob/main/data/pricewatch.json
- ✅ Raw URL works: https://raw.githubusercontent.com/raycoderhk/openclaw-knowledge/main/data/pricewatch.json

**If Failed:**
- ❌ Red X on workflow
- 📝 Check logs for error
- ⚠️ Consumer Council may be blocking GitHub IPs too

---

### Step 5: Update OpenClaw Config

Once data is in openclaw-knowledge:

```bash
cd /home/node/.openclaw/workspace/skills/supermarket-prices
```

Update `fetch-prices.js`:
```javascript
DATA_URL: 'https://raw.githubusercontent.com/raycoderhk/openclaw-knowledge/main/data/pricewatch.json'
```

Update `skill.json`:
```json
"dataEndpoint": "https://raw.githubusercontent.com/raycoderhk/openclaw-knowledge/main/data/pricewatch.json"
```

---

## Why openclaw-knowledge?

| Repo | Purpose | Suitable for Price Data? |
|------|---------|-------------------------|
| **2048-game** | Games | ❌ No |
| **openclaw-knowledge** | Knowledge/Data | ✅ Yes! |
| **mini-games** | Games | ❌ No |

**openclaw-knowledge** is the correct repo for:
- ✅ Reference data
- ✅ Knowledge bases
- ✅ Datasets
- ✅ Documentation

---

## Alternative: If GitHub Actions Also Blocked

If Consumer Council blocks GitHub IPs too:

### Option A: Manual Download
```bash
# Download manually once a week
curl -o data/pricewatch.json "https://online-price-watch.consumer.org.hk/opw/opendata/pricewatch.json"
git add data/pricewatch.json
git commit -m "Weekly price data update"
git push
```

### Option B: Contact Consumer Council
Email: cc@consumer.org.hk  
Request: Official API access for non-profit consumer education

### Option C: Community Contribution
Ask users to submit price data via form/PR

---

## Files

| File | Location |
|------|----------|
| Workflow | `.github/workflows/fetch-prices-daily.yml` |
| Data | `data/pricewatch.json` |
| Config | `skills/supermarket-prices/fetch-prices.js` |
| This Guide | `data/GITHUB-ACTIONS-SETUP.md` |

---

**Created:** 2026-03-10  
**Status:** Ready for setup in openclaw-knowledge repo
