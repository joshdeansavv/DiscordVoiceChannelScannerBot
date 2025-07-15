"""
24/7 junctionnow radio relay
discord.py ≥2.4
"""

import os
import asyncio
import logging
from typing import Optional
import traceback
import time
import random

import discord
from discord.ext import commands, tasks
import discord.opus

# Try to load Opus explicitly
if not discord.opus.is_loaded():
    # Try to load opus from common locations
    import platform
    system = platform.system()
    
    if system == "Darwin":  # macOS
        opus_paths = [
            "/opt/homebrew/Cellar/opus/1.5.2/lib/libopus.0.dylib",  # Found path
            "/opt/homebrew/lib/libopus.dylib",  # Apple Silicon Homebrew
            "/usr/local/lib/libopus.dylib",     # Intel Homebrew
            "/usr/local/lib/libopus.0.dylib",   # Alternative
        ]
    elif system == "Linux":  # Linux server
        opus_paths = [
            "/usr/lib/x86_64-linux-gnu/libopus.so.0",  # Ubuntu/Debian
            "/usr/lib/libopus.so.0",                    # Generic Linux
            "/usr/lib64/libopus.so.0",                  # CentOS/RHEL
            "/usr/local/lib/libopus.so.0",              # Compiled from source
        ]
    else:
        opus_paths = []
    
    for path in opus_paths:
        try:
            discord.opus.load_opus(path)
            if discord.opus.is_loaded():
                print(f"✅ Loaded Opus from: {path}")
                break
        except Exception as e:
            print(f"❌ Failed to load Opus from {path}: {e}")
            continue
    
    if not discord.opus.is_loaded():
        print("❌ WARNING: Could not load Opus library. Voice features may not work.")

# Try to load from .env file first
def load_env_file():
    """Load environment variables from .env file if it exists."""
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        pass  # .env file doesn't exist, use system environment

load_env_file()

# Configuration
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = {GUILD_ID_GOES_HERE}
VOICE_CHANNEL_ID = {VOICE_CHANNEL_ID_GOES_HERE}
STREAM_URL = "https://audio.junctionnow.com:8000/radio.mp3"

# Validate token
if not TOKEN:
    print("❌ ERROR: DISCORD_TOKEN not found!")
    print("Please set your Discord bot token in one of these ways:")
    print("1. Create a .env file with: DISCORD_TOKEN=your_token_here")
    print("2. Set environment variable: export DISCORD_TOKEN=your_token_here")
    print("3. Run with: DISCORD_TOKEN=your_token_here python main.py")
    exit(1)

# Bot setup
intents = discord.Intents.default()
intents.message_content = False
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Logging setup
log = logging.getLogger("radio_bot")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Connection state management
connection_attempts = 0
max_connection_attempts = 10
last_connection_attempt = 0
connection_backoff = 1  # Starting backoff in seconds

async def wait_with_backoff():
    """Wait with exponential backoff between connection attempts."""
    global connection_backoff
    wait_time = connection_backoff + random.uniform(0, 2)  # Add jitter
    log.info(f"Waiting {wait_time:.1f} seconds before next connection attempt...")
    await asyncio.sleep(wait_time)
    connection_backoff = min(connection_backoff * 2, 60)  # Cap at 60 seconds

