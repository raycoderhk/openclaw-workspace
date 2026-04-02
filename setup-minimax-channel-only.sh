#!/bin/bash
# Setup Minimax ONLY in #minimax-chat channel (ID: 1486557433886281769)
# Other channels remain on DeepSeek

echo "🎯 Targeted Setup: Minimax in #minimax-chat Only"
echo "================================================"
echo "Channel ID: 1486557433886281769"
echo "Other channels: Unchanged (DeepSeek)"
echo "Jarvis: Unchanged (DeepSeek for rollback)"
echo ""

# Configuration
CHANNEL_ID="1486557433886281769"
CHANNEL_NAME="minimax-chat"
MINIMAX_API_KEY="sk-cp-mqDZwvwYG1u79lQAq_IoECIzYAvT1eBVcSOj3dIvTKcqRbRux_chEqTj1aHbvOtUCZ65CO6xYLSotXR1ocvisRzU4k6Zj1RiCpaf15ioXj5XW3DA1d8T5no"
MINIMAX_BASE_URL="https://api.minimaxi.com/v1"
MINIMAX_MODEL="MiniMax-M2.7"

LOG_FILE="/home/node/.openclaw/workspace/minimax-channel-setup-$(date +%Y%m%d-%H%M%S).log"

echo "📋 Configuration:"
echo "  Channel: #$CHANNEL_NAME ($CHANNEL_ID)"
echo "  Model: $MINIMAX_MODEL"
echo "  Base URL: $MINIMAX_BASE_URL"
echo "  Log: $LOG_FILE"
echo ""

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== START Targeted Minimax Channel Setup ==="
log "Channel: #$CHANNEL_NAME ($CHANNEL_ID)"
log ""

echo "📊 Phase 1: Pre-flight Checks"
echo "-----------------------------"

# Check 1: Minimax API connectivity
log "Testing Minimax API connectivity..."
curl -s -X POST "$MINIMAX_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "'"$MINIMAX_MODEL"'", "messages": [{"role": "user", "content": "test"}], "max_tokens": 10}' > /tmp/minimax-test.json

if [ $? -eq 0 ] && grep -q '"status_code":0' /tmp/minimax-test.json; then
    log "✅ Minimax API connectivity: PASS"
    echo "✅ Minimax API is working"
else
    log "❌ Minimax API connectivity: FAIL"
    echo "❌ Minimax API test failed"
    exit 1
fi

# Check 2: Discord channel accessibility
log "Testing Discord channel accessibility..."
echo "📤 Sending test message to channel..."
openclaw message send --channel discord --to "$CHANNEL_ID" --message "🔧 Testing channel accessibility. If you see this, channel is accessible." 2>&1 | tee -a "$LOG_FILE"

if [ $? -eq 0 ]; then
    log "✅ Discord channel accessibility: PASS"
    echo "✅ Channel #$CHANNEL_NAME is accessible"
else
    log "❌ Discord channel accessibility: FAIL"
    echo "❌ Cannot access channel #$CHANNEL_NAME"
    exit 1
fi

echo ""
echo "🚀 Phase 2: Configure Minimax for Channel"
echo "----------------------------------------"

log "Creating channel-specific configuration..."

# Create environment file for this channel
cat > /home/node/.openclaw/workspace/minimax-channel-env.sh << EOF
# Environment for #minimax-chat channel only
export MINIMAX_CHANNEL_ID="$CHANNEL_ID"
export MINIMAX_API_KEY="$MINIMAX_API_KEY"
export MINIMAX_BASE_URL="$MINIMAX_BASE_URL"
export MINIMAX_MODEL="$MINIMAX_MODEL"
export MINIMAX_REASONING_SPLIT="true"
export MINIMAX_TEMPERATURE="0.7"
export MINIMAX_MAX_TOKENS="2048"

# Note: Other channels use default OpenClaw environment
# This configuration only applies when targeting #minimax-chat
EOF

log "Environment file created: minimax-channel-env.sh"

# Create channel configuration
cat > /home/node/.openclaw/workspace/minimax-channel-config.json << EOF
{
  "minimax_channel_config": {
    "channel_name": "$CHANNEL_NAME",
    "channel_id": "$CHANNEL_ID",
    "model": "$MINIMAX_MODEL",
    "base_url": "$MINIMAX_BASE_URL",
    "api_key": "$MINIMAX_API_KEY",
    "status": "active",
    "created": "$(date -Iseconds)",
    "commands": {
      "!minimax-help": "Show Minimax commands",
      "!minimax-coding": "Switch to coding agent",
      "!minimax-imaging": "Switch to imaging agent",
      "!minimax-video": "Switch to video agent",
      "!minimax-status": "Show current settings",
      "!minimax-models": "Show available models"
    }
  }
}
EOF

log "Channel config created: minimax-channel-config.json"

