# 🚀 Quick Start Guide

Get your Discord bot running in 5 minutes!

## Step 1: Create Discord Bot
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" → Name it
3. Go to "Bot" → "Add Bot" → Copy the token
4. Go to "OAuth2" → "URL Generator"
5. Select: `bot` + `applications.commands`
6. Select permissions: `Connect`, `Speak`, `Use Voice Activity`
7. Copy the URL and invite bot to your server

## Step 2: Get IDs
1. Enable Developer Mode: Settings → Advanced → Developer Mode
2. Right-click server name → "Copy Server ID"
3. Right-click voice channel → "Copy Channel ID"

## Step 3: Setup Bot
```bash
# Download and setup
git clone https://github.com/yourusername/DiscordVoiceChannelScannerBot.git
cd DiscordVoiceChannelScannerBot
python3 setup.py  # Automatic setup!

# Configure
nano .env  # Add your token and IDs
```

## Step 4: Run
```bash
python3 main.py
```

🎉 **Done!** Your bot is now streaming audio to Discord!

---

**Need help?** Check the full [README.md](README.md) for detailed instructions. 