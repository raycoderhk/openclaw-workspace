# 🎾 Reclub App Pickleball 自動追蹤可行性研究

**研究日期：** 2026-03-22  
**研究目標：** 自動追蹤荃灣區 Pickleball Activity  
**狀態：** 🟡 研究中

---

## 📱 Reclub App 概述

### 基本信息

| 項目 | 詳情 |
|------|------|
| **名稱** | Reclub |
| **平台** | iOS / Android |
| **網站** | https://reclub.co |
| **Pickleball 專區** | https://pickleball.reclub.co |
| **功能** | 俱樂部管理、活動組織、比賽追蹤、DUPR 集成 |

### 主要功能

1. **Clubs (俱樂部管理)**
   - 球員管理
   - 活動組織
   - RSVP + 候選名單

2. **Competitions (比賽)**
   - 報名、種子、抽籤
   - 比賽追蹤
   - DUPR 分數集成

3. **Meets (活動)**
   - 即時設置活動詳情
   - 隊伍分配
   - RSVP 管理

4. **Community (社區)**
   - 連接球員
   - 分享時刻
   - 慶祝勝利

---

## 🔍 荃灣區 Pickleball 場地 (Reclub)

### 已知場地

| 場地 | 地區 | 類型 | 預約方式 |
|------|------|------|---------|
| **Pickledise (荃灣)** | 荃灣 | 室內 | Reclub App |
| **Pulley (荃灣)** | 荃灣 | 室內 | Reclub App |
| **愉景新城會所** | 荃灣 | 室內 | 私人會所 |
| **WestK** | 西九 | 室外 | Reclub App |
| **Pick and Match** | 待定 | 室內 | Reclub App |

---

## 🔧 自動化方案分析

### 方案 1: Reclub API (官方)

**可行性：** ⚠️ **待確認**

**優點：**
- ✅ 官方支持
- ✅ 穩定可靠
- ✅ 合規合法

**缺點：**
- ⚠️ API 文檔唔清楚 (需要申請)
- ⚠️ 可能需要 API Key
- ⚠️ 可能有 rate limit

**實施步驟：**
```
1. 聯絡 Reclub 團隊查詢 API 訪問
2. 申請 API Key (如有)
3. 讀取 API 文檔
4. 開發集成腳本
5. 測試 + 部署
```

**API 端點推測：**
```
GET /api/v1/clubs/{club_id}/events
GET /api/v1/locations/{location_id}/bookings
GET /api/v1/users/{user_id}/rsvps
```

**認證方式：**
```
Authorization: apikey YOUR_API_KEY
```

---

### 方案 2: Web Scraping (網頁爬蟲)

**可行性：** 🟡 **中等**

**優點：**
- ✅ 唔需要 API Key
- ✅ 可以快速實施

**缺點：**
- ⚠️ 可能違反 ToS
- ⚠️ 網站結構改變會失效
- ⚠️ 可能需要處理登入

**實施步驟：**
```
1. 分析 Reclub 網站結構
2. 使用 Playwright/Selenium 模擬瀏覽器
3. 登入 (需要用戶賬號)
4. 爬取活動數據
5. 解析 + 保存
```

**技術棧：**
```python
# 使用 Playwright
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://reclub.co')
    # 登入 + 爬取數據
```

---

### 方案 3: Mobile App Automation (手機自動化)

**可行性：** 🟡 **中等**

**優點：**
- ✅ 同普通用戶體驗一樣
- ✅ 可以獲取 App 獨有數據

**缺點：**
- ⚠️ 需要運行 Android/iOS 模擬器
- ⚠️ 複雜度高
- ⚠️ 可能違反 App ToS

**實施步驟：**
```
1. 設置 Android 模擬器 (如 Genymotion)
2. 安裝 Reclub App
3. 使用 Appium 自動化操作
4. 截取屏幕 + OCR 解析
5. 或直接訪問 App API
```

**技術棧：**
```python
# 使用 Appium
from appium import webdriver

caps = {
    'platformName': 'Android',
    'appPackage': 'co.reclub.app',
    'appActivity': '.MainActivity'
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', caps)
```

---

### 方案 4: Browser Extension Relay (瀏覽器擴展中繼)

**可行性：** 🟢 **高 (推薦)**

**優點：**
- ✅ 使用真實用戶會話
- ✅ 唔需要破解 API
- ✅ 可以集成到 OpenClaw
- ✅ 符合 OpenClaw 架構

**缺點：**
- ⚠️ 需要用戶登入
- ⚠️ 需要保持瀏覽器會話

