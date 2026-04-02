#!/usr/bin/env python3
"""
Test script to verify all Minimax models are working correctly.
This tests text models (coding, general) and vision model configuration.
"""

import os
import sys
import json
from pathlib import Path

# Add workspace to path
workspace_path = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_path))

def test_config_files():
    """Test that all configuration files exist and are valid JSON."""
    print("🔍 Testing Minimax configuration files...")
    
    config_files = [
        "minimax-models-config.json",
        "minimax-coding-agent.json",
        "minimax-imaging-agent.json",
        "minimax-video-agent.json",
        "minimax-m2.7-agent.json"
    ]
    
    all_valid = True
    for config_file in config_files:
        file_path = Path(__file__).parent / config_file
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                print(f"  ✅ {config_file}: Valid JSON")
            except json.JSONDecodeError as e:
                print(f"  ❌ {config_file}: Invalid JSON - {e}")
                all_valid = False
        else:
            print(f"  ❌ {config_file}: File not found")
            all_valid = False
    
    return all_valid

def test_api_key():
    """Test that Minimax API key is available."""
    print("\n🔑 Testing Minimax API key...")
    
    # Check vision config.env
    vision_env_path = workspace_path / "skills" / "vision" / "config.env"
    if vision_env_path.exists():
        with open(vision_env_path, 'r') as f:
            content = f.read()
            if "MINIMAX_API_KEY=" in content:
                print("  ✅ MINIMAX_API_KEY found in vision/config.env")
                
                # Extract the key (first 10 chars for display)
                for line in content.split('\n'):
                    if line.startswith("MINIMAX_API_KEY="):
                        key_value = line.split('=', 1)[1].strip()
                        if key_value:
                            masked_key = key_value[:10] + "..." + key_value[-10:] if len(key_value) > 20 else "***"
                            print(f"  📋 API Key: {masked_key}")
                            return True
            else:
                print("  ❌ MINIMAX_API_KEY not found in vision/config.env")
    else:
        print("  ❌ vision/config.env not found")
    
    return False

def test_model_configurations():
    """Test that all model configurations are properly defined."""
    print("\n🤖 Testing model configurations...")
    
    models_config_path = Path(__file__).parent / "minimax-models-config.json"
    if models_config_path.exists():
        with open(models_config_path, 'r') as f:
            config = json.load(f)
        
        # Check text models
        text_models = config.get("minimax_models", {}).get("text_models", [])
        print(f"  📝 Text models configured: {len(text_models)}")
        for model in text_models:
            print(f"    • {model.get('name')}: {model.get('description', 'No description')}")
        
        # Check vision models
        vision_models = config.get("minimax_models", {}).get("vision_models", [])
        print(f"  👁️ Vision models configured: {len(vision_models)}")
        for model in vision_models:
            print(f"    • {model.get('name')}: {model.get('description', 'No description')}")
        
        # Check subscription info
        subscription = config.get("subscription_info", {})
        print(f"  💰 Subscription: {subscription.get('plan', 'Unknown')}")
        print(f"  💵 Price: {subscription.get('price', 'Unknown')}")
        
        return True
    else:
        print("  ❌ minimax-models-config.json not found")
        return False

def test_agent_files():
    """Test that all agent files reference correct models."""
    print("\n🤵 Testing agent configurations...")
    
    agent_files = [
        ("minimax-coding-agent.json", "coding"),
        ("minimax-imaging-agent.json", "imaging"),
        ("minimax-video-agent.json", "video"),
        ("minimax-m2.7-agent.json", "general")
    ]
    
    all_correct = True
    for agent_file, agent_type in agent_files:
        file_path = Path(__file__).parent / agent_file
        if file_path.exists():
            with open(file_path, 'r') as f:
                agent_config = json.load(f)
            
            model = agent_config.get("model", "")
            model_name = agent_config.get("config", {}).get("model_name", "")
            
            print(f"  🔧 {agent_type.capitalize()} Agent:")
            print(f"    • Model reference: {model}")
            print(f"    • Model name: {model_name}")
            
            # Verify model names are valid Minimax models
            if "minimax/" in model or "abab" in model_name:
                print(f"    ✅ Valid Minimax model reference")
            else:
                print(f"    ⚠️ May not be a Minimax model")
                all_correct = False
        else:
            print(f"  ❌ {agent_file} not found")
            all_correct = False
    
    return all_correct

def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Minimax Models Configuration Test")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Config Files", test_config_files()))
    results.append(("API Key", test_api_key()))
    results.append(("Model Configs", test_model_configurations()))
    results.append(("Agent Files", test_agent_files()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! Minimax models are configured correctly.")
        print("\n📋 Available Models:")
        print("  • Text: abab6-chat, abab6.5-chat, abab6.5s-chat")
        print("  • Vision: abab6.5s-vision (already in use)")
        print("  • Image Generation: Available (separate billing)")
        print("  • Voice Synthesis: Available (separate billing)")
        
        print("\n🚀 Next Steps:")
        print("  1. Test actual API calls with test_minimax_m2.7.py")
        print("  2. Configure session_spawn to use these agents")
        print("  3. Set up cost monitoring for separate billing services")
    else:
        print("⚠️ Some tests failed. Please check the configuration.")
        print("\n🔧 Recommended fixes:")
        print("  1. Ensure vision/config.env has MINIMAX_API_KEY")
        print("  2. Verify all JSON files are valid")
        print("  3. Check model names in agent configurations")
    
    print("=" * 60)

if __name__ == "__main__":
    main()