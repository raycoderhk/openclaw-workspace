# 🦞 Minimax Agents - Example Usage

## Quick Examples for OpenClaw

### 1. Spawn Coding Agent for Debugging
```python
# In your OpenClaw session
sessions_spawn(
    task="Debug this Python function that's supposed to calculate factorial but returns wrong results:\n\ndef factorial(n):\n    result = 1\n    for i in range(1, n):\n        result *= i\n    return result\n\nWhat's wrong and how to fix it?",
    label="debug-factorial",
    agentId="minimax-coding-agent"
)
```

### 2. Spawn Imaging Agent for Food Analysis
```python
# For nutritionist app integration
sessions_spawn(
    task="Analyze this food image (pizza). Describe the ingredients, estimate calories, and suggest healthier alternatives.",
    label="food-analysis-pizza",
    agentId="minimax-imaging-agent"
)
```

### 3. Spawn Video Agent for Content Creation
```python
# For YouTube/TikTok content planning
sessions_spawn(
    task="Create a script for a 3-minute TikTok video about '5 OpenClaw features you didn't know about'. Include hook, main points, and call-to-action.",
    label="tiktok-script-openclaw",
    agentId="minimax-video-agent"
)
```

### 4. Spawn General Agent for Analysis
```python
# For document analysis or research
sessions_spawn(
    task="Analyze this technical document about API rate limiting. Summarize key points and suggest implementation strategies.",
    label="api-analysis",
    agentId="minimax-m2.7-agent"
)
```

## Real-World Use Cases

### Use Case 1: Code Review Workflow
```python
# 1. Get code from GitHub
code_to_review = """
def process_data(data):
    results = []
    for item in data:
        if item['status'] == 'active':
            processed = transform(item)
            results.append(processed)
    return results
"""

# 2. Spawn coding agent for review
sessions_spawn(
    task=f"Review this Python code for:\n1. Performance issues\n2. Error handling\n3. Code style\n4. Security concerns\n\nCode:\n{code_to_review}",
    label="code-review-python",
    agentId="minimax-coding-agent"
)
```

### Use Case 2: Image-Based Nutrition Analysis
```python
# For the nutritionist app - automated analysis
sessions_spawn(
    task="You are a nutritionist AI. Analyze the attached food image (burger and fries). Provide:\n1. Estimated calories\n2. Macronutrient breakdown\n3. Health score (1-10)\n4. Healthier alternatives\n5. Meal planning suggestions",
    label="nutrition-analysis-burger",
    agentId="minimax-imaging-agent"
)
```

### Use Case 3: Video Script Automation
```python
# Automated content creation for social media
topics = ["AI coding assistants", "OpenClaw setup", "Minimax models", "Automation workflows"]

for topic in topics:
    sessions_spawn(
        task=f"Create a YouTube Shorts script (60 seconds) about '{topic}'. Include:\n- Hook (first 5 seconds)\n- 3 main points\n- Call to action\n- Hashtags",
        label=f"youtube-shorts-{topic.lower().replace(' ', '-')}",
        agentId="minimax-video-agent"
    )
```

## Integration with Existing Systems

### With Kanban Board
```python
# When a new coding task is added to kanban
if new_task["type"] == "coding":
    sessions_spawn(
        task=f"Help with this coding task: {new_task['description']}",
        label=f"kanban-coding-{new_task['id']}",
        agentId="minimax-coding-agent"
    )
```

### With Email Processing
```python
# When email contains technical question
if email_contains_technical_question:
    sessions_spawn(
        task=f"Answer this technical question from email:\n{email_content}",
        label=f"email-tech-support-{email_id}",
        agentId="minimax-coding-agent"
    )
```

### With Discord Community
```python
# When Discord message needs technical answer
if discord_message_needs_technical_response:
    sessions_spawn(
        task=f"Provide helpful technical answer for this Discord question:\n{discord_question}",
        label=f"discord-tech-{message_id}",
        agentId="minimax-coding-agent"
    )
```

## Cost-Effective Usage Patterns

### Pattern 1: Batch Processing
```python
# Instead of multiple small calls, batch similar tasks
coding_tasks = [
    "Fix bug in login function",
    "Optimize database query",
    "Add error handling to API endpoint"
]

for task in coding_tasks:
    sessions_spawn(
        task=task,
        label=f"batch-coding-{hash(task)}",
        agentId="minimax-coding-agent"
    )
```

