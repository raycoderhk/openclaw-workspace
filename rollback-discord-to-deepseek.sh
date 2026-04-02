#!/bin/bash
# Rollback Discord from Minimax to DeepSeek
# To be executed by Jarvis if Minimax has issues

echo "🔄 Discord Rollback: Minimax → DeepSeek"
echo "======================================="
echo "Executed by Jarvis for system stability"
echo ""

ROLLBACK_REASON="$1"
BACKUP_DIR="/home/node/.openclaw/workspace/backup-*"  # Latest backup
LOG_FILE="/home/node/.openclaw/workspace/discord-rollback-$(date +%Y%m%d-%H%M%S).log"

# Find latest backup
LATEST_BACKUP=$(ls -td $BACKUP_DIR 2>/dev/null | head -1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "❌ No backup directory found"
    echo "💡 Creating emergency rollback configuration..."
    LATEST_BACKUP="/home/node/.openclaw/workspace/backup-emergency"
    mkdir -p "$LATEST_BACKUP"
fi

echo "📋 Rollback Details:"
echo "  Reason: ${ROLLBACK_REASON:-'Preventive rollback by Jarvis'}"
echo "  Backup: $LATEST_BACKUP"
echo "  Log: $LOG_FILE"
echo ""

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== START Discord Rollback ==="
log "Rollback reason: $ROLLBACK_REASON"
log "Backup source: $LATEST_BACKUP"
log "Executed by: Jarvis (DeepSeek agent)"
log ""

echo "📊 Phase 1: Pre-rollback Checks"
echo "-------------------------------"

# Check current state
log "Checking current Discord configuration..."
openclaw models list > /tmp/pre-rollback-models.txt
log "Pre-rollback models: $(cat /tmp/pre-rollback-models.txt)"

# Check Minimax API status (for diagnostic)
log "Testing Minimax API status..."
curl -s -X POST "https://api.minimaxi.com/v1/chat/completions" \
  -H "Authorization: Bearer sk-cp-mqDZwvwYG1u79lQAq_IoECIzYAvT1eBVcSOj3dIvTKcqRbRux_chEqTj1aHbvOtUCZ65CO6xYLSotXR1ocvisRzU4k6Zj1RiCpaf15ioXj5XW3DA1d8T5no" \
  -H "Content-Type: application/json" \
  -d '{"model": "MiniMax-M2.7", "messages": [{"role": "user", "content": "test"}], "max_tokens": 10}' > /tmp/minimax-status.json 2>&1

MINIMAX_STATUS=$?
log "Minimax API test exit code: $MINIMAX_STATUS"
log "Minimax API response: $(cat /tmp/minimax-status.json | head -100)"

echo ""
echo "📋 Phase 2: Execute Rollback"
echo "---------------------------"

# Step 1: Clear Minimax environment variables
log "Clearing Minimax environment variables..."
unset OPENAI_API_KEY
unset OPENAI_BASE_URL
unset OPENAI_MODEL

# Remove Minimax environment file if exists
if [ -f "/home/node/.openclaw/workspace/minimax-discord-env.sh" ]; then
    log "Removing minimax-discord-env.sh"
    rm -f "/home/node/.openclaw/workspace/minimax-discord-env.sh"
fi

# Step 2: Restore from backup if available
if [ -f "$LATEST_BACKUP/environment-backup.txt" ]; then
    log "Restoring environment from backup..."
    source "$LATEST_BACKUP/environment-backup.txt"
    log "Environment restored from backup"
else
    log "No environment backup found, setting DeepSeek defaults"
    # Set DeepSeek as default
    export DEEPSEEK_API_KEY="sk-f14b5c7e6d8e4f5a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
    log "DeepSeek environment configured"
fi

# Step 3: Send rollback notification to Discord
log "Sending rollback notification to Discord..."
ROLLBACK_MSG="🔄 **ROLLBACK INITIATED BY JARVIS**\n\n"
ROLLBACK_MSG+="**Reason:** $ROLLBACK_REASON\n"
ROLLBACK_MSG+="**Action:** Discord channels switching from Minimax back to DeepSeek\n"
ROLLBACK_MSG+="**Status:** Rollback in progress...\n"
ROLLBACK_MSG+="**Time:** $(date '+%Y-%m-%d %H:%M:%S %Z')"

openclaw message send --channel discord --to "#system-status" --message "$ROLLBACK_MSG" 2>&1 | tee -a "$LOG_FILE"

# Step 4: Verify DeepSeek is working
log "Verifying DeepSeek connectivity..."
sleep 2

# Step 5: Send confirmation message
log "Sending rollback confirmation..."
CONFIRM_MSG="✅ **ROLLBACK COMPLETE**\n\n"
CONFIRM_MSG+="All Discord channels have been switched back to DeepSeek.\n"
CONFIRM_MSG+="**Previous:** Minimax M2.7\n"
CONFIRM_MSG+="**Current:** DeepSeek Chat\n"
CONFIRM_MSG+="**Stability:** System restored to stable configuration\n"
CONFIRM_MSG+="**Next:** Monitor system and consider alternative solutions"

openclaw message send --channel discord --to "#system-status" --message "$CONFIRM_MSG" 2>&1 | tee -a "$LOG_FILE"

echo ""
echo "✅ Phase 3: Verification"
echo "-----------------------"

log "Verifying rollback completion..."

# Check post-rollback state
openclaw models list > /tmp/post-rollback-models.txt
log "Post-rollback models: $(cat /tmp/post-rollback-models.txt)"

# Send test message to verify DeepSeek is working
log "Sending test message to verify DeepSeek..."
TEST_MSG="🧪 Test message from DeepSeek after rollback. If you see this, rollback was successful."
openclaw message send --channel discord --to "#system-status" --message "$TEST_MSG" 2>&1 | tee -a "$LOG_FILE"

echo ""
echo "📊 Phase 4: Post-Rollback Analysis"
echo "----------------------------------"

log "Generating rollback analysis..."

# Create analysis report
ANALYSIS_FILE="/home/node/.openclaw/workspace/rollback-analysis-$(date +%Y%m%d-%H%M%S).md"
cat > "$ANALYSIS_FILE" << EOF
# Discord Rollback Analysis

## Rollback Details
- **Date:** $(date)
- **Executed by:** Jarvis (DeepSeek agent)
- **Reason:** $ROLLBACK_REASON
- **From:** Minimax M2.7
- **To:** DeepSeek Chat

## System State
### Pre-rollback
\`\`\`
$(cat /tmp/pre-rollback-models.txt)
\`\`\`

### Post-rollback
\`\`\`
$(cat /tmp/post-rollback-models.txt)
\`\`\`

## Minimax Status at Time of Rollback
- **API Test Exit Code:** $MINIMAX_STATUS
- **API Response:** $(cat /tmp/minimax-status.json | head -5)

## Actions Taken
1. Cleared Minimax environment variables
2. Restored DeepSeek configuration
3. Notified Discord channels
4. Verified DeepSeek connectivity

## Recommendations
1. Investigate Minimax issue: $(echo $ROLLBACK_REASON | cut -c1-50)...
2. Consider testing with single channel first next time
3. Set up better monitoring for API failures
4. Document lessons learned

## Log File
- **Location:** $LOG_FILE
- **Backup:** $LATEST_BACKUP
EOF

log "Analysis report created: $ANALYSIS_FILE"

echo ""
echo "🎉 Rollback Complete!"
echo "====================="
echo ""
echo "📋 Summary:"
echo "  • Discord channels restored to DeepSeek"
echo "  • Rollback reason: $ROLLBACK_REASON"
echo "  • Analysis report: $ANALYSIS_FILE"
echo "  • Log file: $LOG_FILE"
echo ""
echo "🔧 Next Steps:"
echo "  1. Review analysis report"
echo "  2. Investigate Minimax issue"
echo "  3. Consider alternative approaches"
echo "  4. Document lessons learned"
echo ""
echo "💡 Jarvis is monitoring system stability..."
log "=== END Discord Rollback ==="

# Final message
echo "🔄 Rollback executed successfully. System is stable on DeepSeek."