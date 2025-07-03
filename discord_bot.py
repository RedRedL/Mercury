import os
import asyncio
import aiohttp
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from aiohttp_sse_client import sse_client
import json
import logging
from typing import List, Optional

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MinecraftBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!mc', intents=intents)
        
        # Configuration
        self.hermes_base_url = os.getenv('HERMES_API_BASE_URL', 'http://localhost:8080')
        self.hermes_api_key = os.getenv('HERMES_API_KEY', '')
        self.channel_id = int(os.getenv('DISCORD_CHANNEL_ID'))
        
        # HTTP session for API calls
        self.session: Optional[aiohttp.ClientSession] = None
        
        # SSE monitoring tasks
        self.player_events_task: Optional[asyncio.Task] = None
        self.chat_events_task: Optional[asyncio.Task] = None
        
    async def setup_hook(self):
        """Called when the bot is starting up"""
        # Create HTTP session
        self.session = aiohttp.ClientSession()
        
        # Start monitoring join/leave events and chat messages
        self.player_events_task = asyncio.create_task(self.monitor_player_events())
        self.chat_events_task = asyncio.create_task(self.monitor_chat_messages())
        
        logger.info("Bot setup completed")
    
    async def close(self):
        """Clean up when bot shuts down"""
        if self.player_events_task:
            self.player_events_task.cancel()
        
        if self.chat_events_task:
            self.chat_events_task.cancel()
        
        if self.session:
            await self.session.close()
        
        await super().close()
    
    async def on_ready(self):
        """Called when the bot has successfully connected to Discord"""
        logger.info(f'{self.user} has connected to Discord!')
        
        # Get the designated channel
        channel = self.get_channel(self.channel_id)
        if channel:
            embed = discord.Embed(
                title="🟢 Minecraft Bot Online",
                description="Bot is now monitoring the Minecraft server!",
                color=discord.Color.green()
            )
            await channel.send(embed=embed)
    
    async def on_message(self, message):
        """Handle messages from Discord users"""
        # Ignore messages from the bot itself
        if message.author == self.user:
            return
        
        # Only process messages from the designated channel
        if message.channel.id != self.channel_id:
            return
        
        # Process commands first
        await self.process_commands(message)
        
        # If it's not a command, try to forward to Minecraft
        if not message.content.startswith(self.command_prefix):
            await self.forward_to_minecraft(message)
    
    async def forward_to_minecraft(self, message):
        """Forward Discord message to Minecraft server via chat API"""
        try:
            headers = {'Content-Type': 'application/json'}
            if self.hermes_api_key:
                headers['Authorization'] = f'Bearer {self.hermes_api_key}'
            
            # Prepare the chat message payload
            payload = {
                'sender': f"[Discord] {message.author.display_name}",
                'message': message.content
            }
            
            logger.info(f"Forwarding to Minecraft: [{message.author.display_name}] {message.content}")
            
            async with self.session.post(
                f"{self.hermes_base_url}/chat/send",
                headers=headers,
                json=payload
            ) as response:
                if response.status == 200:
                    try:
                        await message.add_reaction("✅")
                    except discord.errors.Forbidden:
                        pass  # Bot doesn't have permission to add reactions
                    logger.info("Message successfully sent to Minecraft")
                else:
                    try:
                        await message.add_reaction("❌")
                    except discord.errors.Forbidden:
                        pass
                    logger.error(f"Failed to send message to Minecraft: HTTP {response.status}")
                    
        except Exception as e:
            logger.error(f"Error forwarding message to Minecraft: {e}")
            try:
                await message.add_reaction("❌")
            except discord.errors.Forbidden:
                pass
    
    async def forward_from_minecraft(self, player_name: str, chat_message: str):
        """Forward Minecraft chat message to Discord (placeholder for future chat API)"""
        channel = self.get_channel(self.channel_id)
        if channel:
            embed = discord.Embed(
                description=f"**{player_name}:** {chat_message}",
                color=discord.Color.blue()
            )
            embed.set_footer(text="Minecraft Chat")
            await channel.send(embed=embed)
    
    async def get_player_count(self) -> Optional[int]:
        """Get the current number of online players"""
        try:
            headers = {}
            if self.hermes_api_key:
                headers['Authorization'] = f'Bearer {self.hermes_api_key}'
            
            async with self.session.get(
                f"{self.hermes_base_url}/players/count",
                headers=headers
            ) as response:
                if response.status == 200:
                    count_text = await response.text()
                    return int(count_text.strip())
                else:
                    logger.error(f"Failed to get player count: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error getting player count: {e}")
            return None
    
    async def get_player_names(self) -> Optional[List[str]]:
        """Get the list of online player names"""
        try:
            headers = {}
            if self.hermes_api_key:
                headers['Authorization'] = f'Bearer {self.hermes_api_key}'
            
            async with self.session.get(
                f"{self.hermes_base_url}/players/names",
                headers=headers
            ) as response:
                if response.status == 200:
                    names_text = await response.text()
                    if names_text.strip():
                        return [name.strip() for name in names_text.split(',')]
                    else:
                        return []
                else:
                    logger.error(f"Failed to get player names: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error getting player names: {e}")
            return None
    
    async def monitor_player_events(self):
        """Monitor join/leave events via SSE"""
        while True:
            try:
                headers = {}
                if self.hermes_api_key:
                    headers['Authorization'] = f'Bearer {self.hermes_api_key}'
                
                logger.info("Connecting to SSE stream for player events...")
                
                async with sse_client.EventSource(
                    f"{self.hermes_base_url}/players/connections",
                    headers=headers
                ) as event_source:
                    async for event in event_source:
                        if event.data:
                            await self.handle_player_event(event.data)
                        
            except Exception as e:
                logger.error(f"SSE connection error: {e}")
                logger.info("Retrying SSE connection in 30 seconds...")
                await asyncio.sleep(30)
    
    async def handle_player_event(self, event_data: str):
        """Handle player join/leave events from SSE stream"""
        try:
            channel = self.get_channel(self.channel_id)
            if not channel:
                return
            
            # Parse the event data
            event_text = event_data.strip()
            logger.info(f"Received player event: {event_text}")
            
            if " has joined!" in event_text:
                player_name = event_text.replace(" has joined!", "")
                embed = discord.Embed(
                    title="🟢 Player Joined",
                    description=f"**{player_name}** joined the server",
                    color=discord.Color.green()
                )
                await channel.send(embed=embed)
                
            elif " has left." in event_text:
                player_name = event_text.replace(" has left.", "")
                embed = discord.Embed(
                    title="🔴 Player Left",
                    description=f"**{player_name}** left the server",
                    color=discord.Color.red()
                )
                await channel.send(embed=embed)
                
        except Exception as e:
            logger.error(f"Error handling player event: {e}")

    async def monitor_chat_messages(self):
        """Monitor Minecraft chat messages via SSE"""
        while True:
            try:
                headers = {}
                if self.hermes_api_key:
                    headers['Authorization'] = f'Bearer {self.hermes_api_key}'
                
                logger.info("Connecting to SSE stream for chat messages...")
                
                async with sse_client.EventSource(
                    f"{self.hermes_base_url}/chat/stream",
                    headers=headers
                ) as event_source:
                    async for event in event_source:
                        if event.data:
                            await self.handle_chat_event(event.data)
                        
            except Exception as e:
                logger.error(f"Chat SSE connection error: {e}")
                logger.info("Retrying chat SSE connection in 30 seconds...")
                await asyncio.sleep(30)
    
    async def handle_chat_event(self, event_data: str):
        """Handle chat messages from SSE stream"""
        try:
            channel = self.get_channel(self.channel_id)
            if not channel:
                return
            
            # Parse the event data (expecting JSON format)
            try:
                chat_data = json.loads(event_data)
                player_name = chat_data.get('player', 'Unknown')
                message = chat_data.get('message', '')
                
                # Don't forward messages that came from Discord (to prevent loops)
                if message and not player_name.startswith('[Discord]'):
                    logger.info(f"Received chat from Minecraft: [{player_name}] {message}")
                    await self.forward_from_minecraft(player_name, message)
                    
            except json.JSONDecodeError:
                # If it's not JSON, try to parse as plain text format
                # Expected format: "PlayerName: message content"
                if ':' in event_data:
                    parts = event_data.split(':', 1)
                    player_name = parts[0].strip()
                    message = parts[1].strip()
                    
                    # Don't forward messages that came from Discord (to prevent loops)
                    if message and not player_name.startswith('[Discord]'):
                        logger.info(f"Received chat from Minecraft: [{player_name}] {message}")
                        await self.forward_from_minecraft(player_name, message)
                        
        except Exception as e:
            logger.error(f"Error handling chat event: {e}")

