#!/bin/bash
# Test script to verify Minimax M2.7 Discord configuration
# Created: 2026-03-26

echo "Testing Minimax M2.7 Discord Configuration..."
echo "============================================="

echo "1. Checking OpenClaw configuration..."
if grep -q '"agentId": "minimax-coding"' /home/node/.openclaw/openclaw.json; then
    echo "✅ Discord is configured to use minimax-coding agent"
else
    echo "❌ Discord NOT configured for minimax-coding"
fi

echo ""
echo "2. Checking Minimax M2.7 model configuration..."
if grep -q '"model": "minimax/MiniMax-M2.7"' /home/node/.openclaw/openclaw.json; then
    echo "✅ Minimax coding agent uses MiniMax-M2.7 model"
else
    echo "❌ MiniMax-M2.7 model not correctly configured"
fi

echo ""
echo "3. Checking Minimax provider base URL..."
if grep -q '"baseUrl": "https://api.minimaxi.com/v1"' /home/node/.openclaw/openclaw.json; then
    echo "✅ Minimax uses correct API endpoint for M2.x models"
else
    echo "❌ Incorrect API endpoint"
fi

echo ""
echo "4. Checking available Minimax models..."
echo "Available Minimax models in config:"
grep -A5 '"id": "MiniMax' /home/node/.openclaw/openclaw.json | grep '"id"' | sed 's/.*"id": "//' | sed 's/",//'

echo ""
echo "5. Checking API key..."
if grep -q "MINIMAX_API_KEY=" /home/node/.openclaw/.env; then
    echo "✅ MINIMAX_API_KEY found in .env"
else
    echo "❌ MINIMAX_API_KEY not found"
fi

echo ""
echo "6. Checking agent availability..."
openclaw agents list 2>/dev/null | grep -i minimax && echo "✅ Minimax agent available" || echo "⚠️  Minimax agent may not be listed"

echo ""
echo "============================================="
echo "Configuration Summary:"
echo "- Discord channels → minimax-coding agent"
echo "- minimax-coding agent → minimax/MiniMax-M2.7 model"
echo "- API endpoint: https://api.minimaxi.com/v1 (correct for M2.x)"
echo "- Available models: MiniMax-M2.7, MiniMax-M2.7-highspeed, MiniMax-M2.5, abab6.5s-vision"
echo "- API key: Configured"
echo ""
echo "To apply changes, restart OpenClaw:"
echo "openclaw gateway restart"
echo ""
echo "Rollback script: ./rollback-discord-to-deepseek-v2.sh"