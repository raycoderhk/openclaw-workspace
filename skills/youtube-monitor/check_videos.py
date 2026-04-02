#!/usr/bin/env python3
"""
YouTube Monitor - Check for new videos from subscribed channels
Uses channel page scraping (works when RSS is blocked)
"""

import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# Paths
WORKSPACE = Path.home() / ".openclaw" / "workspace"
SKILL_DIR = WORKSPACE / "skills" / "youtube-monitor"
MEMORY_DIR = WORKSPACE / "memory"
CONFIG_FILE = SKILL_DIR / "config.json"
STATE_FILE = MEMORY_DIR / "youtube-state.json"
VIDEOS_FILE = MEMORY_DIR / "youtube-videos.json"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

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

def fetch_videos_rss(channel_id):
    """Fallback: try RSS feed"""
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read().decode('utf-8')
        
        import xml.etree.ElementTree as ET
        tree = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015'}
        
        videos = []
        for entry in tree.findall('.//{http://www.w3.org/2005/Atom}entry'):
            vid = entry.find('yt:videoId', ns)
            title = entry.find('{http://www.w3.org/2005/Atom}title')
            published = entry.find('{http://www.w3.org/2005/Atom}published')
            link = entry.find('{http://www.w3.org/2005/Atom}link')
            
            videos.append({
                'video_id': vid.text if vid is not None else '',
                'title': title.text if title is not None else '',
                'url': link.get('href') if link is not None else '',
                'published': published.text if published is not None else '',
                'channel': '',
            })
        return videos, 'rss'
    except Exception as e:
        return [], 'rss_error'

def fetch_videos_scraping(channel_id):
    """Primary: scrape channel page for video list"""
    url = f"https://www.youtube.com/channel/{channel_id}/videos"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8')
        
        # Extract video data from ytInitialData
        match = re.search(r'var ytInitialData = (.+?);</script>', html, re.DOTALL)
        if not match:
            return [], 'parse_error'
        
        data = json.loads(match.group(1))
        
        # Navigate to video list
        contents = data.get('contents', {}).get('twoColumnBrowseResultsRenderer', {}).get('tabs', [])
        video_tab = None
        for tab in contents:
            if tab.get('tabRenderer', {}).get('title', '') == 'Videos':
                video_tab = tab
                break
        
        if not video_tab:
            return [], 'no_videos_tab'
        
        videos_data = video_tab['tabRenderer']['content']['richGridRenderer']['contents']
        
        videos = []
        for item in videos_data:
            renderer = item.get('richItemRenderer', {}).get('content', {}).get('videoRenderer', {})
            if not renderer:
                continue
            
            video_id = renderer.get('videoId', '')
            title_runs = renderer.get('title', {}).get('runs', [])
            title = title_runs[0].get('text', '') if title_runs else ''
            
            # Published time (may be "2 days ago" or ISO date)
            published_text = ''
            published_vert = renderer.get('publishedTimeText', {}).get('simpleText', '')
            
            # Get URL
            url_runs = renderer.get('navigationEndpoint', {}).get('commandMetadata', {}).get('webCommandMetadata', {}).get('url', '')
            
            if video_id and title:
                videos.append({
                    'video_id': video_id,
                    'title': title,
                    'url': 'https://youtube.com' + url_runs,
                    'published': published_vert,
                    'channel': '',
                })
        
        return videos, 'scraping'
    except Exception as e:
        return [], f'scraping_error: {e}'

def fetch_videos(channel_id):
    """Try RSS first, fall back to scraping"""
    videos, method = fetch_videos_rss(channel_id)
    if videos:
        return videos, method
    
    videos, method = fetch_videos_scraping(channel_id)
    return videos, method

def check_new_videos():
    print(f"[{datetime.now().isoformat()}] Starting YouTube check...")
    
    config = load_json(CONFIG_FILE)
    state = load_json(STATE_FILE)
    sent = load_json(VIDEOS_FILE, [])
    
    sent_ids = set(sent) if isinstance(sent, list) else set()
    all_new = []
    
    for channel in config.get('channels', []):
        if not channel.get('enabled', True):
            continue
        
        print(f"\nChecking {channel['name']} ({channel['id']})...")
        videos, method = fetch_videos(channel['id'])
        
        new_for_channel = 0
        for video in videos:
            if video['video_id'] not in sent_ids:
                video['channel'] = channel['name']
                print(f"  🆕 {video['title'][:60]}...")
                all_new.append(video)
                new_for_channel += 1
            else:
                print(f"  ✅ already sent")
        
        print(f"  Method: {method} | New: {new_for_channel}")
    
    if all_new:
        print(f"\n✅ Found {len(all_new)} new video(s)!")
        
        new_videos_file = MEMORY_DIR / "youtube-new-videos.json"
        save_json(new_videos_file, {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'videos': all_new
        })
        
        print("\n📬 Sending Discord notifications...")
        send_notifications(all_new)
        
        sent.extend([v['video_id'] for v in all_new])
        save_json(VIDEOS_FILE, sent)
        save_json(STATE_FILE, {'lastCheck': datetime.now(timezone.utc).isoformat()})
    else:
        print(f"\n✅ No new videos found")
    
    print(f"Next check: ~30 minutes")
    return len(all_new)

def send_notifications(videos):
    import subprocess
    notify_script = SKILL_DIR / "notify_discord.py"
    webhook_url = 'https://discord.com/api/webhooks/1488017483368501299/X2YLwe54qZFzURcWLpZ_MU_GB_JWMS5HP1hNqJmq7Q5xtBK_Xsb6A_rp98AjEe0s4GSi'
    result = subprocess.run(
        [sys.executable, str(notify_script)],
        env={**os.environ, 'DISCORD_WEBHOOK_URL': webhook_url},
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

if __name__ == '__main__':
    check_new_videos()
