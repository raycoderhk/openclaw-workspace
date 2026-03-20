# YouTube Monitor Skill

自動監控 YouTube 頻道，新片發布時自動通知 + AI 總結。

## 功能

- ✅ 監控任意 YouTube 頻道 (via RSS)
- ✅ 每 30 分鐘自動檢查
- ✅ 新片檢測 + 避免重複
- ✅ AI 總結視頻內容 (描述/字幕)
- ✅ Discord 通知
- ✅ 自動創建 Kanban Task

## 設置

### 1. 添加要監控的頻道

編輯 `config.json`，添加頻道 ID：

```json
{
  "channels": [
    {
      "id": "UCxxxxx",
      "name": "頻道名稱",
      "enabled": true
    }
  ]
}
```

### 2. 獲取 YouTube Channel ID

方法 1: 頻道頁面 URL
```
https://www.youtube.com/channel/UCxxxxx
                              ^^^^^^^^ 呢個就係 Channel ID
```

方法 2: 頻道 Handle 轉換
```
https://www.youtube.com/@MrBeast
→ 去頻道頁面 → View Source → 搜尋 "channelId"
```

方法 3: 用工具
```
https://commentpicker.com/youtube-channel-id.php
```

### 3. RSS Feed URL 格式

```
https://www.youtube.com/feeds/videos.xml?channel_id=UCxxxxx
```

## Cron 設置

OpenClaw 自動每 30 分鐘檢查一次。

手動測試：
```bash
cd skills/youtube-monitor
python3 check_videos.py
```

## 狀態追蹤

檢查記錄保存在：
- `memory/youtube-last-checked.json` - 最後檢查時間
- `memory/youtube-videos.json` - 已通知的視頻列表

## 通知格式

Discord 通知包含：
- 視頻標題
- 頻道名稱
- 發布時間
- AI 總結
- 視頻連結
- Kanban Task (可選)
