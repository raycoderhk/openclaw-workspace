#!/usr/bin/env python3
"""
Token 用量分析工具
分析 OpenClaw 配置，識別 Token 消耗熱點，提供優化建議
"""

import json
import os
from pathlib import Path

# 配置
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"

def load_config():
    """讀取 OpenClaw 配置"""
    with open(OPENCLAW_CONFIG, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_models(config):
    """分析模型配置"""
    print("\n" + "="*60)
    print("📊 模型配置分析")
    print("="*60)
    
    providers = config.get('models', {}).get('providers', {})
    
    for provider_name, provider_config in providers.items():
        print(f"\n🔹 {provider_name.upper()}")
        models = provider_config.get('models', [])
        
        for model in models:
            model_id = model.get('id', 'Unknown')
            context = model.get('contextWindow', 'N/A')
            max_tokens = model.get('maxTokens', 'N/A')
            cost = model.get('cost', {})
            
            print(f"  • {model_id}")
            print(f"    Context: {context:,} | Max: {max_tokens:,}")
            
            if cost and any(v != 0 for v in cost.values()):
                print(f"    Cost: In=${cost.get('input',0)}/1k, Out=${cost.get('output',0)}/1k")
            else:
                print(f"    Cost: 免費 / 未配置")

def analyze_agents(config):
    """分析 Agent 配置"""
    print("\n" + "="*60)
    print("🤖 Agent 配置分析")
    print("="*60)
    
    agents = config.get('agents', {}).get('list', [])
    
    for agent in agents:
        agent_id = agent.get('id', 'Unknown')
        agent_name = agent.get('name', 'Unnamed')
        model = agent.get('model', 'Default')
        is_default = agent.get('default', False)
        
        print(f"\n🔹 {agent_name} ({agent_id}){' ⭐' if is_default else ''}")
        print(f"   Model: {model}")
        
        # Sub-agent 配置
        subagents = agent.get('subagents', {})
        if subagents:
            print(f"   Sub-agents: 允許 {subagents.get('allowAgents', ['*'])}")

def analyze_tools(config):
    """分析工具配置"""
    print("\n" + "="*60)
    print("🛠️  工具配置分析")
    print("="*60)
    
    tools = config.get('tools', {})
    
    for tool_name, tool_config in tools.items():
        if isinstance(tool_config, dict):
            enabled = tool_config.get('enabled', True)
            print(f"\n🔹 {tool_name}: {'✅' if enabled else '❌'}")
        else:
            print(f"\n🔹 {tool_name}: {tool_config}")

def identify_optimization_opportunities(config):
    """識別優化機會"""
    print("\n" + "="*60)
    print("💡 優化機會分析")
    print("="*60)
    
    opportunities = []
    
    # 檢查 1: 是否使用免費模型
    providers = config.get('models', {}).get('providers', {})
    free_models = []
    paid_models = []
    
    for provider_name, provider_config in providers.items():
        for model in provider_config.get('models', []):
            cost = model.get('cost', {})
            if cost and any(v != 0 for v in cost.values()):
                paid_models.append(model['id'])
            else:
                free_models.append(model['id'])
    
    if free_models:
        opportunities.append({
            'type': '免費模型可用',
            'description': f"以下模型免費：{', '.join(free_models)}",
            'potential_saving': '100% (對於這些模型)'
        })
    
    # 檢查 2: Sub-agents 使用便宜模型
    defaults = config.get('agents', {}).get('defaults', {})
    subagents_config = defaults.get('subagents', {})
    subagent_model = subagents_config.get('model', '')
    
    if 'turbo' in subagent_model.lower() or 'cheap' in subagent_model.lower():
        opportunities.append({
            'type': 'Sub-agents 使用經濟模型',
            'description': f"Sub-agents 使用 {subagent_model}",
            'potential_saving': '50-70% (相比主模型)'
        })
    else:
        opportunities.append({
            'type': 'Sub-agents 模型優化',
            'description': f"考慮將 Sub-agents 改為使用更經濟的模型 (當前：{subagent_model})",
            'potential_saving': '50-70%'
        })
    
    # 檢查 3: Prompt 模板 (需要檢查 skills)
    opportunities.append({
        'type': 'Prompt 模板優化',
        'description': '檢查 skills 中的 prompt 模板，減少冗餘描述',
        'potential_saving': '5-10%'
    })
    
    # 檢查 4: Response 緩存
    opportunities.append({
        'type': 'Response 緩存',
        'description': '實施重複查詢緩存機制',
        'potential_saving': '15-25%'
    })
    
    # 顯示所有機會
    for i, opp in enumerate(opportunities, 1):
        print(f"\n💡 機會 #{i}: {opp['type']}")
        print(f"   描述：{opp['description']}")
        print(f"   預計節省：{opp['potential_saving']}")
    
    # 總結
    print("\n" + "="*60)
    print("📊 總結")
    print("="*60)
    print(f"發現 {len(opportunities)} 個優化機會")
    print(f"累計潛在節省：50-80% (如果實施所有優化)")

def main():
    print("\n🔍 OpenClaw Token 用量分析工具")
    print("="*60)
    
    try:
        config = load_config()
        print("✅ 配置加載成功")
        
        analyze_models(config)
        analyze_agents(config)
        analyze_tools(config)
        identify_optimization_opportunities(config)
        
    except Exception as e:
        print(f"❌ 錯誤：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
