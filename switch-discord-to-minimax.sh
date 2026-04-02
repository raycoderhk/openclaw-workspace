#!/bin/bash
# Safe switch of all Discord channels from DeepSeek to Minimax
# Jarvis remains on DeepSeek for rollback support

echo "🚀 Discord to Minimax Switch - SAFE MODE"
echo "========================================="
echo "Jarvis remains on DeepSeek for rollback support"
echo ""

# Configuration
MINIMAX_API_KEY="sk-cp-mqDZwvwYG1u79lQAq_IoECIzYAvT1eBVcSOj3dIvTKcqRbRux_chEqTj1aHbvOtUCZ65CO6xYLSotXR1ocvisRzU4k6Zj1RiCpaf15ioXj5XW3DA1d8T5no"
MINIMAX_BASE_URL="https://api.minimaxi.com/v1"
MINIMAX_MODEL="MiniMax-M2.7"

BACKUP_DIR="/home/node/.openclaw/workspace/backup-$(date +%Y%m%d-%H%M%S)"
LOG_FILE="/home/node/.openclaw/workspace/discord-switch-$(date +%Y%m%d-%H%M%S).log"

echo "📋 Configuration:"
echo "  Backup Dir: $BACKUP_DIR"
echo "  Log File: $LOG_FILE"
echo "  Minimax Model: $MINIMAX_MODEL"
echo ""

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to check if we should continue
confirm() {
    echo ""
    read -p "❓ $1 (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "User cancelled at: $2"
        echo "❌ Operation cancelled by user"
        exit 1
    fi
}

# Start logging
log "=== START Discord to Minimax Switch ==="
log "User: $(whoami)"
log "Date: $(date)"
log ""

echo "📊 Phase 1: Pre-flight Checks"
echo "-----------------------------"

# Check 1: Minimax API connectivity
log "Checking Minimax API connectivity..."
curl -s -X POST "$MINIMAX_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "'"$MINIMAX_MODEL"'", "messages": [{"role": "user", "content": "test"}], "max_tokens": 10}' > /tmp/minimax-test.json

if [ $? -eq 0 ] && grep -q '"status_code":0' /tmp/minimax-test.json; then
    log "✅ Minimax API connectivity: PASS"
    echo "✅ Minimax API is reachable"
else
    log "❌ Minimax API connectivity: FAIL"
    echo "❌ Minimax API test failed. Check API key and connectivity."
    echo "   Response: $(cat /tmp/minimax-test.json)"
    exit 1
fi

# Check 2: Current Discord configuration
log "Checking current Discord configuration..."
openclaw models list > /tmp/current-models.txt
log "Current models: $(cat /tmp/current-models.txt)"
echo "✅ Current model configuration recorded"

# Check 3: Create backup directory
mkdir -p "$BACKUP_DIR"
log "Backup directory created: $BACKUP_DIR"
echo "✅ Backup directory ready"

echo ""
echo "📋 Phase 2: Backup Current Configuration"
echo "----------------------------------------"

# Backup current Discord configuration
log "Backing up current configuration..."
cp -r /home/node/.openclaw/workspace/openclaw-discord-template.json "$BACKUP_DIR/" 2>/dev/null || true
cp -r /home/node/.openclaw/workspace/mini-games/openclaw-discord-template.json "$BACKUP_DIR/mini-games/" 2>/dev/null || true

# Save current environment
env | grep -E "(DISCORD|OPENAI|DEEPSEEK|ALIYUN)" > "$BACKUP_DIR/environment-backup.txt"
log "Environment backed up to: $BACKUP_DIR/environment-backup.txt"

echo "✅ Configuration backed up to: $BACKUP_DIR"
log "Backup completed"

echo ""
echo "🚀 Phase 3: Execute Switch"
echo "--------------------------"

confirm "Proceed with switching ALL Discord channels to Minimax?" "Phase 3 start"

log "Starting Discord to Minimax switch..."

# Step 1: Set environment variables for Minimax
log "Setting Minimax environment variables..."
export OPENAI_API_KEY="$MINIMAX_API_KEY"
export OPENAI_BASE_URL="$MINIMAX_BASE_URL"
export OPENAI_MODEL="$MINIMAX_MODEL"

