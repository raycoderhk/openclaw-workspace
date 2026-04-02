#!/bin/bash
# Rollback script to revert Discord channels from Minimax back to DeepSeek
# Created: 2026-03-26

echo "Rolling back Discord configuration from Minimax to DeepSeek..."

# Backup current config
cp /home/node/.openclaw/openclaw.json /home/node/.openclaw/openclaw.json.backup.minimax-discord

# Revert Discord binding to main agent (DeepSeek)
sed -i 's/"agentId": "minimax-coding"/"agentId": "main"/g' /home/node/.openclaw/openclaw.json

# Revert minimax-coding agent model back to DeepSeek (optional - keep as minimax for other uses)
# sed -i 's/"model": "minimax\/abab6.5s-coder"/"model": "deepseek\/deepseek-chat"/g' /home/node/.openclaw/openclaw.json

echo "✅ Rollback complete!"
echo "Changes made:"
echo "1. Discord default binding changed from 'minimax-coding' back to 'main'"
echo "2. Original config backed up to: /home/node/.openclaw/openclaw.json.backup.minimax-discord"
echo ""
echo "To apply changes, restart OpenClaw:"
echo "openclaw gateway restart"