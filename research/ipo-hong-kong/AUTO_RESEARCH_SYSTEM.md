# 🤖 AutoResearch IPO 自動追蹤系統

**版本：** 1.0  
**創建日期：** 2026-03-22  
**作者：** OpenClaw IPO Research Team

---

## 🎯 系統概述

本系統使用 AutoResearch 框架，自動執行三個核心任務：

1. **自動監控 IPO 招股數據** - 實時追蹤所有正在招股嘅 IPO
2. **自動預測 IPO 表現** - 基於數據分析預測首日升幅
3. **自動追蹤已上市 IPO 股價** - 監控上市後表現

---

## 📋 AutoResearch 任務配置

### 任務 1：自動監控 IPO 招股數據

```yaml
/auto-research 
  goal: "建立實時 IPO 追蹤系統，自動監控所有正在招股嘅 IPO"
  metric: "數據更新延遲 <30 分鐘，準確率 >95%，覆蓋率 100%"
  maxIterations: 10
  schedule: "每 30 分鐘自動執行"
  dataSources:
    - Tavily API (新聞/公告)
    - HKEX 披露易
    - 阿斯達克 IPO 頻道
    - 富途 IPO 中心
  outputFiles:
    - research/ipo-hong-kong/tracking/ongoing-ipos.md
    - research/ipo-hong-kong/data/ongoing-ipos.json
  alerts:
    - 新 IPO 開始招股
    - 招股截止 (<24 小時)
    - 超額認購倍數異常 (>500 倍)
```

**檢查項目：**
- [ ] 正在招股 IPO 列表
- [ ] 招股價範圍
- [ ] 每手股數/入場費
- [ ] 截止日/上市日
- [ ] 超額認購倍數
- [ ] 孖展認購額
- [ ] 保荐人/基石投資者
- [ ] 行業分類

---

### 任務 2：自動預測 IPO 表現

```yaml
/auto-research 
  goal: "預測邊 5 隻 IPO 會有最高首日升幅"
  metric: "預測準確率 >60%, 覆蓋所有熱門 IPO"
  maxIterations: 20
  schedule: "每日 08:00 HKT 自動執行"
  factors:
    - 超額認購倍數 (權重 30%)
    - 行業熱門度 (權重 25%)
    - 保荐人聲譽 (權重 15%)
    - 基石投資者 (權重 15%)
    - 招股價估值 (權重 10%)
    - 市場情緒 (權重 5%)
  outputFiles:
    - research/ipo-hong-kong/analysis/ipo-prediction.md
    - research/ipo-hong-kong/data/prediction-model.json
  historicalData:
    - 2025 年 IPO 表現數據庫
    - 2026 年 IPO 表現數據庫
```

**預測模型：**
```python
predicted_gain = (
    subscription_multiple * 0.30 +
    industry_hotness * 0.25 +
    sponsor_reputation * 0.15 +
    cornerstone_investors * 0.15 +
    valuation_score * 0.10 +
    market_sentiment * 0.05
)
```

---

### 任務 3：自動追蹤已上市 IPO 股價

```yaml
/auto-research 
  goal: "監控所有 2026 年上市 IPO 嘅股價表現"
  metric: "數據更新延遲 <5 分鐘，準確率 >99%"
  maxIterations: 5
  schedule: "交易日每 5 分鐘自動執行"
  dataSources:
    - Yahoo Finance API
    - 阿斯達克實時報價
    - 富途牛牛 API
  outputFiles:
    - research/ipo-hong-kong/tracking/listed-ipo-performance.md
    - research/ipo-hong-kong/data/ipo-stock-prices.json
  alerts:
    - 首日升幅 >50% (熱門提醒)
    - 跌幅 >20% (止蝕提醒)
    - 成交量異常 (>平均 3 倍)
    - 突破 52 週高/低
```

**追蹤指標：**
- 首日升幅
- 累計升幅
- 成交量變化
- 市值變化
- 52 週高/低
- 相對恒指表現

---

## 📁 文件結構

```
research/ipo-hong-kong/
├── tracking/
│   ├── ongoing-ipos.md (正在招股)
│   ├── listed-ipo-performance.md (已上市表現)
│   └── current-ipo-offerings.md (可認購清單)
├── analysis/
│   ├── ipo-prediction.md (預測報告)
│   ├── preliminary-analysis.md (初步分析)
│   └── best-performing-ipos-2026.md (最佳表現)
├── data/
│   ├── ongoing-ipos.json (招股數據)
│   ├── ipo-stock-prices.json (股價數據)
│   ├── prediction-model.json (預測模型)
│   ├── ipo-margin-data.json (孖展數據)
│   └── best-performing-ipos-2026.json (歷史數據)
└── README.md (項目說明)
```

---

## ⚙️ 自動化設置

### Heartbeat 集成 (每 30 分鐘)