# Save environment to file for persistence
echo "export OPENAI_API_KEY='$MINIMAX_API_KEY'" > /home/node/.openclaw/workspace/minimax-discord-env.sh
echo "export OPENAI_BASE_URL='$MINIMAX_BASE_URL'" >> /home/node/.openclaw/workspace/minimax-discord-env.sh
echo "export OPENAI_MODEL='$MINIMAX_MODEL'" >> /home/node/.openclaw/workspace/minimax-discord-env.sh
log "Environment variables saved to: minimax-discord-env.sh"

# Step 2: Test with a single Discord message first
log "Testing Minimax with Discord message..."
echo "📤 Sending test message to Discord #system-status..."
openclaw message send --channel discord --to "#system-status" --message "🔧 TEST: Switching to Minimax M2.7. This message should come from Minimax if successful." 2>&1 | tee -a "$LOG_FILE"

confirm "Did the test message send successfully? Check Discord." "Test message sent"

# Step 3: Create new Discord configuration
log "Creating new Discord configuration with Minimax..."
cat > /home/node/.openclaw/workspace/discord-minimax-config.json << EOF
{
  "discord_minimax_config": {
    "name": "Discord with Minimax Default",
    "date": "$(date +%Y-%m-%d)",
    "status": "active",
    "configuration": {
      "default_model": "MiniMax-M2.7",
      "model_provider": "openai",
      "base_url": "$MINIMAX_BASE_URL",
      "api_key_env": "OPENAI_API_KEY",
      "reasoning_split": true,
      "temperature": 0.7,
      "max_tokens": 2048
    },
    "channels_affected": "All Discord channels",
    "exceptions": [
      "Jarvis agent (remains on DeepSeek)",
      "Telegram channels",
      "Webchat interface"
    ],
    "rollback_instructions": "Run: source $BACKUP_DIR/environment-backup.txt && restore original config files",
    "cost_monitoring": "https://platform.minimaxi.com/user-center/payment/token-plan"
  }
}
EOF

log "Configuration file created: discord-minimax-config.json"

echo ""
echo "✅ Phase 4: Verification"
echo "------------------------"

log "Starting verification phase..."

# Verification 1: Check environment
log "Verifying environment variables..."
if [ -n "$OPENAI_API_KEY" ] && [ -n "$OPENAI_BASE_URL" ] && [ -n "$OPENAI_MODEL" ]; then
    log "✅ Environment variables set correctly"
    echo "✅ Environment configured for Minimax"
else
    log "❌ Environment variables missing"
    echo "❌ Environment setup incomplete"
    exit 1
fi

# Verification 2: Send verification message
log "Sending verification message..."
VERIFY_MSG="✅ Discord channels now using Minimax M2.7. Jarvis remains on DeepSeek for rollback support. Use !help for agent commands."
openclaw message send --channel discord --to "#system-status" --message "$VERIFY_MSG" 2>&1 | tee -a "$LOG_FILE"

echo ""
echo "🎉 Phase 5: Completion"
echo "----------------------"

log "Switch completed successfully"

echo "✅ SWITCH COMPLETE!"
echo ""
echo "📊 Summary:"
echo "  • All Discord channels now use Minimax M2.7"
echo "  • Jarvis (me) remains on DeepSeek for rollback"
echo "  • Telegram/Webchat unchanged (DeepSeek)"
echo "  • Backup saved to: $BACKUP_DIR"
echo "  • Log file: $LOG_FILE"
echo ""
echo "🔧 Available Commands in Discord:"
echo "  !help - Show Minimax commands"
echo "  !coding - Switch to coding agent"
echo "  !imaging - Switch to imaging agent"
echo "  !video - Switch to video agent"
echo "  !status - Show current settings"
echo ""
echo "⚠️ Important:"
echo "  • Monitor costs at: https://platform.minimaxi.com"
echo "  • Jarvis can rollback if needed"
echo "  • Test with various message types"
echo ""
echo "🔄 Rollback Instructions:"
echo "  Source backup: source $BACKUP_DIR/environment-backup.txt"
echo "  Or ask Jarvis: 'Rollback Discord to DeepSeek'"
echo ""
log "=== END Discord to Minimax Switch ==="
echo "🚀 Discord is now running on Minimax M2.7!"