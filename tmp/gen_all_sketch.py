#!/usr/bin/env python3
"""Generate pencil sketch versions for ALL remaining HK places"""
import os, json, urllib.request, time

API_KEY = "sk-cp-mqDZwvwYG1u79lQAq_IoECIzYAvT1eBVcSOj3dIvTKcqRbRux_chEqTj1aHbvOtUCZ65CO6xYLSotXR1ocvisRzU4k6Zj1RiCpaf15ioXj5XW3DA1d8T5no"
URL = "https://api.minimaxi.com/v1/image_generation"
OUT = "/home/node/.openclaw/workspace/mini-games/hk-places-quiz/assets/ink"

SKETCH = "Pencil sketch drawing style. Clean line art, hand-drawn aesthetic, cross-hatching shading. Black graphite on white. Preserve original subjects, composition and spatial arrangement exactly. Subtle gray tones for depth. Artistic illustration."

places = [
    ("sketch-murray-house", "Hong Kong Murray House historic colonial building Stanley, stone walls, Victorian architecture, traditional design"),
    ("sketch-wanchai-heliport", "Hong Kong Wan Chai Heliport waterfront, helicopter pad, Victoria Harbour backdrop, urban coast"),
    ("sketch-shekong-airfield", "Hong Kong Shek Kong Airfield military base, runway, hangar buildings, open apron"),
    ("sketch-tszshan-monastery", "Hong Kong Tsz Shan Monastery Buddhist temple, large bronze Guanyin statue, traditional architecture, peaceful"),
    ("sketch-qiandao-lake", "Hong Kong Tai Lam Chung Reservoir islands, calm water reflections, lush green hills, scenic"),
    ("sketch-stonejauk-golf", "Hong Kong Shek O Golf Club lush course, palm trees, coastal hillside backdrop"),
    ("sketch-avenue-of-stars", "Hong Kong Avenue of Stars waterfront promenade, movie star handprints, Victoria Harbour night view"),
    ("sketch-shingmun-reservoir", "Hong Kong Shing Mun Reservoir scenic dam, monkey sculptures, lush green hillsides, calm water"),
    ("sketch-tingkau-bridge", "Hong Kong Ting Kau Bridge triple-tower cable-stayed bridge, dramatic cables, coastal setting"),
    ("sketch-garden-bakery", "Hong Kong Garden Bakery classic building, traditional storefront, retro architectural style"),
    ("sketch-parkisland", "Hong Kong Park Island Ma Wan residential complex, colorful buildings, sea views, modern architecture"),
    ("sketch-parkisland-ferry", "Hong Kong Park Island Ferry pier waterfront, small boats harbor, coastal promenade"),
    ("sketch-clearwaterbay-golf", "Hong Kong Clearwater Bay Golf Club upscale course, coastal cliffs, South China Sea views"),
    ("sketch-tsingma-bridge", "Hong Kong Tsing Ma Bridge massive suspension bridge two towers, hundreds cables, island mountain backdrop"),
    ("sketch-maonshan", "Hong Kong Ma On Shan mountain iron ore quarry remnants, green slopes, hiking trails"),
    ("sketch-harrow-school", "Hong Kong Harrow International School modern campus, contemporary architecture"),
    ("sketch-goldencoast-dolphin", "Hong Kong Gold Coast dolphin sculpture plaza, seaside promenade, harbor views"),
    ("sketch-rainbow-village", "Hong Kong Ma Wan Rainbow Village colorful apartment buildings, vibrant rainbow colors"),
]

os.makedirs(OUT, exist_ok=True)

for name, desc in places:
    outpath = f"{OUT}/{name}.jpg"
    if os.path.exists(outpath):
        print(f"⏭️  Skip {name} (exists)")
        continue
    print(f"🎨 {name}...")
    payload = {"model": "image-01", "prompt": f"{SKETCH}\n\nSubject: {desc}", "image_size": "1024x1536", "num_images": 1}
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

print("\nDone!")