### Pattern 2: Cached Responses
```python
# Cache common responses to reduce API calls
common_questions = {
    "how to setup openclaw": "cached_response_1",
    "minimax api key error": "cached_response_2",
    "nutritionist app setup": "cached_response_3"
}

if user_question in common_questions:
    use_cached_response(common_questions[user_question])
else:
    sessions_spawn(
        task=user_question,
        label=f"new-question-{timestamp}",
        agentId="minimax-m2.7-agent"
    )
```

### Pattern 3: Progressive Detail
```python
# Start simple, add detail only if needed
# First: Simple answer
sessions_spawn(
    task="Explain rate limiting in 2 sentences",
    label="rate-limiting-simple",
    agentId="minimax-m2.7-agent"
)

# Only if user asks for more detail:
sessions_spawn(
    task="Provide detailed implementation of rate limiting with code examples",
    label="rate-limiting-detailed",
    agentId="minimax-coding-agent"
)
```

## Monitoring and Optimization

### Track Usage
```python
# Simple usage tracking
usage_log = {
    "timestamp": "2026-03-26T09:45:00Z",
    "agent": "minimax-coding-agent",
    "task_length": 150,  # characters
    "estimated_tokens": 50,
    "cost_estimate": 0.00006  # USD
}
```

### Cost Alerts
```python
# Set up cost thresholds
DAILY_BUDGET = 0.50  # USD
MONTHLY_BUDGET = 15.00  # USD

if daily_cost > DAILY_BUDGET:
    send_alert("Minimax daily budget exceeded")
    
if monthly_cost > MONTHLY_BUDGET:
    send_alert("Minimax monthly budget exceeded")
    # Switch to cheaper models or reduce usage
```

## Ready-to-Use Templates

### Template 1: Code Debugging
```python
sessions_spawn(
    task="""Debug this code:
{code}

Errors encountered:
{errors}

Expected behavior:
{expected}

Please provide:
1. What's wrong
2. Fixed code
3. Explanation of fix""",
    label="code-debug-{filename}",
    agentId="minimax-coding-agent"
)
```

### Template 2: Image Analysis
```python
sessions_spawn(
    task="""Analyze this image:
{image_description_or_url}

Please provide:
1. What you see
2. Key elements identified
3. Context or meaning
4. Any concerns or recommendations""",
    label="image-analysis-{image_type}",
    agentId="minimax-imaging-agent"
)
```

### Template 3: Content Creation
```python
sessions_spawn(
    task="""Create content about:
{topic}

Format: {format} (blog post, video script, social media post)
Length: {length}
Tone: {tone}
Target audience: {audience}

Please include:
1. Title/hook
2. Main points
3. Conclusion/call-to-action
4. SEO keywords/hashtags""",
    label="content-{topic}-{format}",
    agentId="minimax-video-agent"  # or minimax-m2.7-agent
)
```

## Getting Started Right Now

### Try These Immediately:
```python
# 1. Quick coding help
sessions_spawn(
    task="Write a Python function to validate email addresses",
    label="test-email-validation",
    agentId="minimax-coding-agent"
)

# 2. Simple analysis
sessions_spawn(
    task="What are the benefits of using Minimax M2.7 over other models?",
    label="test-minimax-analysis",
    agentId="minimax-m2.7-agent"
)

# 3. Creative task
sessions_spawn(
    task="Write a short story about an AI assistant helping a developer",
    label="test-creative-writing",
    agentId="minimax-video-agent"
)
```

## Need Help?

### Common Issues & Solutions:
1. **Agent not found**: Check `agentId` matches JSON filename (without .json)
2. **API errors**: Verify `MINIMAX_API_KEY` in vision/config.env
3. **Cost concerns**: Start with text-only tasks, monitor usage
4. **Slow responses**: Use `abab6.5s-chat` for faster responses

### Support:
- Check `MINIMAX_AGENTS_SETUP.md` for detailed setup
- Run `test-all-minimax-models.py` to verify configuration
- Monitor usage in Minimax dashboard: https://platform.minimaxi.com

---

**🎯 Start Simple:** Try one agent today, monitor costs, expand as needed!
**💰 Remember:** Text models are most cost-effective, use them for 90% of tasks.
**🚀 Have Fun:** Experiment with different agents for different tasks!