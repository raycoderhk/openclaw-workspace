# 🦞 Minimax M2.7 Agents Setup Guide

**Date:** March 26, 2026  
**Plan:** M2.7 Token Plan Plus (179 RMB/year - 90% discount)  
**Status:** ✅ Models configured, ready for use

---

## 📋 Available Agents

### 1. **Minimax Coding Agent** (`minimax-coding-agent.json`)
- **Model:** `MiniMax-M2.7` (OpenAI-compatible)
- **Best for:** Programming, debugging, technical writing, code review
- **Temperature:** 0.2 (precise, deterministic)
- **Context:** 204.8K tokens
- **Provider:** `openai` (uses OpenAI-compatible API)

### 2. **Minimax Imaging Agent** (`minimax-imaging-agent.json`)
- **Model:** `MiniMax-M2.7` (OpenAI-compatible, vision capabilities included)
- **Best for:** Image analysis, visual QA, object detection, scene description
- **Temperature:** 0.7 (creative, descriptive)
- **Context:** 4K tokens
- **Provider:** `openai` (uses OpenAI-compatible API)

### 3. **Minimax Video Agent** (`minimax-video-agent.json`)
- **Model:** `MiniMax-M2.7` (OpenAI-compatible)
- **Best for:** Script writing, storyboarding, video planning, creative storytelling
- **Temperature:** 0.8 (creative, engaging)
- **Context:** 204.8K tokens
- **Provider:** `openai` (uses OpenAI-compatible API)

### 4. **Minimax General Agent** (`minimax-m2.7-agent.json`)
- **Model:** `MiniMax-M2.7` (OpenAI-compatible)
- **Best for:** General chat, analysis, summarization, translation
- **Temperature:** 0.7 (balanced)
- **Context:** 204.8K tokens
- **Provider:** `openai` (uses OpenAI-compatible API)

### Alternative Models (Tested & Working):
- `MiniMax-M2.5` - Balanced performance
- `MiniMax-M2.5-highspeed` - Faster responses
- `MiniMax-M2` - Basic model (responds as "gpt-4o-mini")

---

## 🚀 Quick Start

### Option 1: Manual Session Spawn
```bash
# Spawn coding agent
openclaw sessions spawn --agent minimax-coding-agent.json --task "Write Python code for web scraping"

# Spawn imaging agent  
openclaw sessions spawn --agent minimax-imaging-agent.json --task "Analyze this image and describe what you see"

# Spawn video agent
openclaw sessions spawn --agent minimax-video-agent.json --task "Create a script for a 5-minute tutorial video"
```

### Option 2: Programmatic Use
```python
from openclaw import sessions

# Spawn coding agent
coding_session = sessions.spawn(
    agent="minimax-coding-agent.json",
    task="Debug this Python function",
    label="coding-debug"
)

# Spawn imaging agent
imaging_session = sessions.spawn(
    agent="minimax-imaging-agent.json", 
    task="Describe the nutritional content in this food image",
    label="food-analysis"
)
```

### Option 3: Direct API Calls (Advanced)
```python
import requests
import os

api_key = os.getenv("MINIMAX_API_KEY")  # From vision/config.env

response = requests.post(
    "https://api.minimaxi.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "model": "abab6.5-chat",
        "messages": [{"role": "user", "content": "Write a Python function"}],
        "temperature": 0.2
    }
)
```

---

## 💰 Cost Management

### Pricing (Per Million Tokens)
| Service | Input | Output | Notes |
|---------|-------|--------|-------|
| **Text Models** | $0.30 | $1.20 | Best value, use for most tasks |
| **Vision Models** | $0.30 | $1.20 | Same pricing as text |
| **Image Generation** | Separate | Separate | Higher cost, use sparingly |
| **Voice Synthesis** | Separate | Separate | Specialized use only |

### Cost-Effective Strategy
1. **Primary:** Use text models for 90% of tasks
2. **Secondary:** Use vision models only when needed
3. **Tertiary:** Use image/voice generation for specific projects
4. **Monitor:** Keep track of usage in Minimax dashboard

### Estimated Monthly Costs
| Usage Level | Text Tokens | Vision Tokens | Estimated Cost |
|-------------|-------------|---------------|----------------|
| **Light** | 1M in, 0.5M out | 0.5M total | ~$0.90/month |
| **Medium** | 5M in, 2M out | 2M total | ~$3.90/month |
| **Heavy** | 20M in, 10M out | 5M total | ~$18.00/month |

---

## 🔧 Configuration Details

### API Key Location
```
/home/node/.openclaw/workspace/skills/vision/config.env
MINIMAX_API_KEY=sk-cp-... (your key here)
```

### Model Endpoints
- **Text:** `https://api.minimaxi.com/v1/chat/completions`
- **Vision:** `https://api.minimaxi.com/v1/chat/completions` (with images)
- **Image Gen:** Separate endpoint (not configured yet)
- **Voice Synth:** Separate endpoint (not configured yet)

### Available Models
```
Text: abab6-chat, abab6.5-chat, abab6.5s-chat
Vision: abab6.5s-vision
Image Gen: Available but separate billing
Voice: Available but separate billing
```

---

## 🎯 Use Case Examples