```markdown
## IPO 自動追蹤 (Heartbeat 任務)

**頻率：** 每 30 分鐘  
**腳本：** `skills/ipo-tracker/auto-track.py`

**檢查項目：**
1. 讀取 HEARTBEAT.md IPO 清單
2. 運行 `auto-track.py` 更新數據
3. 檢測到新 IPO → 發送 Discord 通知
4. 檢測到截止 (<24h) → 發送緊急提醒
5. 更新 `memory/ipo-tracker-state.json`

**通知規則：**
- 🔴 新 IPO 開始招股
- 🟠 招股截止 (<24 小時)
- 🟡 超額認購 >500 倍
- 🟢 常規更新 (每 30 分鐘)
```

### Cron 任務設置

```bash
# 每 30 分鐘更新 IPO 招股數據
*/30 * * * * cd /workspace && python3 skills/ipo-tracker/auto-track.py

# 每日 08:00 生成預測報告
0 8 * * * cd /workspace && python3 skills/ipo-tracker/predict-ipo.py

# 交易日每 5 分鐘更新股價 (9:30-16:00 HKT)
*/5 1-8 * * 1-5 cd /workspace && python3 skills/ipo-tracker/track-prices.py
```

---

## 🔔 Discord 通知格式

### 新 IPO 開始招股

```
🚨 **新 IPO 開始招股！**

**公司：** [公司名稱] ([代碼])
**行業：** [行業]
**招股價：** $[範圍]
**入場費：** ~$[金額]
**截止日：** [日期]
**上市日：** [日期]
**保荐人：** [保荐人]

**推薦度：** ⭐⭐⭐⭐⭐

[📄 詳細資料](連結)
```

### 招股截止提醒

```
⏰ **IPO 截止提醒 (<24 小時)**

**公司：** [公司名稱] ([代碼])
**截止時間：** [日期] [時間]
**剩餘時間：** [X] 小時

**當前超購：** [X] 倍
**孖展額：** $[X] 億

**立即認購：** [券商連結]
```

### 預測報告

```
📊 **IPO 表現預測 (今日)**

**預測升幅最高 5 隻：**

1. [公司] - 預測 +[X]% ⭐⭐⭐⭐⭐
2. [公司] - 預測 +[X]% ⭐⭐⭐⭐
3. [公司] - 預測 +[X]% ⭐⭐⭐⭐
4. [公司] - 預測 +[X]% ⭐⭐⭐
5. [公司] - 預測 +[X]% ⭐⭐⭐

**模型準確率：** [X]% (過去 30 日)

[📄 完整報告](連結)
```

### 股價異常提醒

```
📈 **IPO 股價異常！**

**公司：** [公司名稱] ([代碼])
**現價：** $[X] ([+X]%)
**成交量：** [X] 萬股 (平均 [X] 倍)
**市值：** $[X] 億

**原因：** [超額認購/行業利好/等等]

[📊 查看圖表](連結)
```

---

## 📊 狀態追蹤

### `memory/ipo-tracker-state.json`

```json
{
  "lastUpdate": "2026-03-22T12:30:00+08:00",
  "nextUpdate": "2026-03-22T13:00:00+08:00",
  "ongoingIpos": 7,
  "listedIpos": 30,
  "lastPrediction": "2026-03-22T08:00:00+08:00",
  "predictionAccuracy": 65.3,
  "alertsSent": {
    "newIpo": 3,
    "deadline": 5,
    "priceAlert": 12
  }
}
```

---

## 🧪 測試計劃

### 測試案例

| 測試 # | 目標 | 預期結果 | 狀態 |
|--------|------|---------|------|
| 1 | 檢測新 IPO | 自動發現並通知 | ⏳ 待測試 |
| 2 | 超額認購警報 | >500 倍時發送通知 | ⏳ 待測試 |
| 3 | 預測準確性 | >60% 準確率 | ⏳ 待測試 |
| 4 | 股價更新延遲 | <5 分鐘 | ⏳ 待測試 |
| 5 | 截止提醒 | <24 小時發送 | ⏳ 待測試 |

---

## 📈 性能指標

| 指標 | 目標 | 當前 | 狀態 |
|------|------|------|------|
| 數據更新延遲 | <30 分鐘 | - | ⏳ 待測量 |
| 預測準確率 | >60% | - | ⏳ 待測量 |
| 股價更新延遲 | <5 分鐘 | - | ⏳ 待測量 |
| 通知送達率 | >95% | - | ⏳ 待測量 |
| 系統可用性 | >99% | - | ⏳ 待測量 |

---

## 🔗 有用連結

| 資源 | 連結 |
|------|------|
| **HKEX 披露易** | https://www.hkexnews.hk |
| **阿斯達克 IPO** | https://www.aastocks.com |
| **富途 IPO** | https://www.futunn.com |
| **Tavily API** | https://api.tavily.com |
| **GitHub Repo** | https://github.com/raycoderhk/openclaw-workspace |

---

## 📞 查詢與支持

**Discord:** #ipo-tracking  
**Email:** ipo-tracker@openclaw.local  
**GitHub Issues:** https://github.com/raycoderhk/openclaw-workspace/issues

---

*最後更新：2026-03-22 12:30 HKT*  
*版本：1.0*

**⚠️ 免責聲明：** 本系統僅供參考，不構成投資建議。IPO 投資有風險，入市需謹慎。
