#!/usr/bin/env python3
"""
YouTube Monitor - Discord Integration via Webhooks using curl
"""

import json
import os
import subprocess
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"
SKILL_DIR = WORKSPACE / "skills" / "youtube-monitor"
MEMORY_DIR = WORKSPACE / "memory"
CONFIG_FILE = SKILL_DIR / "config.json"
NEW_VIDEOS_FILE = MEMORY_DIR / "youtube-new-videos.json"

WEBHOOK_URL = "https://discord.com/api/webhooks/1488017483368501299/X2YLwe54qZFzURcWLpZ_MU_GB_JWMS5HP1hNqJmq7Q5xtBK_Xsb6A_rp98AjEe0s4GSi"

def load_json(path, default=None):
    if default is None:
        default = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return default

def send_webhook(message):
    """Send via Discord webhook using curl"""
    cmd = [
        'curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
        '-X', 'POST', WEBHOOK_URL,
        '-H', 'Content-Type: application/json',
        '-d', json.dumps({"content": message, "username": "YouTube Monitor"})
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def main():
    data = load_json(NEW_VIDEOS_FILE, [])
    videos = data.get('videos', [])
    
    if not videos:
        print("No new videos to notify")
        return
    
    print(f"Sending {len(videos)} notification(s)...")
    
    for video in videos:
        title = video.get('title', 'No title')
        url = video.get('url', '')
        channel = video.get('channel', '')
        published = video.get('published', '')
        
        msg = f"🆕 **{channel}**\n**{title}**\n{url}"
        if published:
            msg += f"\n⏱ {published}"
        
        status = send_webhook(msg)
        if status == '204':
            print(f"✅ Sent: {title[:50]}...")
        else:
            print(f"❌ HTTP {status}")
    
    print(f"Done!")

if __name__ == '__main__':
    main()