### Coding Tasks
```bash
# Debug Python code
openclaw sessions spawn --agent minimax-coding-agent.json --task "Debug this function: def calculate_sum(numbers): return sum(numbers)"

# Write API integration
openclaw sessions spawn --agent minimax-coding-agent.json --task "Create FastAPI endpoint for user authentication"

# Code review
openclaw sessions spawn --agent minimax-coding-agent.json --task "Review this React component for best practices"
```

### Imaging Tasks
```bash
# Food analysis (nutritionist app)
openclaw sessions spawn --agent minimax-imaging-agent.json --task "Analyze this food image and estimate calories"

# Document processing
openclaw sessions spawn --agent minimax-imaging-agent.json --task "Extract text and information from this scanned document"

# Creative description
openclaw sessions spawn --agent minimax-imaging-agent.json --task "Describe this landscape photo in poetic terms"
```

### Video Tasks
```bash
# Tutorial script
openclaw sessions spawn --agent minimax-video-agent.json --task "Write script for 10-minute OpenClaw tutorial"

# Storyboard
openclaw sessions spawn --agent minimax-video-agent.json --task "Create storyboard for product demo video"

# Content planning
openclaw sessions spawn --agent minimax-video-agent.json --task "Plan YouTube content calendar for AI tools channel"
```

---

## 🛠️ Testing & Validation

### Run Configuration Test
```bash
cd /home/node/.openclaw/workspace/agents
python3 test-all-minimax-models.py
```

### Test Individual Models
```bash
# Test text model
python3 test_minimax_m2.7.py

# Test vision model (via nutritionist app)
cd ../nutritionist-app
python3 server.py
```

### Verify API Key
```bash
# Check API key is set
grep MINIMAX_API_KEY ../skills/vision/config.env

# Test API connectivity
python3 simple_test.py
```

---

## ⚠️ Important Notes

### 1. **Separate Billing**
- Text/Vision: Combined billing (same API key)
- Image Generation: Separate service, separate billing
- Voice Synthesis: Separate service, separate billing
- **Monitor usage in Minimax dashboard regularly**

### 2. **API Key Security**
- API key stored in `vision/config.env`
- File marked with `⚠️ DO NOT commit to GitHub`
- Never share or expose the API key

### 3. **Model Selection**
- Use `abab6.5-chat` for complex tasks (coding, analysis)
- Use `abab6.5s-chat` for quick responses
- Use `abab6.5s-vision` for image tasks
- Vision model already working in nutritionist app

### 4. **Cost Control**
- Set up usage alerts in Minimax dashboard
- Prefer text models over image generation
- Batch similar tasks to reduce API calls
- Use caching when possible

---

## 🔄 Integration with Existing Systems

### Nutritionist App
- Already using `abab6.5s-vision` model
- API key: `MINIMAX_API_KEY` from `vision/config.env`
- Working successfully since March 25

### OpenClaw Skills
- Vision skill configured for Minimax
- Can extend to other skills (coding, writing, etc.)
- Use `sessions_spawn` to invoke specialized agents

### Kanban Board
- Add tasks for Minimax model testing
- Track usage and costs
- Create projects for different agent types

---

## 🚨 Troubleshooting

### Common Issues

1. **"insufficient balance" error**
   - Check Minimax dashboard for quota allocation
   - Text generation quota may need activation
   - Contact Minimax support if needed

2. **API key not working**
   - Verify key in `vision/config.env`
   - Check for typos or missing characters
   - Test with `simple_test.py`

3. **Model not recognized**
   - Verify model name in agent configuration
   - Check Minimax documentation for available models
   - Use `test_model_names.py` to validate

4. **High costs**
   - Switch to text-only models
   - Reduce image generation usage
   - Implement response caching

### Support Resources
- Minimax Dashboard: https://platform.minimaxi.com
- Documentation: https://api.minimaxi.com/document
- Support: Contact via dashboard or email

---

## 📈 Next Steps

### Short Term (This Week)
1. ✅ Configure all Minimax agents
2. ✅ Test text models with API calls
3. ✅ Verify vision model continues working
4. Set up cost monitoring dashboard
5. Create usage examples for each agent

### Medium Term (Next Month)
1. Integrate with OpenClaw cron jobs
2. Set up automated testing for agents
3. Create specialized workflows
4. Monitor and optimize costs
5. Document best practices

### Long Term (Ongoing)
1. Expand to image generation (if needed)
2. Add voice synthesis capabilities
3. Create multi-agent workflows
4. Optimize for specific use cases
5. Share experiences with OpenClaw community

---

## 🎉 Success Metrics

### Technical
- ✅ All agent configurations created
- ✅ API key validated and working
- ✅ Vision model already in production use
- ✅ Test scripts available

### Financial
- ✅ 90% discount secured (179 RMB/year)
- ✅ Cost-effective model selection
- ✅ Usage monitoring plan in place
- ✅ Budget control strategies defined

### Operational
- ✅ Ready for immediate use
- ✅ Clear documentation available
- ✅ Troubleshooting guide prepared
- ✅ Integration path defined

---

**🦞 Summary:** You now have a complete Minimax M2.7 agent ecosystem ready for use. The 179 RMB/year plan gives you access to state-of-the-art models at 90% discount. Start with text models for most tasks, use vision when needed, and expand to image/voice generation as required.

**Next Action:** Run `python3 test-all-minimax-models.py` to verify everything is working, then start using the agents with `sessions_spawn`!

*Last updated: March 26, 2026*