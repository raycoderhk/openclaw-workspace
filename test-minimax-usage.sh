#!/bin/bash
# Test script to demonstrate Minimax usage in OpenClaw

echo "🔍 Checking Minimax configuration..."
echo "======================================"

# 1. Check if agents exist
echo "1. Available Minimax Agents:"
ls -1 /home/node/.openclaw/workspace/agents/minimax-*.json | xargs -I {} basename {}

echo ""
echo "2. Working Minimax Models (from tests):"
echo "   ✅ MiniMax-M2.7"
echo "   ✅ MiniMax-M2.5"
echo "   ✅ MiniMax-M2.5-highspeed"
echo "   ✅ MiniMax-M2"
echo "   ❌ MiniMax-M2.7-highspeed (not supported by your plan)"
echo "   ❌ abab6.5-chat (error 1008 - needs quota allocation)"

echo ""
echo "3. How to use Minimax:"
echo "   Method A: Use sessions_spawn with agentId"
echo "   -----------------------------------------"
echo "   openclaw sessions spawn \\"
echo "     --agent minimax-coding-agent.json \\"
echo "     --task \"Write Python code for web scraping\""
echo ""
echo "   Method B: Set environment variables"
echo "   -----------------------------------"
echo "   export OPENAI_API_KEY=sk-cp-...your-key..."
echo "   export OPENAI_BASE_URL=https://api.minimaxi.com/v1"
echo "   export OPENAI_MODEL=MiniMax-M2.7"
echo ""
echo "   Method C: Programmatic usage"
echo "   ----------------------------"
echo "   sessions_spawn("
echo "     task=\"Debug this code\","
echo "     label=\"coding-help\","
echo "     agentId=\"minimax-coding-agent\""
echo "   )"

echo ""
echo "4. Current OpenClaw Models:"
openclaw models list

echo ""
echo "5. Why Minimax doesn't appear in /models list:"
echo "   • Minimax uses OpenAI-compatible API, not native integration"
echo "   • Configured as specialized agents, not main model entries"
echo "   • Use 'agentId' parameter to access Minimax capabilities"

echo ""
echo "🎯 Recommendation:"
echo "   Keep DeepSeek as default for general tasks"
echo "   Use Minimax agents for specialized tasks when needed"
echo "   Example: minimax-coding-agent for complex programming"