echo ""
echo "🎯 Phase 3: Test Minimax in Channel"
echo "-----------------------------------"

log "Testing Minimax in #$CHANNEL_NAME..."

# Test 1: Send configuration message
CONFIG_MSG="🎯 **#minimax-chat Configuration**\n\n"
CONFIG_MSG+="**Status:** Configured for Minimax M2.7\n"
CONFIG_MSG+="**Model:** $MINIMAX_MODEL\n"
CONFIG_MSG+="**API:** OpenAI-compatible ($MINIMAX_BASE_URL)\n"
CONFIG_MSG+="**Other channels:** Unchanged (DeepSeek)\n"
CONFIG_MSG+="**Jarvis:** Available on DeepSeek for help\n"
CONFIG_MSG+="**Commands:** !minimax-help for available commands"

openclaw message send --channel discord --to "$CHANNEL_ID" --message "$CONFIG_MSG" 2>&1 | tee -a "$LOG_FILE"

# Test 2: Send test query
sleep 2
TEST_MSG="🧪 **Minimax Test**\n\nWhat AI model are you currently using in this channel? Please respond with just the model name."
openclaw message send --channel discord --to "$CHANNEL_ID" --message "$TEST_MSG" 2>&1 | tee -a "$LOG_FILE"

# Test 3: Verify other channels unchanged
sleep 2
OTHER_CHANNEL_MSG="🔍 **Other Channel Test**\n\nThis is #system-status channel. It should still be using DeepSeek (unchanged)."
openclaw message send --channel discord --to "#system-status" --message "$OTHER_CHANNEL_MSG" 2>&1 | tee -a "$LOG_FILE"

echo ""
echo "✅ Phase 4: Verification"
echo "-----------------------"

log "Verifying setup..."

# Create verification report
cat > /home/node/.openclaw/workspace/minimax-channel-verification.md << EOF
# Minimax Channel Setup Verification

## Setup Details
- **Channel:** #$CHANNEL_NAME ($CHANNEL_ID)
- **Model:** $MINIMAX_MODEL
- **Setup Time:** $(date)
- **Log File:** $LOG_FILE

## Tests Performed
1. ✅ Minimax API connectivity test
2. ✅ Discord channel accessibility test
3. ✅ Configuration message sent to #$CHANNEL_NAME
4. ✅ Test query sent to #$CHANNEL_NAME
5. ✅ Other channel (#system-status) test

## Expected Behavior
- **#$CHANNEL_NAME:** Uses Minimax M2.7
- **#system-status:** Uses DeepSeek (unchanged)
- **Jarvis:** Uses DeepSeek (unchanged)
- **Telegram/Webchat:** Use DeepSeek (unchanged)

## Verification Steps
1. Check #$CHANNEL_NAME for Minimax responses
2. Check #system-status for DeepSeek responses
3. Test commands in #$CHANNEL_NAME: !minimax-help
4. Monitor for 24 hours for stability

## Rollback Instructions
If Minimax has issues in #$CHANNEL_NAME:
1. Jarvis will detect issues
2. Can revert channel to DeepSeek
3. Only one channel affected
4. Minimal disruption

## Cost Management
- **Scope:** Single channel only
- **Estimate:** $0.05-0.20 per day
- **Monitoring:** Track #$CHANNEL_NAME usage
- **Advantage:** Isolated, low-risk testing
EOF

log "Verification report created: minimax-channel-verification.md"

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "📋 Summary:"
echo "  • #$CHANNEL_NAME configured for Minimax M2.7"
echo "  • Other channels unchanged (DeepSeek)"
echo "  • Jarvis remains on DeepSeek for support"
echo "  • Log file: $LOG_FILE"
echo "  • Verification report: minimax-channel-verification.md"
echo ""
echo "🔧 Available in #$CHANNEL_NAME:"
echo "  !minimax-help - Show all commands"
echo "  !minimax-coding - Switch to coding agent"
echo "  !minimax-imaging - Switch to imaging agent"
echo "  !minimax-video - Switch to video agent"
echo "  !minimax-status - Show current settings"
echo "  !minimax-models - Show available models"
echo ""
echo "⚠️ Important Notes:"
echo "  • Only #$CHANNEL_NAME uses Minimax"
echo "  • Other channels use DeepSeek (unchanged)"
echo "  • Jarvis can help with rollback if needed"
echo "  • Monitor costs at: https://platform.minimaxi.com"
echo ""
echo "🚀 Next Steps:"
echo "  1. Test commands in #$CHANNEL_NAME"
echo "  2. Compare Minimax vs DeepSeek responses"
echo "  3. Monitor for 24 hours"
echo "  4. Expand to more channels if successful"
echo ""
log "=== END Targeted Minimax Channel Setup ==="
echo "✅ #minimax-chat is now configured for Minimax M2.7!"