**實施步驟：**
```
1. 安裝 OpenClaw Browser Relay (Chrome Extension)
2. 登入 Reclub (https://reclub.co)
3. 創建自動化腳本 (Python + Playwright)
4. 使用 Chrome Extension Relay 執行
5. 定期檢查 + 通知
```

**技術棧：**
```python
# 使用 Playwright + OpenClaw Browser Relay
from playwright.sync_api import sync_playwright

def check_reclub_activities():
    with sync_playwright() as p:
        # 使用現有 Chrome 會話
        browser = p.chromium.connect_over_cdp('http://localhost:9222')
        page = browser.contexts[0].pages[0]
        
        # 導航到 Reclub
        page.goto('https://reclub.co/pickleball/hong-kong/tsuen-wan')
        
        # 提取活動數據
        activities = page.query_selector_all('.activity-card')
        
        results = []
        for activity in activities:
            results.append({
                'title': activity.query_selector('.title').inner_text(),
                'date': activity.query_selector('.date').inner_text(),
                'location': activity.query_selector('.location').inner_text(),
                'spots': activity.query_selector('.spots').inner_text()
            })
        
        return results
```

---

## 🎯 推薦方案：Browser Extension Relay + AutoResearch

### 架構設計

```
┌─────────────────────────────────────────────────────────┐
│                    OpenClaw Gateway                      │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              Chrome Extension Relay                      │
│              (用戶已登入 Reclub)                         │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│            AutoResearch Pickleball Tracker               │
│  - 每 30 分鐘檢查一次                                     │
│  - 過濾荃灣區活動                                         │
│  - 檢測新活動                                             │
│  - 發送 Discord 通知                                       │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                 Discord #pickleball                      │
│                 (通知渠道)                               │
└─────────────────────────────────────────────────────────┘
```

---

### 實施細節

#### 1. 數據模型

```python
class PickleballActivity:
    def __init__(self):
        self.id: str           # 活動 ID
        self.title: str        # 活動標題
        self.date: datetime    # 活動日期時間
        self.location: str     # 場地名稱
        self.district: str     # 地區 (荃灣/西九/等等)
        self.spots_total: int  # 總名額
        self.spots_available: int  # 剩餘名額
        self.price: float      # 價格
        self.level: str        # 級別 (初學/中級/高級)
        self.organizer: str    # 組織者
        self.rsvp_url: str     # 報名連結
        self.created_at: datetime  # 創建時間
```

#### 2. 檢查邏輯

```python
def check_tsuen_wan_activities():
    """檢查荃灣區 Pickleball 活動"""
    
    # 定義荃灣區場地關鍵字
    tsuen_wan_keywords = [
        '荃灣', 'Tsuen Wan', 'Pickledise', 'Pulley',
        '愉景新城', 'D park', '荃新天地'
    ]
    
    # 獲取所有活動
    all_activities = fetch_reclub_activities()
    
    # 過濾荃灣區
    tsuen_wan_activities = [
        act for act in all_activities
        if any(keyword in act.location for keyword in tsuen_wan_keywords)
    ]
    
    return tsuen_wan_activities
```

#### 3. 通知規則

| 事件 | 觸發條件 | 通知優先級 |
|------|---------|-----------|
| **新活動發布** | 檢測到新活動 (<1 小時) | 🔴 高 |
| **名額緊張** | 剩餘名額 <5 | 🟠 中 |
| **即將截止** | 活動前 <24 小時 | 🟡 低 |
| **常規更新** | 每 30 分鐘檢查 | 🟢 僅記錄 |

#### 4. 通知格式

```
🎾 **新 Pickleball 活動！**

**活動：** [活動名稱]
**日期：** [日期時間]
**地點：** [場地名稱] (荃灣)
**名額：** [剩餘]/[總數]
**價格：** $[價格]
**級別：** [初學/中級/高級]

**組織者：** [組織者名稱]

[📝 立即報名](連結)

---
**檢測時間：** [時間]
**剩餘名額：** [X] 個 (緊張！)
```

---

### 狀態追蹤

#### `memory/pickleball-tracker-state.json`

```json
{
  "lastCheck": "2026-03-22T12:30:00+08:00",
  "nextCheck": "2026-03-22T13:00:00+08:00",
  "trackedActivities": [
    {
      "id": "act_123",
      "title": "荃灣 Pickledise 晚間場",
      "date": "2026-03-25T19:00:00+08:00",
      "location": "Pickledise (荃灣)",
      "spotsAvailable": 3,
      "notified": true
    }
  ],
  "alertsSent": {
    "newActivity": 5,
    "spotsLow": 12,
    "deadlineReminder": 3
  },
  "favoriteLocations": [
    "Pickledise (荃灣)",
    "Pulley (荃灣)",
    "愉景新城會所"
  ]
}
```

