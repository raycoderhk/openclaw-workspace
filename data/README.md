# Consumer Council Price Data

This directory contains daily price data fetched from the Consumer Council Online Price Watch.

## Data Source

- **Provider:** Consumer Council (消費者委員會)
- **URL:** https://online-price-watch.consumer.org.hk/opw/opendata/pricewatch.json
- **Update Frequency:** Daily at 6 AM HKT
- **Fetch Method:** GitHub Actions (automated)

## Files

| File | Description |
|------|-------------|
| `pricewatch.json` | Latest price data (auto-updated daily) |
| `pricewatch-YYYYMMDD.json` | Historical backups |

## Raw Data URL

For programmatic access:

```
https://raw.githubusercontent.com/raycoderhk/2048-game/main/data/pricewatch.json
```

## Usage

### OpenClaw Skill Configuration

```javascript
DATA_URL: 'https://raw.githubusercontent.com/raycoderhk/2048-game/main/data/pricewatch.json'
```

### Manual Download

```bash
curl -O https://raw.githubusercontent.com/raycoderhk/2048-game/main/data/pricewatch.json
```

## Automated Updates

Data is automatically fetched daily via GitHub Actions:

- **Workflow:** `.github/workflows/fetch-prices-daily.yml`
- **Schedule:** 6 AM HKT daily
- **Manual Trigger:** Go to Actions tab → "Daily Price Data Fetch" → "Run workflow"

## Data Structure

The JSON contains price information for products across multiple supermarkets in Hong Kong.

## Attribution

Data Source: Consumer Council Online Price Watch  
URL: https://online-price-watch.consumer.org.hk/

---

**Last Updated:** Auto-updated daily  
**Maintained By:** GitHub Actions Bot
