# JunctionNow Radio Discord Bot

A 24/7 Discord bot that streams JunctionNow radio to a specific voice channel.

## Features

- Streams audio from https://audio.junctionnow.com:8000/radio.mp3
- Automatically reconnects if the connection drops
- Runs a watchdog loop to ensure 24/7 uptime
- Handles voice channel disconnections gracefully

## Prerequisites

1. **Python 3.8+**
2. **FFmpeg** - Must be installed and available in your system PATH
3. **Discord Bot Token** - Create a bot at https://discord.com/developers/applications

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install FFmpeg:**
   - **macOS:** `brew install ffmpeg`
   - **Ubuntu/Debian:** `sudo apt install ffmpeg`
   - **Windows:** Download from https://ffmpeg.org/download.html

3. **Set up your Discord bot:**
   - Go to https://discord.com/developers/applications
   - Create a new application
   - Go to the "Bot" section
   - Create a bot and copy the token
   - Enable the following bot permissions:
     - Connect
     - Speak
     - Use Voice Activity
     - View Channels

4. **Invite the bot to your server:**
   - Go to OAuth2 > URL Generator
   - Select "bot" scope
   - Select the permissions mentioned above
   - Use the generated URL to invite the bot

## Configuration

The bot is already configured with your specific IDs:
- **Guild ID:** 1364579849276227584
- **Voice Channel ID:** 1394518568112226396
- **Stream URL:** https://audio.junctionnow.com:8000/radio.mp3

## Usage

1. **Set your Discord bot token as an environment variable:**
   ```bash
   export DISCORD_TOKEN="your_bot_token_here"
   ```

2. **Run the bot:**
   ```bash
   python main.py
   ```

## 24/7 Hosting

For true 24/7 operation, host the bot on a VPS or cloud service:

### Using systemd (Linux)
1. Create a service file: `/etc/systemd/system/junctionnow-radio.service`
2. Enable and start the service:
   ```bash
   sudo systemctl enable junctionnow-radio
   sudo systemctl start junctionnow-radio
   ```

### Using PM2 (Node.js process manager)
1. Install PM2: `npm install -g pm2`
2. Start the bot: `pm2 start main.py --name "junctionnow-radio" --interpreter python3`
3. Save and enable auto-restart: `pm2 save && pm2 startup`

## Troubleshooting

- **"Voice channel not found"** - Check that the VOICE_CHANNEL_ID is correct and the bot has access
- **"Guild not found"** - Check that the GUILD_ID is correct and the bot is in the server
- **No audio** - Ensure FFmpeg is installed and in your PATH
- **Connection drops** - The bot will automatically reconnect; check your internet connection

## Logs

The bot logs important events including:
- Connection status
- Stream start/stop events
- Error messages
- Reconnection attempts

## Security Notes

- Never commit your bot token to version control
- Use environment variables for sensitive configuration
- Regularly rotate your bot token 