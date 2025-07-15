# 🎵 Discord Voice Channel Scanner Bot

A robust 24/7 Discord bot that streams audio to a voice channel with automatic reconnection, perfect for radio stations, music streams, or any continuous audio feed.

## ✨ Features

- 🎧 **24/7 Audio Streaming** - Continuously streams audio to Discord voice channels
- 🔄 **Auto-Reconnection** - Automatically reconnects on network issues or crashes
- 🛡️ **Robust Error Handling** - Handles WebSocket errors and connection drops gracefully
- 📊 **Health Monitoring** - Built-in watchdog to ensure the stream stays active
- 🚀 **Easy Setup** - Simple configuration with environment variables
- 🔒 **Secure** - No hardcoded tokens or sensitive data

## 🚀 Quick Start

### 1. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to "Bot" section and click "Add Bot"
4. Copy the bot token (you'll need this later)
5. Enable these permissions:
   - **Server Members Intent**
   - **Message Content Intent** (if needed)
6. Go to "OAuth2" → "URL Generator"
7. Select scopes: `bot` and `applications.commands`
8. Select permissions: `Connect`, `Speak`, `Use Voice Activity`
9. Use the generated URL to invite the bot to your server

### 2. Get Your Server and Channel IDs

1. **Enable Developer Mode** in Discord:
   - User Settings → Advanced → Developer Mode
2. **Get Server ID**: Right-click your server name → "Copy Server ID"
3. **Get Voice Channel ID**: Right-click the voice channel → "Copy Channel ID"

### 3. Download and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/DiscordVoiceChannelScannerBot.git
cd DiscordVoiceChannelScannerBot

# Run the automatic setup script
python3 setup.py

# Edit the .env file with your values
nano .env
```

### 4. Configure Your Bot

Edit the `.env` file with your Discord information:

```env
DISCORD_TOKEN=your_bot_token_here
DISCORD_GUILD_ID=your_server_id_here
DISCORD_VOICE_CHANNEL_ID=your_voice_channel_id_here
STREAM_URL=https://your-audio-stream-url.com/stream.mp3
```

### 5. Run the Bot

```bash
python3 main.py
```

🎉 **That's it!** Your bot should now connect to the voice channel and start streaming audio.

## 📋 Requirements

- **Python 3.8+**
- **FFmpeg** (for audio processing)
- **Discord Bot Token**
- **Audio Stream URL** (optional - defaults to JunctionNow radio)

### Installing FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [FFmpeg website](https://ffmpeg.org/download.html)

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_TOKEN` | ✅ | Your Discord bot token |
| `DISCORD_GUILD_ID` | ✅ | Your Discord server ID |
| `DISCORD_VOICE_CHANNEL_ID` | ✅ | Your voice channel ID |
| `STREAM_URL` | ❌ | Audio stream URL (defaults to JunctionNow radio) |

### Example Stream URLs

- **Radio Stream**: `https://stream.radio.co/s1234567890/listen`
- **MP3 Stream**: `https://example.com/audio.mp3`
- **Icecast Stream**: `http://icecast.example.com:8000/stream.mp3`

## 🛠️ Advanced Setup

### Running as a Service (Linux)

```bash
# Make the deployment script executable
chmod +x deploy.sh

# Run the deployment script
./deploy.sh
```

### Running as a Service (macOS)

```bash
# Make the deployment script executable
chmod +x deploy-macos.sh

# Run the deployment script
./deploy-macos.sh
```

### Manual Service Setup

See the detailed guides:
- [Linux Commands](BOT_COMMANDS.md)
- [macOS Commands](BOT_COMMANDS_MACOS.md)

## 🔍 Troubleshooting

### Common Issues

**Bot won't connect to voice channel:**
- Check if the bot has permission to join the voice channel
- Verify the channel ID is correct
- Ensure the bot is in the server

**Audio not playing:**
- Check if FFmpeg is installed
- Verify the stream URL is accessible
- Check the bot logs for errors

**Connection drops frequently:**
- This is normal! The bot has built-in reconnection logic
- Check your internet connection
- The bot will automatically retry with exponential backoff

### Getting Help

1. Check the logs: `tail -f bot.log`
2. Verify your configuration in `.env`
3. Test the stream URL in a browser
4. Check Discord bot permissions

## 📝 Logs

The bot creates detailed logs:
- `bot.log` - General bot activity
- `bot-error.log` - Error messages

View logs in real-time:
```bash
tail -f bot.log
```

## 🔒 Security

- ✅ No hardcoded tokens or sensitive data
- ✅ Environment variables for configuration
- ✅ `.env` file is ignored by git
- ✅ Minimal bot permissions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [discord.py](https://github.com/Rapptz/discord.py)
- Audio processing with FFmpeg
- Inspired by the need for reliable Discord audio streaming

---

**Need help?** Open an issue on GitHub or check the troubleshooting section above! 