async def connect_and_play():
    """(Re)connects to the voice channel and starts the stream."""
    global connection_attempts, last_connection_attempt, connection_backoff
    
    try:
        current_time = time.time()
        
        # Reset connection attempts if it's been a while since last attempt
        if current_time - last_connection_attempt > 300:  # 5 minutes
            connection_attempts = 0
            connection_backoff = 1
        
        connection_attempts += 1
        last_connection_attempt = current_time
        
        if connection_attempts > max_connection_attempts:
            log.error(f"Maximum connection attempts ({max_connection_attempts}) reached. Giving up.")
            return False
        
        log.info(f"Connection attempt {connection_attempts}/{max_connection_attempts}")
        
        guild = bot.get_guild(GUILD_ID)
        if guild is None:
            log.error("Guild not found. Check GUILD_ID.")
            return False

        channel = guild.get_channel(VOICE_CHANNEL_ID)
        if channel is None or not isinstance(channel, discord.VoiceChannel):
            log.error("Voice channel not found or invalid. Check VOICE_CHANNEL_ID.")
            return False

        # Check if we're already connected to this channel
        voice_client = discord.utils.get(bot.voice_clients, guild=guild)
        if voice_client and voice_client.is_connected() and voice_client.channel == channel:
            if voice_client.is_playing():
                log.info("Already connected and playing. Nothing to do.")
                connection_attempts = 0  # Reset on success
                connection_backoff = 1
                return True
            else:
                log.info("Connected but not playing. Starting stream...")
        else:
            # Need to connect or reconnect
            if voice_client:
                try:
                    await voice_client.disconnect(force=True)
                except Exception as e:
                    log.warning(f"Error disconnecting existing voice client: {e}")
            
            log.info("Connecting to voice channel...")
            try:
                voice_client = await channel.connect(reconnect=False, timeout=30.0)
            except discord.errors.ConnectionClosed as e:
                if e.code == 4006:
                    log.error("WebSocket closed with code 4006 (Session no longer valid). This might be a network issue.")
                    await wait_with_backoff()
                    return False
                else:
                    log.error(f"Connection closed with code {e.code}: {e}")
                    await wait_with_backoff()
                    return False
            except Exception as e:
                log.error(f"Failed to connect to voice channel: {e}")
                await wait_with_backoff()
                return False

        # Start playing the stream
        if not voice_client.is_playing():
            try:
                source = discord.FFmpegPCMAudio(
                    STREAM_URL,
                    before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                    options="-vn"
                )
                
                def after_playing(error):
                    if error:
                        log.error(f"Player error: {error}")
                    else:
                        log.info("Stream ended normally")
                
                voice_client.play(source, after=after_playing)
                log.info("✅ Successfully started streaming JunctionNow radio")
                connection_attempts = 0  # Reset on success
                connection_backoff = 1
                return True
                
            except Exception as e:
                log.error(f"Error starting audio stream: {e}")
                return False
        
        return True
        
    except Exception as e:
        log.error(f"Unexpected error in connect_and_play: {e}")
        traceback.print_exc()
        return False

@bot.event
async def on_ready():
    log.info(f"Logged in as {bot.user}")
    
    # Give Discord some time to fully initialize
    await asyncio.sleep(2)
    
    # Try to connect with retries
    success = False
    for attempt in range(5):
        log.info(f"Initial connection attempt {attempt + 1}/5")
        success = await connect_and_play()
        if success:
            break
        await asyncio.sleep(5)
    
    if not success:
        log.error("Failed to establish initial connection after 5 attempts")
    
    # Start the watchdog
    if not watchdog.is_running():
        watchdog.start()

@tasks.loop(seconds=180)  # Check every 3 minutes
async def watchdog():
    """Keeps the bot connected and the audio playing."""
    try:
        guild = bot.get_guild(GUILD_ID)
        if guild is None:
            log.error("Guild not found in watchdog")
            return
            
        voice_client = discord.utils.get(bot.voice_clients, guild=guild)

        if voice_client is None:
            log.warning("No voice client found, attempting to connect...")
            await connect_and_play()
        elif not voice_client.is_connected():
            log.warning("Voice client disconnected, attempting to reconnect...")
            await connect_and_play()
        elif not voice_client.is_playing():
            log.warning("Stream not playing, attempting to restart...")
            await connect_and_play()
        else:
            log.info("✅ Voice connection healthy")
            
    except Exception as e:
        log.error(f"Error in watchdog: {e}")
        traceback.print_exc()

@watchdog.before_loop
async def before_watchdog():
    await bot.wait_until_ready()

@bot.event
async def on_voice_state_update(member, before, after):
    """Handle voice state changes."""
    if bot.user and member.id == bot.user.id:
        if before.channel and not after.channel:
            log.warning("⚠️ Bot was disconnected from voice channel")
            # Schedule a reconnection attempt
            asyncio.create_task(asyncio.sleep(5))  # Wait 5 seconds
            asyncio.create_task(connect_and_play())
        elif not before.channel and after.channel:
            log.info("✅ Bot connected to voice channel")

if __name__ == "__main__":
    try:
        print(discord.opus.is_loaded())
        bot.run(TOKEN)
    except Exception as e:
        log.error(f"Failed to start bot: {e}")