---

## 📋 實施清單

### 第一階段：研究 (完成)

- [x] 搜尋 Reclub App 資訊
- [x] 分析自動化方案
- [x] 撰寫可行性報告
- [ ] 聯絡 Reclub 團隊查詢 API

### 第二階段：開發 (待定)

- [ ] 設置 Browser Extension Relay
- [ ] 開發爬蟲腳本
- [ ] 測試登入流程
- [ ] 實現活動過濾 (荃灣區)
- [ ] 實現通知系統

### 第三階段：部署 (待定)

- [ ] 設置 Heartbeat (每 30 分鐘)
- [ ] 配置 Discord 通知
- [ ] 測試完整流程
- [ ] 文檔化

### 第四階段：優化 (待定)

- [ ] 添加更多過濾條件 (時間/價格/級別)
- [ ] 添加報名自動化 (可選)
- [ ] 添加日曆同步 (Google Calendar)
- [ ] 添加統計分析 (活動頻率/價格趨勢)

---

## ⚠️ 風險與注意事項

### 技術風險

| 風險 | 可能性 | 影響 | 緩解措施 |
|------|--------|------|---------|
| API 變更 | 中 | 高 | 定期檢查 + 快速修復 |
| 登入失效 | 高 | 中 | 自動重試 + 通知用戶 |
| Rate Limit | 中 | 中 | 控制檢查頻率 |
| 網站結構改變 | 中 | 高 | 使用穩定選擇器 |

### 合規風險

| 風險 | 可能性 | 影響 | 緩解措施 |
|------|--------|------|---------|
| 違反 ToS | 中 | 高 | 使用官方 API (如有) |
| 賬號被封 | 低 | 高 | 控制請求頻率 |
| 數據隱私 | 中 | 中 | 只存必要數據 |

---

## 💡 替代方案

### 方案 A: 人手檢查 + Discord 提醒

**優點：**
- ✅ 簡單直接
- ✅ 唔需要開發

**缺點：**
- ❌ 需要人手操作
- ❌ 容易忘記

**實施：**
```
1. 用戶人手檢查 Reclub App
2. 發現荃灣區活動 → 發送 Discord 消息
3. 其他用戶可以響應
```

---

### 方案 B: Google Calendar + IFTTT

**優點：**
- ✅ 使用現有工具
- ✅ 可以設置提醒

**缺點：**
- ❌ Reclub 唔支持 IFTTT
- ❌ 需要人手添加活動

---

### 方案 C: WhatsApp/Telegram 群組

**優點：**
- ✅ 簡單
- ✅ 實時通知

**缺點：**
- ❌ 需要人手分享
- ❌ 信息容易淹沒

---

## 🎯 結論與建議

### 可行性評估

| 方案 | 可行性 | 推薦度 | 實施難度 |
|------|--------|--------|---------|
| **Browser Extension Relay** | 🟢 高 | ⭐⭐⭐⭐⭐ | 中等 |
| 官方 API | 🟡 待確認 | ⭐⭐⭐⭐ | 低 |
| Web Scraping | 🟡 中等 | ⭐⭐⭐ | 中等 |
| Mobile Automation | 🟡 中等 | ⭐⭐ | 高 |

### 推薦方案

**🏆 Browser Extension Relay + AutoResearch**

**理由：**
1. 符合 OpenClaw 架構
2. 使用真實用戶會話 (合規)
3. 可以集成現有系統 (Discord/Heartbeat)
4. 實施難度中等

### 下一步行動

1. **聯絡 Reclub 團隊**
   - 查詢是否有官方 API
   - 詢問自動化訪問政策

2. **設置測試環境**
   - 安裝 Chrome Extension Relay
   - 登入 Reclub
   - 測試基本爬取功能

3. **開發 MVP**
   - 實現基本檢查功能
   - 過濾荃灣區活動
   - 發送 Discord 通知

4. **測試 + 優化**
   - 測試穩定性
   - 優化檢查頻率
   - 添加更多功能

---

## 📞 聯絡 Reclub

**網站：** https://reclub.co  
**Email:** support@reclub.co (推測)  
**Discord:** (待查)  

**查詢內容：**
```
你好，

我係一個 OpenClaw 用戶，想開發一個自動化系統來追蹤
荃灣區嘅 Pickleball 活動。

想請問：
1. Reclub 有無提供官方 API？
2. 如果有，點樣申請 API Key？
3. 有無自動化訪問嘅限制或政策？

謝謝！
```

---

*最後更新：2026-03-22 12:35 HKT*  
*版本：1.0*  
*狀態：🟡 研究中*
