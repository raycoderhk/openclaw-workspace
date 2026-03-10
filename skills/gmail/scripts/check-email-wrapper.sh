#!/bin/bash
# Email Checker Wrapper - Runs email check and posts to Discord
# Call this from heartbeat or cron

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/home/node/.openclaw/workspace"

echo "📬 Running email check..."

# Run email checker with flags:
# --status: Include security status
# --only-new: Only post if there are NEW emails (silent if no new)
OUTPUT=$(python3 "$SCRIPT_DIR/email-checker.py" --status --only-new 2>&1)
EXIT_CODE=$?

# Extract Discord message
DISCORD_MSG=$(echo "$OUTPUT" | sed -n '/DISCORD_MESSAGE_START/,/DISCORD_MESSAGE_END/p' | sed '1d;$d')

# Check if there's nothing to post (no new emails)
if [ "$DISCORD_MSG" = "NO_NEW_EMAILS" ] || [ -z "$DISCORD_MSG" ]; then
    echo "✅ No new emails - staying silent (as requested)"
    exit 0
fi

if [ -z "$DISCORD_MSG" ]; then
    echo "❌ Failed to get email check output"
    echo "$OUTPUT"
    exit 1
fi

echo "✅ Email check complete"
echo "$DISCORD_MSG"

# Send to Discord #email channel
# Using message tool via OpenClaw
cd "$WORKSPACE"

# Channel ID for #email
EMAIL_CHANNEL_ID="channel:1478356227770683392"

# Check if urgent emails (exit code 1)
if [ $EXIT_CODE -eq 1 ]; then
    echo "🚨 URGENT emails detected!"
    # Send with high priority notification
    openclaw message send --target "$EMAIL_CHANNEL_ID" --message "$DISCORD_MSG"
else
    echo "📧 No urgent emails"
    # Send normal message
    openclaw message send --target "$EMAIL_CHANNEL_ID" --message "$DISCORD_MSG"
fi

echo "✅ Posted to Discord #email channel"
