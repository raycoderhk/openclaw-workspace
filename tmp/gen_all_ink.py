#!/usr/bin/env python3
"""Generate ink wash paintings for all 21 remaining HK places"""
import os
import json
import urllib.request
import time

API_KEY = os.environ.get("MINIMAX_API_KEY", "sk-cp-mqDZwvwYG1u79lQAq_IoECIzYAvT1eBVcSOj3dIvTKcqRbRux_chEqTj1aHbvOtUCZ65CO6xYLSotXR1ocvisRzU4k6Zj1RiCpaf15ioXj5XW3DA1d8T5no")
URL = "https://api.minimaxi.com/v1/image_generation"
OUT = "/home/node/.openclaw/workspace/mini-games/hk-places-quiz/assets/ink"

INKWASH = """Traditional Chinese ink wash painting (水墨畫). TOP RIGHT empty (留白). Classic 国画水墨, zen, flowing ink gradients, sumi-e brushwork, ethereal, misty. NO text, calligraphy, signatures, seals, or Chinese characters."""

places = [
    ("fishing-junk-peak", "Hong Kong mountain peak with sharp peak rising from green hillsides, hiking trail, scenic view"),
    ("amah-rock", "Large rock formation on hillside in Hong Kong, traditional Chinese landscape, mountainous terrain"),
    ("ap-lei-chau-bridge", "Hong Kong suspension bridge connecting Ap Lei Chau island to mainland, harbor views, coastal scenery"),
    ("rainbow-village", "Colorful apartment buildings in Hong Kong, vibrant rainbow colors, modern residential architecture"),
    ("golden-coast-dolphin", "Hong Kong waterfront plaza with dolphin sculpture, seaside promenade, harbor backdrop"),
    ("harrow-school", "Modern international school building in Hong Kong, contemporary architecture, campus setting"),
    ("murray-house", "Historic colonial building in Stanley, Victorian architecture, stone walls, traditional design"),
    ("wanchai-heliport", "Hong Kong helipad on waterfront, Victoria Harbour backdrop, urban coast"),
    ("shek-kong-airfield", "Hong Kong military airfield with runway, open apron, mountain backdrop"),
    ("tsz-shan-monastery", "Buddhist temple with large bronze Guanyin statue, traditional Chinese architecture, peaceful setting"),
    ("qiandao-lake", "Serene reservoir with multiple islands, calm water reflecting hills, lush greenery"),
    ("stone-jauk-golf", "Hong Kong golf course with manicured greens, palm trees, coastal hillside backdrop"),
    ("avenue-of-stars", "Hong Kong waterfront promenade with movie star handprints, Victoria Harbour night view"),
    ("shing-mun-reservoir", "Hong Kong reservoir with monkey sculptures, calm water, green hillsides, scenic outlook"),
    ("ting-kau-bridge", "Triple-tower cable-stayed bridge in Hong Kong, dramatic cables, coastal setting"),
    ("garden-bakery", "Classic Hong Kong bakery building, traditional storefront, retro architecture"),
    ("park-island", "Modern residential complex on Ma Wan island, colorful buildings, sea views"),
    ("park-island-ferry", "Hong Kong ferry pier at waterfront, small boats in harbor, coastal pier"),
    ("clearwater-bay-golf", "Upscale golf course in Clearwater Bay, coastal cliffs, South China Sea views"),
    ("tsing-ma-bridge", "Massive suspension bridge with two towers, numerous cables, island and mountain backdrop"),
    ("ma-on-shan", "Hong Kong mountain with iron ore quarry remnants, green slopes, hiking trails"),
]

os.makedirs(OUT, exist_ok=True)

for name, desc in places:
    outpath = f"{OUT}/{name}.jpg"
    if os.path.exists(outpath):
        print(f"⏭️  Skip {name} (exists)")
        continue
    
    print(f"🎨 {name}...")
    payload = {
        "model": "image-01",
        "prompt": f"{INKWASH}\n\nSubject: {desc}",
        "image_size": "1024x1536",
        "num_images": 1
    }
    
    try:
        req = urllib.request.Request(
            URL,
            data=json.dumps(payload).encode(),
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            url = result["data"]["image_urls"][0]
            urllib.request.urlretrieve(url, outpath)
            size = os.path.getsize(outpath)
            print(f"✅ {name} saved ({size} bytes)")
    except Exception as e:
        print(f"❌ {name}: {e}")
    time.sleep(1)  # Be nice to the API

print("\nDone!")
