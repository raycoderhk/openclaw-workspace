#!/bin/bash
# Simple test of Minimax API using curl

echo "🧪 Testing Minimax API with curl..."
echo "===================================="

API_KEY="sk-cp-mqDZwvwYG1u79lQAq_IoECIzYAvT1eBVcSOj3dIvTKcqRbRux_chEqTj1aHbvOtUCZ65CO6xYLSotXR1ocvisRzU4k6Zj1RiCpaf15ioXj5XW3DA1d8T5no"
BASE_URL="https://api.minimaxi.com/v1"
MODEL="MiniMax-M2.7"

echo "🔧 Configuration:"
echo "  API Key: ${API_KEY:0:10}...${API_KEY: -10}"
echo "  Base URL: $BASE_URL"
echo "  Model: $MODEL"

echo ""
echo "📤 Sending test request..."
curl -s -X POST "$BASE_URL/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "'"$MODEL"'",
    "reasoning_split": true,
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant. Respond in one short sentence."
      },
      {
        "role": "user",
        "content": "Say hello and confirm you are using Minimax."
      }
    ],
    "max_tokens": 100
  }'

echo ""
echo ""
echo "✅ Test complete!"
echo "If you see JSON response with 'choices', Minimax API is working."
echo "If you see error 1008, check quota allocation on platform.minimaxi.com"