# Bot commands
@commands.command(name='players', aliases=['online', 'who'])
async def players_command(ctx):
    """Display current online players"""
    bot = ctx.bot
    
    # Get player count and names
    count = await bot.get_player_count()
    names = await bot.get_player_names()
    
    if count is None or names is None:
        embed = discord.Embed(
            title="❌ Error",
            description="Could not retrieve player information from the server.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Create embed with player information
    embed = discord.Embed(
        title="🎮 Online Players",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="Player Count",
        value=f"{count} player{'s' if count != 1 else ''} online",
        inline=False
    )
    
    if names:
        players_list = "\n".join([f"• {name}" for name in names])
        embed.add_field(
            name="Players",
            value=players_list,
            inline=False
        )
    else:
        embed.add_field(
            name="Players",
            value="No players online",
            inline=False
        )
    
    await ctx.send(embed=embed)

@commands.command(name='status', aliases=['server'])
async def status_command(ctx):
    """Check server status and basic info"""
    bot = ctx.bot
    
    try:
        # Test API connectivity
        headers = {}
        if bot.hermes_api_key:
            headers['Authorization'] = f'Bearer {bot.hermes_api_key}'
        
        async with bot.session.get(
            f"{bot.hermes_base_url}/players/count",
            headers=headers
        ) as response:
            if response.status == 200:
                count = int((await response.text()).strip())
                
                embed = discord.Embed(
                    title="🟢 Server Status",
                    description="Server is online and responding",
                    color=discord.Color.green()
                )
                embed.add_field(
                    name="Players Online",
                    value=f"{count} player{'s' if count != 1 else ''}",
                    inline=True
                )
                embed.add_field(
                    name="API Endpoint",
                    value=bot.hermes_base_url,
                    inline=True
                )
                
            else:
                embed = discord.Embed(
                    title="🟡 Server Status",
                    description=f"Server responded with status code: {response.status}",
                    color=discord.Color.orange()
                )
    
    except Exception as e:
        embed = discord.Embed(
            title="🔴 Server Status",
            description="Server is offline or unreachable",
            color=discord.Color.red()
        )
        embed.add_field(
            name="Error",
            value=str(e),
            inline=False
        )
    
    await ctx.send(embed=embed)

# Add commands to the bot
async def main():
    """Main function to run the bot"""
    bot = MinecraftBot()
    bot.add_command(players_command)
    bot.add_command(status_command)
    
    # Get Discord bot token
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error("DISCORD_BOT_TOKEN not found in environment variables")
        return
    
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main()) 