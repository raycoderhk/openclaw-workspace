#!/usr/bin/env python3
"""
YouTube Monitor - Check for new videos from subscribed channels
Uses YouTube RSS feeds (no API key required)
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
import feedparser
import requests

# Paths
WORKSPACE = Path.home() / ".openclaw" / "workspace"
SKILL_DIR = WORKSPACE / "skills" / "youtube-monitor"
MEMORY_DIR = WORKSPACE / "memory"
CONFIG_FILE = SKILL_DIR / "config.json"
STATE_FILE = MEMORY_DIR / "youtube-state.json"
VIDEOS_FILE = MEMORY_DIR / "youtube-videos.json"

def load_json(path, default=None):
    """Load JSON file or return default"""
    if default is None:
        default = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json(path, data):
    """Save data to JSON file"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_channel_rss(channel_id):
    """Generate YouTube RSS feed URL"""
    return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

def fetch_videos(rss_url):
    """Fetch videos from YouTube RSS feed"""
    try:
        feed = feedparser.parse(rss_url)
        videos = []
        for entry in feed.entries:
            videos.append({
                'video_id': entry.get('yt_videoid', ''),
                'title': entry.get('title', ''),
                'url': entry.get('link', ''),
                'published': entry.get('published', ''),
                'author': entry.get('author', ''),
                'description': entry.get('description', '')
            })
        return videos
    except Exception as e:
        print(f"Error fetching videos: {e}")
        return []

def summarize_video(description, title):
    """Use AI to summarize video content"""
    # For now, extract key info from description
    # Can be enhanced to call OpenClaw's AI API
    
    # Clean up description
    clean_desc = description.strip()
    if len(clean_desc) > 500:
        clean_desc = clean_desc[:500] + "..."
    
    return clean_desc if clean_desc else "無描述"

def format_discord_message(video, channel_name):
    """Format message for Discord notification"""
    published = video.get('published', '')
    # Convert published time to HKT
    try:
        dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
        hkt_time = dt.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M HKT')
    except:
        hkt_time = published
    
    summary = summarize_video(video.get('description', ''), video.get('title', ''))
    
    message = f"""## 🎬 新片通知！

**頻道:** {channel_name}
**標題:** {video['title']}
**發布:** {hkt_time}

**簡介:**
{summary}

[📺 觀看視頻]({video['url']})

---
*YouTube Monitor - OpenClaw*"""
    
    return message

def check_new_videos():
    """Main function to check for new videos"""
    print(f"[{datetime.now().isoformat()}] Starting YouTube check...")
    
    # Load config
    config = load_json(CONFIG_FILE, {'channels': []})
    channels = config.get('channels', [])
    
    if not channels:
        print("⚠️ No channels configured in config.json")
        return
    
    # Load state
    state = load_json(STATE_FILE, {
        'lastCheck': None,
        'checkedVideos': []  # List of video IDs already notified
    })
    
    new_videos_found = []
    
    for channel in channels:
        if not channel.get('enabled', True):
            continue
        
        channel_id = channel.get('id')
        channel_name = channel.get('name', 'Unknown Channel')
        
        if not channel_id:
            print(f"⚠️ Skipping channel without ID: {channel_name}")
            continue
        
        rss_url = get_channel_rss(channel_id)
        print(f"Checking {channel_name} ({channel_id})...")
        
        videos = fetch_videos(rss_url)
        
        for video in videos:
            video_id = video.get('video_id')
            
            # Skip if already notified
            if video_id in state.get('checkedVideos', []):
                continue
            
            # New video!
            print(f"🆕 New video found: {video['title']}")
            new_videos_found.append({
                'video': video,
                'channel_name': channel_name
            })
            
            # Add to checked list
            if 'checkedVideos' not in state:
                state['checkedVideos'] = []
            state['checkedVideos'].append(video_id)
    
    # Update state
    state['lastCheck'] = datetime.now(timezone.utc).isoformat()
    
    # Keep only last 100 video IDs to prevent file bloat
    state['checkedVideos'] = state['checkedVideos'][-100:]
    
    save_json(STATE_FILE, state)
    
    # Output results for OpenClaw to process
    if new_videos_found:
        print(f"\n✅ Found {len(new_videos_found)} new video(s)!")
        
        # Save new videos for OpenClaw to send notifications
        new_videos_file = MEMORY_DIR / "youtube-new-videos.json"
        save_json(new_videos_file, {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'videos': new_videos_found
        })
        
        # Print Discord messages
        for item in new_videos_found:
            print("\n--- DISCORD MESSAGE ---")
            print(format_discord_message(item['video'], item['channel_name']))
            print("--- END MESSAGE ---\n")
    else:
        print("\n✅ No new videos found")
    
    print(f"Next check: ~30 minutes")
    return len(new_videos_found)

if __name__ == '__main__':
    check_new_videos()
