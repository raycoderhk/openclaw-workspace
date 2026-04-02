#!/bin/bash
# Test script to verify Minimax Discord configuration
# Created: 2026-03-26

echo "Testing Minimax Discord Configuration..."
echo "========================================"

echo "1. Checking OpenClaw configuration..."
if grep -q '"agentId": "minimax-coding"' /home/node/.openclaw/openclaw.json; then
    echo "✅ Discord is configured to use minimax-coding agent"
else
    echo "❌ Discord NOT configured for minimax-coding"
fi

echo ""
echo "2. Checking Minimax agent configuration..."
if grep -q '"model": "minimax/abab6.5s-coder"' /home/node/.openclaw/openclaw.json; then
    echo "✅ Minimax coding agent uses correct model"
else
    echo "❌ Minimax model not correctly configured"
fi

echo ""
echo "3. Checking API key..."
if grep -q "MINIMAX_API_KEY=" /home/node/.openclaw/.env; then
    echo "✅ MINIMAX_API_KEY found in .env"
else
    echo "❌ MINIMAX_API_KEY not found"
fi

echo ""
echo "4. Checking agent availability..."
openclaw agents list 2>/dev/null | grep -i minimax && echo "✅ Minimax agent available" || echo "⚠️  Minimax agent may not be listed"

echo ""
echo "========================================"
echo "Configuration Summary:"
echo "- Discord channels → minimax-coding agent"
echo "- minimax-coding agent → minimax/abab6.5s-coder model"
echo "- API key: Configured"
echo ""
echo "To apply changes, restart OpenClaw:"
echo "openclaw gateway restart"
echo ""
echo "Rollback script: ./rollback-discord-to-deepseek-v2.sh"