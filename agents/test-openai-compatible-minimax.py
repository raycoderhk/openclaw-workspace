#!/usr/bin/env python3
"""
Test MiniMax OpenAI-compatible API as described in the technical documentation.
This follows the exact specifications from the user's documentation.
"""

import os
import sys
import json
import requests
from pathlib import Path

def load_minimax_api_key():
    """Load MINIMAX_API_KEY from vision/config.env"""
    vision_env_path = Path(__file__).parent.parent / "skills" / "vision" / "config.env"
    
    if not vision_env_path.exists():
        print(f"❌ vision/config.env not found at: {vision_env_path}")
        return None
    
    with open(vision_env_path, 'r') as f:
        content = f.read()
    
    for line in content.split('\n'):
        if line.startswith("MINIMAX_API_KEY="):
            key = line.split('=', 1)[1].strip()
            if key:
                print(f"✅ Found MINIMAX_API_KEY: {key[:10]}...{key[-10:]}")
                return key
    
    print("❌ MINIMAX_API_KEY not found in vision/config.env")
    return None

def test_openai_compatible_api():
    """Test the OpenAI-compatible API endpoint as per documentation"""
    
    api_key = load_minimax_api_key()
    if not api_key:
        return False
    
    base_url = "https://api.minimaxi.com/v1"
    model = "MiniMax-M2.7"
    
    print(f"\n🔧 Testing OpenAI-compatible API:")
    print(f"  Base URL: {base_url}")
    print(f"  Model: {model}")
    print(f"  Using reasoning_split: true")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "reasoning_split": True,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. Respond in one short sentence."
            },
            {
                "role": "user",
                "content": "Say hello and confirm you're using MiniMax M2.7."
            }
        ],
        "max_tokens": 256
    }
    
    try:
        print(f"\n📤 Sending request to {base_url}/chat/completions")
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Response keys: {list(data.keys())}")
            
            if "choices" in data and len(data["choices"]) > 0:
                message = data["choices"][0].get("message", {})
                content = message.get("content", "No content")
                print(f"\n💬 Assistant response: {content}")
                
                # Check for reasoning split
                if "reasoning" in message:
                    print(f"🧠 Reasoning (separated): {message.get('reasoning', 'No reasoning')}")
                else:
                    print("ℹ️ No separate reasoning field (might be in content)")
            
            return True
            
        elif response.status_code == 401:
            print("❌ HTTP 401: Invalid API key or authentication error")
            print("   Check: API key, region, product type")
            
        elif response.status_code == 429:
            print("❌ HTTP 429: Rate limit or quota exceeded")
            data = response.json()
            error_code = data.get("error", {}).get("code", "unknown")
            print(f"   Error code: {error_code}")
            
            if error_code == 1008:
                print("   ⚠️ Code 1008: insufficient_balance - Token or prepaid balance exhausted")
                print("   💡 Solution: Top up or switch plan at https://platform.minimaxi.com/user-center/payment/token-plan")
            
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout (30 seconds)")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - check network or base URL")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    return False

def test_environment_variables():
    """Test if environment variables are set correctly for OpenClaw"""
    print("\n🔍 Checking OpenClaw environment variables:")
    
    env_vars = {
        "OPENAI_API_KEY": "Should be MINIMAX_API_KEY from vision/config.env",
        "OPENAI_BASE_URL": "Should be https://api.minimaxi.com/v1",
        "OPENAI_MODEL": "Should be MiniMax-M2.7 or similar"
    }
    
    all_set = True
    for var, description in env_vars.items():
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: Set ({value[:20]}...)" if len(value) > 20 else f"  ✅ {var}: {value}")
        else:
            print(f"  ⚠️ {var}: Not set ({description})")
            all_set = False
    
    return all_set

def test_curl_command():
    """Generate the curl command from documentation for manual testing"""
    api_key = load_minimax_api_key()
    if not api_key:
        return
    
    print("\n📋 Curl command for manual testing (from documentation):")
    curl_cmd = f"""curl -sS "https://api.minimaxi.com/v1/chat/completions" \\
  -H "Authorization: Bearer {api_key}" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "model": "MiniMax-M2.7",
    "reasoning_split": true,
    "messages": [
      {{
        "role": "system",
        "content": "You are a helpful assistant."
      }},
      {{
        "role": "user",
        "content": "Say hello in one short sentence."
      }}
    ],
    "max_tokens": 256
  }}'"""
    
    print(curl_cmd)

def main():
    """Run all tests"""
    print("=" * 70)
    print("🧪 MiniMax OpenAI-Compatible API Test")
    print("Following technical documentation specifications")
    print("=" * 70)
    
    # Test 1: Load API key
    api_key = load_minimax_api_key()
    if not api_key:
        print("\n❌ Cannot proceed without API key")
        return
    
    # Test 2: Environment variables
    env_ok = test_environment_variables()
    
    # Test 3: API call
    print("\n" + "=" * 70)
    print("🚀 Testing OpenAI-compatible API call")
    print("=" * 70)
    
    api_ok = test_openai_compatible_api()
    
    # Test 4: Generate curl command
    test_curl_command()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Test Summary")
    print("=" * 70)
    
    print(f"API Key loaded: {'✅' if api_key else '❌'}")
    print(f"Environment vars: {'✅' if env_ok else '⚠️'}")
    print(f"API call: {'✅' if api_ok else '❌'}")
    
    if api_ok:
        print("\n🎉 Success! MiniMax OpenAI-compatible API is working.")
        print("\n📚 Next steps:")
        print("  1. Update OpenClaw agent configurations to use:")
        print("     - model: 'MiniMax-M2.7'")
        print("     - model_provider: 'openai'")
        print("     - reasoning_split: true")
        print("  2. Set environment variables if not already set")
        print("  3. Test with actual OpenClaw sessions_spawn")
    else:
        print("\n⚠️ Issues detected. Common solutions:")
        print("  1. Check API key is correct Token Plan key (sk-cp-...)")
        print("  2. Verify balance in MiniMax dashboard")
        print("  3. Ensure base URL is https://api.minimaxi.com/v1")
        print("  4. Check network connectivity")
    
    print("=" * 70)

if __name__ == "__main__":
    main()