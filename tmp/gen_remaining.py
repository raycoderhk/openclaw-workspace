#!/usr/bin/env python3
"""Generate remaining 3 ink wash paintings"""
import os
import json
import urllib.request
import time

API_KEY = "sk-cp-mqDZwvwYG1u79lQAq_IoECIzYAvT1eBVcSOj3dIvTKcqRbRux_chEqTj1aHbvOtUCZ65CO6xYLSotXR1ocvisRzU4k6Zj1RiCpaf15ioXj5XW3DA1d8T5no"
URL = "https://api.minimaxi.com/v1/image_generation"
OUT = "/home/node/.openclaw/workspace/mini-games/hk-places-quiz/assets/ink"

INKWASH = "Traditional Chinese ink wash painting (水墨畫). TOP RIGHT empty (留白). Classic 国画水墨, zen, flowing ink, sumi-e, ethereal, misty. NO text/calligraphy/seals."

remaining = [
    ("clearwater-bay-golf", "Upscale golf course perched on coastal cliffs, South China Sea views, Clearwater Bay Hong Kong"),
    ("park-island-ferry", "Hong Kong ferry pier with small boats in harbor, waterfront promenade, coastal scenery"),
    ("tsing-ma-bridge", "Massive suspension bridge with two grand towers, hundreds of suspension cables, island and mountain backdrop"),
]

for name, desc in remaining:
    outpath = f"{OUT}/{name}.jpg"
    print(f"🎨 {name}...")
    payload = {"model": "image-01", "prompt": f"{INKWASH}\n\nSubject: {desc}", "image_size": "1024x1536", "num_images": 1}
    try:
        req = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            url = result["data"]["image_urls"][0]
            urllib.request.urlretrieve(url, outpath)
            print(f"✅ {name} ({os.path.getsize(outpath)} bytes)")
    except Exception as e:
        print(f"❌ {name}: {e}")
    time.sleep(1)

print("Done!")
