# YouTube Monitor - 快速設置指南

## ✅ 已完成

- [x] 創建 YouTube Monitor Skill
- [x] 安裝依賴 (feedparser, requests)
- [x] 測試成功 (檢測到 30 條新片！)
- [x] 創建 Discord 通知腳本

## 📝 下一步：自定義頻道

### 1. 編輯 config.json

```bash
cd /home/node/.openclaw/workspace/skills/youtube-monitor
nano config.json
```

### 2. 添加你想監控的頻道

**獲取 Channel ID 方法：**

**方法 A：頻道頁面**
```
1. 去 YouTube 頻道頁面
2. 睇 URL: https://www.youtube.com/channel/UCxxxxx
3. 複製 UCxxxxx 呢個 ID
```

**方法 B：Handle 轉換**
```
1. 去：https://commentpicker.com/youtube-channel-id.php
2. 輸入頻道 Handle (例如 @MrBeast)
3. 獲取 Channel ID
```

**方法 C：View Source**
```
1. 去頻道頁面
2. Ctrl+U (View Source)
3. 搜尋 "channelId"
4. 複製 ID
```

### 3. 添加到 config.json

```json
{
  "channels": [
    {
      "id": "UCXuqSBlHAE6Xw-yeJA0Tunw",
      "name": "Linus Tech Tips",
      "enabled": true
    },
    {
      "id": "UCBJycsmduvYEL83R_U4JriQ",
      "name": "Marques Brownlee",
      "enabled": true
    },
    {
      "id": "你想加嘅頻道 ID",
      "name": "頻道名稱",
      "enabled": true
    }
  ]
}
```

### 4. 手動測試

```bash
cd /home/node/.openclaw/workspace/skills/youtube-monitor
python3 check_videos.py
```

### 5. 設置自動檢查 (Heartbeat)

編輯 `HEARTBEAT.md`，添加：

```markdown
### YouTube Monitor (每次 Heartbeat 檢查)
**頻率:** 每 30 分鐘
**位置:** `skills/youtube-monitor/check_videos.py`
**通知:** Discord #youtube-updates 頻道

檢查步驟:
1. 運行 `python3 check_videos.py`
2. 如果有新片 → 發送 Discord 通知
3. 記錄到 `memory/youtube-state.json`
```

---

## 🎯 功能列表

| 功能 | 狀態 | 說明 |
|------|------|------|
| RSS 監控 | ✅ | 無需 API Key |
| 多頻道支援 | ✅ | 可監控任意數量頻道 |
| 避免重複通知 | ✅ | 記錄已通知的視頻 |
| Discord 通知 | ✅ | 自動發送 |
| AI 總結 | 🔄 | 可選 (目前用描述) |
| Kanban 整合 | ⏳ | 可選 |

---

## 📊 文件結構

```
skills/youtube-monitor/
├── check_videos.py      # 主腳本 (檢查新片)
├── notify_discord.py    # Discord 通知
├── config.json          # 頻道配置
├── requirements.txt     # Python 依賴
└── README.md            # 文檔

memory/
├── youtube-state.json   # 檢查狀態
├── youtube-videos.json  # 已通知視頻列表
└── youtube-sent.json    # 已發送通知
```

---

## 🔧 常用命令

**手動檢查：**
```bash
cd skills/youtube-monitor
python3 check_videos.py
```

**查看狀態：**
```bash
cat memory/youtube-state.json
```

**重置記錄 (重新通知所有片)：**
```bash
rm memory/youtube-state.json memory/youtube-sent.json
```

**禁用某個頻道：**
```json
{
  "id": "UCxxxxx",
  "name": "頻道名稱",
  "enabled": false  // 改呢個
}
```

---

## 💡 提示

1. **第一次運行** 會檢測到所有現有視頻 (可能好多通知)
2. **之後** 只會通知新上傳的視頻
3. **如果想重置** 刪除 `memory/youtube-*.json` 文件
4. **檢查頻率** 預設 30 分鐘 (可修改 config.json)
5. **YouTube RSS** 通常延遲 5-15 分鐘 (正常現象)

---

## ❓ 常見問題

**Q: 點解檢測唔到某啲頻道？**
A: 確保 Channel ID 正確 (係 UC 開頭)

**Q: 點解通知咗舊片？**
A: 第一次運行會檢測所有片，之後就只會通知新片

**Q: 可以監控 Shorts 嗎？**
A: 可以！YouTube RSS 包含所有視頻類型

**Q: 可以加 AI 總結嗎？**
A: 可以！修改 `summarize_video()` 函數調用 OpenClaw AI

---

**完成！** 🎉 而家你有一個全自動 YouTube 監控系統！
