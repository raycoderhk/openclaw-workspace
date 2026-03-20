#!/usr/bin/env python3
"""
YouTube Monitor - OpenClaw Integration
Sends new video notifications to Discord via OpenClaw message tool
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
NEW_VIDEOS_FILE = MEMORY_DIR / "youtube-new-videos.json"
SENT_VIDEOS_FILE = MEMORY_DIR / "youtube-sent.json"

def load_json(path, default=None):
    if default is None:
        default = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def send_discord_message(message):
    """Send message to Discord via OpenClaw message tool"""
    # This would be called by OpenClaw's exec or cron system
    # For now, we output the message for OpenClaw to process
    print(f"DISCORD_MESSAGE:{message}")
    
def main():
    """Check for new videos and send notifications"""
    print(f"[{datetime.now().isoformat()}] Checking for new videos to notify...")
    
    # Load new videos from check_videos.py
    new_videos_data = load_json(NEW_VIDEOS_FILE)
    
    if not new_videos_data or 'videos' not in new_videos_data:
        print("No new videos to notify")
        return
    
    # Load sent videos (to avoid duplicates)
    sent_videos = load_json(SENT_VIDEOS_FILE, {'video_ids': []})
    sent_ids = set(sent_videos.get('video_ids', []))
    
    videos_to_notify = []
    
    for item in new_videos_data.get('videos', []):
        video = item.get('video', {})
        video_id = video.get('video_id')
        
        # Skip if already sent
        if video_id in sent_ids:
            continue
        
        videos_to_notify.append(item)
        sent_ids.add(video_id)
    
    if not videos_to_notify:
        print("All videos already notified")
        return
    
    # Send notifications
    print(f"Sending {len(videos_to_notify)} notification(s)...")
    
    for item in videos_to_notify:
        video = item['video']
        channel_name = item['channel_name']
        
        # Format message
        published = video.get('published', '')
        try:
            dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
            hkt_time = dt.strftime('%Y-%m-%d %H:%M HKT')
        except:
            hkt_time = published
        
        description = video.get('description', '無描述')
        if len(description) > 500:
            description = description[:500] + "..."
        
        message = f"""## 🎬 新片通知！

**頻道:** {channel_name}
**標題:** {video['title']}
**發布:** {hkt_time}

**簡介:**
{description}

[📺 觀看視頻]({video['url']})

---
*YouTube Monitor - OpenClaw*"""
        
        # Output for OpenClaw to capture
        print(f"\n=== DISCORD_NOTIFICATION ===")
        print(message)
        print(f"=== END_NOTIFICATION ===\n")
    
    # Save sent video IDs
    save_json(SENT_VIDEOS_FILE, {
        'lastUpdate': datetime.now(timezone.utc).isoformat(),
        'video_ids': list(sent_ids)
    })
    
    # Clear processed videos
    save_json(NEW_VIDEOS_FILE, {'processed': True})
    
    print(f"✅ Sent {len(videos_to_notify)} notification(s)")

if __name__ == '__main__':
    main()
