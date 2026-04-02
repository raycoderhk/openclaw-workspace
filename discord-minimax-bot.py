#!/usr/bin/env python3
"""
Discord bot for Minimax-only channel.
This bot defaults to using Minimax M2.7 models in a specific Discord channel.
"""

import os
import sys
import json
import asyncio
import discord
from discord.ext import commands
from pathlib import Path

# Load configuration
config_path = Path(__file__).parent / "discord-minimax-channel-config.json"
with open(config_path, 'r') as f:
    config = json.load(f)

# Set environment variables for Minimax
os.environ["OPENAI_API_KEY"] = config["channel_config"]["environment_variables"]["OPENAI_API_KEY"]
os.environ["OPENAI_BASE_URL"] = config["channel_config"]["environment_variables"]["OPENAI_BASE_URL"]
os.environ["OPENAI_MODEL"] = config["channel_config"]["environment_variables"]["OPENAI_MODEL"]

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    help_command=None
)

# Agent mapping
AGENT_MAP = {
    "default": "minimax-m2.7-agent",
    "coding": "minimax-coding-agent",
    "imaging": "minimax-imaging-agent",
    "video": "minimax-video-agent",
    "general": "minimax-m2.7-agent"
}

# User session tracking
user_sessions = {}

class MinimaxSession:
    """Track user sessions and agent preferences"""
    def __init__(self, user_id):
        self.user_id = user_id
        self.current_agent = "minimax-m2.7-agent"
        self.message_history = []
        self.token_count = 0
        
    def switch_agent(self, agent_type):
        """Switch to a different Minimax agent"""
        if agent_type in AGENT_MAP:
            self.current_agent = AGENT_MAP[agent_type]
            return f"Switched to {agent_type} agent ({self.current_agent})"
        return f"Unknown agent type. Available: {', '.join(AGENT_MAP.keys())}"
    
    def add_message(self, role, content):
        """Add message to history"""
        self.message_history.append({"role": role, "content": content})
        # Keep only last 10 messages to manage context
        if len(self.message_history) > 10:
            self.message_history = self.message_history[-10:]

@bot.event
async def on_ready():
    """Bot is ready"""
    print(f'✅ Minimax Discord Bot is ready!')
    print(f'🤖 Logged in as: {bot.user.name}')
    print(f'🆔 Bot ID: {bot.user.id}')
    print(f'🔧 Default model: {os.environ.get("OPENAI_MODEL", "MiniMax-M2.7")}')
    print(f'📊 Available agents: {", ".join(AGENT_MAP.keys())}')
    print('=' * 50)

@bot.event
async def on_message(message):
    """Handle incoming messages"""
    # Ignore bot's own messages
    if message.author == bot.user:
        return
    
    # Check if this is the minimax channel
    channel_name = message.channel.name if hasattr(message.channel, 'name') else "unknown"
    
    # For now, respond in any channel, but you can restrict to specific channels
    # if channel_name != "minimax-chat":
    #     return
    
    # Get or create user session
    user_id = str(message.author.id)
    if user_id not in user_sessions:
        user_sessions[user_id] = MinimaxSession(user_id)
    
    session = user_sessions[user_id]
    
    # Check for commands
    if message.content.startswith('!'):
        await handle_command(message, session)
        return
    
    # Regular message - process with Minimax
    await process_with_minimax(message, session)

async def handle_command(message, session):
    """Handle bot commands"""
    command = message.content.lower().strip()
    
    if command == '!help':
        help_text = """
**🤖 Minimax Discord Bot Commands:**
`!help` - Show this help message
`!coding` - Switch to coding agent (for programming tasks)
`!imaging` - Switch to imaging agent (for image analysis)
`!video` - Switch to video agent (for scripts/storyboarding)
`!general` - Switch to general agent (default)
`!status` - Show current agent and usage
`!reset` - Reset conversation history
`!models` - Show available Minimax models
"""
        await message.channel.send(help_text)
    
    elif command == '!coding':
        response = session.switch_agent("coding")
        await message.channel.send(f"✅ {response}")
    
    elif command == '!imaging':
        response = session.switch_agent("imaging")
        await message.channel.send(f"✅ {response}")
    
    elif command == '!video':
        response = session.switch_agent("video")
        await message.channel.send(f"✅ {response}")
    
    elif command == '!general':
        response = session.switch_agent("general")
        await message.channel.send(f"✅ {response}")
    
    elif command == '!status':
        status = f"""
**📊 Current Status:**
• Agent: {session.current_agent}
• Message history: {len(session.message_history)} messages
• User: {message.author.name}
• Model: {os.environ.get('OPENAI_MODEL', 'MiniMax-M2.7')}
"""
        await message.channel.send(status)
    
    elif command == '!reset':
        session.message_history = []
        await message.channel.send("✅ Conversation history reset")
    
    elif command == '!models':
        models_info = """
**🦞 Available Minimax Models:**
• `MiniMax-M2.7` - Primary model (default)
• `MiniMax-M2.5` - Balanced performance
• `MiniMax-M2.5-highspeed` - Faster responses
• `MiniMax-M2` - Basic model

**Note:** Currently using: MiniMax-M2.7
"""
        await message.channel.send(models_info)
    
    else:
        await message.channel.send(f"❓ Unknown command. Use `!help` for available commands.")

async def process_with_minimax(message, session):
    """Process message with Minimax API"""
    try:
        # Add user message to history
        session.add_message("user", message.content)
        
        # Show typing indicator
        async with message.channel.typing():
            # In a real implementation, you would call the Minimax API here
            # For now, we'll simulate a response
            
            # Simulate API call delay
            await asyncio.sleep(1)
            
            # Determine response based on agent type
            agent_type = session.current_agent
            
            if "coding" in agent_type:
                response = f"**🤖 [Minimax Coding Agent]:**\nI'll help with your coding question: '{message.content}'\n\nFor actual implementation, this would call the Minimax API with your coding agent configuration."
            elif "imaging" in agent_type:
                response = f"**🤖 [Minimax Imaging Agent]:**\nI'll analyze your image-related query: '{message.content}'\n\nFor actual implementation, this would call the Minimax API with vision capabilities."
            elif "video" in agent_type:
                response = f"**🤖 [Minimax Video Agent]:**\nI'll help with your video/script request: '{message.content}'\n\nFor actual implementation, this would call the Minimax API with creative writing settings."
            else:
                response = f"**🤖 [Minimax M2.7]:**\nI received your message: '{message.content}'\n\nThis channel is configured to use Minimax M2.7 by default. Use commands like `!coding` for specialized agents."
            
            # Add bot response to history
            session.add_message("assistant", response)
            
            # Send response
            await message.channel.send(response)
            
    except Exception as e:
        error_msg = f"❌ Error processing message: {str(e)}"
        await message.channel.send(error_msg)
        print(f"Error: {e}")

def main():
    """Main function to run the bot"""
    # Get Discord token from environment or config
    discord_token = os.environ.get("DISCORD_BOT_TOKEN")
    
    if not discord_token:
        print("❌ DISCORD_BOT_TOKEN environment variable not set")
        print("💡 Set it with: export DISCORD_BOT_TOKEN='your-bot-token-here'")
        sys.exit(1)
    
    print("🚀 Starting Minimax Discord Bot...")
    print(f"🔧 Configuration loaded from: {config_path}")
    print(f"🤖 Bot will default to: {os.environ.get('OPENAI_MODEL')}")
    print(f"🌐 API Base URL: {os.environ.get('OPENAI_BASE_URL')}")
    
    # Run the bot
    bot.run(discord_token)

if __name__ == "__main__":
    main()