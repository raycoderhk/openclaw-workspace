#!/usr/bin/env python3
"""
Test different MiniMax model names to find the correct one.
"""

import os
import sys
import json
import requests
from pathlib import Path

def load_minimax_api_key():
    """Load MINIMAX_API_KEY from vision/config.env"""
    vision_env_path = Path(__file__).parent.parent / "skills" / "vision" / "config.env"
    
    with open(vision_env_path, 'r') as f:
        content = f.read()
    
    for line in content.split('\n'):
        if line.startswith("MINIMAX_API_KEY="):
            return line.split('=', 1)[1].strip()
    
    return None

def test_model(model_name):
    """Test a specific model name"""
    api_key = load_minimax_api_key()
    if not api_key:
        return False, "No API key"
    
    base_url = "https://api.minimaxi.com/v1"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model_name,
        "reasoning_split": True,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. Respond with just the model name you're using."
            },
            {
                "role": "user",
                "content": "What model are you?"
            }
        ],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0].get("message", {}).get("content", "")
                return True, content.strip()
            else:
                return False, f"No choices in response"
        else:
            return False, f"HTTP {response.status_code}: {response.text[:100]}"
            
    except Exception as e:
        return False, f"Error: {e}"

def main():
    """Test all possible model names"""
    print("Testing MiniMax model names...")
    print("=" * 60)
    
    # Model names from documentation and research
    model_names = [
        "MiniMax-M2.7",
        "MiniMax-M2.7-highspeed",
        "MiniMax-M2.5",
        "MiniMax-M2.5-highspeed",
        "MiniMax-M2.2",
        "MiniMax-M2.2-highspeed",
        "MiniMax-M2",
        "MiniMax-M2-highspeed",
        "abab6.5-chat",
        "abab6.5s-chat",
        "abab6-chat",
        "abab6.5s-vision"
    ]
    
    results = []
    for model_name in model_names:
        print(f"Testing: {model_name:<25}", end="", flush=True)
        success, result = test_model(model_name)
        
        if success:
            print(f" ✅ - {result}")
            results.append((model_name, True, result))
        else:
            print(f" ❌ - {result}")
            results.append((model_name, False, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("Working models:")
    print("-" * 60)
    
    working_models = [(name, result) for name, success, result in results if success]
    for name, result in working_models:
        print(f"  • {name}: {result}")
    
    if not working_models:
        print("  No working models found")
    
    print("\n" + "=" * 60)
    print("Recommended model for OpenClaw:")
    print("-" * 60)
    
    # Prioritize M2.7 if available
    for name, success, result in results:
        if success and "M2.7" in name:
            print(f"  Use: {name}")
            print(f"  Reason: {result}")
            break
    else:
        # Fall back to any working model
        for name, success, result in results:
            if success:
                print(f"  Use: {name}")
                print(f"  Reason: {result}")
                break
        else:
            print("  No working models found - check API key and balance")

if __name__ == "__main__":
    main()