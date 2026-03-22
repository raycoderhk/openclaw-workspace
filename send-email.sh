#!/bin/bash

# Send email with technical spec attachment
# Using Gmail skill via Himalaya CLI

SUBJECT="📄 Quiz Battle Technical Specification - For LLM Review"
TO="raycoderhk@gmail.com"
BODY="Hi Raymond,

Attached is the complete technical specification for the Quiz Battle Mode system, formatted for LLM review.

**Document Includes:**
- System architecture overview
- Database schema (4 tables)
- 6 API endpoints with request/response examples
- Host & player flow diagrams
- 4 known issues with fixes and commit references
- Security considerations
- Kahoot mode specification
- 10 code review questions for LLM

**File:** BATTLE_TECHNICAL_SPEC.md
**Lines:** 500+
**Format:** Markdown (can be converted to PDF)

You can:
1. Open directly in GitHub
2. Convert to PDF using any MD→PDF tool
3. Send to LLM for code review

Let me know if you need any sections expanded or clarified!

Best,
Your AI Assistant"

# Check if Himalaya is configured
if ! command -v himalaya &> /dev/null; then
    echo "❌ Himalaya CLI not found"
    exit 1
fi

# Send email
echo "📧 Sending email to $TO..."
echo "$BODY" | himalaya send \
  --to "$TO" \
  --subject "$SUBJECT" \
  --attachment ./study-set-repo/BATTLE_TECHNICAL_SPEC.md

if [ $? -eq 0 ]; then
    echo "✅ Email sent successfully!"
else
    echo "❌ Failed to send email"
    exit 1
fi
