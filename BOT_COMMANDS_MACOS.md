# JunctionNow Radio Bot - macOS Terminal Commands

This guide provides all the terminal commands needed to manage your Discord bot service on macOS using launchd.

## Prerequisites

Ensure you're on macOS and have the bot files in `~/junctionnow-radio-bot/`.

## 🚀 Initial Setup

### 1. Install the Service (macOS)
```bash
# Run the macOS deployment script
./deploy-macos.sh
```

### 2. Create Environment File (if needed)
```bash
# Create .env file with your Discord token
echo "DISCORD_TOKEN=your_token_here" > ~/junctionnow-radio-bot/.env
```

## 🎮 Basic Service Management

### Start the Bot
```bash
launchctl start com.junctionnow.radio
```

### Stop the Bot
```bash
launchctl stop com.junctionnow.radio
```

### Restart the Bot
```bash
launchctl stop com.junctionnow.radio
launchctl start com.junctionnow.radio
```

### Check Bot Status
```bash
launchctl list | grep com.junctionnow.radio
```

## 🔄 Auto-Start Management

### Enable Auto-Start on Boot
```bash
# The service is automatically enabled when installed
# To manually load:
launchctl load ~/Library/LaunchAgents/com.junctionnow.radio.plist
```

### Disable Auto-Start on Boot
```bash
launchctl unload ~/Library/LaunchAgents/com.junctionnow.radio.plist
```

### Check if Auto-Start is Enabled
```bash
launchctl list | grep com.junctionnow.radio
```

## 📝 Logging & Monitoring

### View Real-Time Logs
```bash
tail -f ~/junctionnow-radio-bot/bot.log
```

### View Recent Logs
```bash
tail -n 50 ~/junctionnow-radio-bot/bot.log
```

### View Error Logs
```bash
tail -f ~/junctionnow-radio-bot/bot-error.log
```

### View All Logs
```bash
cat ~/junctionnow-radio-bot/bot.log
```

### Clear Logs
```bash
> ~/junctionnow-radio-bot/bot.log
> ~/junctionnow-radio-bot/bot-error.log
```

## 🔧 Troubleshooting

### Check Service Configuration
```bash
cat ~/Library/LaunchAgents/com.junctionnow.radio.plist
```

### Reload Service After Configuration Changes
```bash
launchctl unload ~/Library/LaunchAgents/com.junctionnow.radio.plist
launchctl load ~/Library/LaunchAgents/com.junctionnow.radio.plist
```

### Manual Test (Run Without launchd)
```bash
cd ~/junctionnow-radio-bot
python3 main.py
```

### Check Python Dependencies
```bash
cd ~/junctionnow-radio-bot
pip3 install -r requirements.txt
```

## 📊 Performance Monitoring

### Check if Process is Running
```bash
ps aux | grep main.py
```

### Check Process Details
```bash
pgrep -f main.py | xargs ps -p
```

### Monitor Resource Usage
```bash
top -pid $(pgrep -f main.py)
```

## 🔒 Security & Permissions

### Check File Permissions
```bash
ls -la ~/junctionnow-radio-bot/
```

### Fix Permissions if Needed
```bash
chmod +x ~/junctionnow-radio-bot/main.py
chmod 644 ~/junctionnow-radio-bot/.env
```

## 🏥 Service Health Check

### Quick Health Check
```bash
# Check if service is loaded
launchctl list | grep com.junctionnow.radio

# Check if process is running
ps aux | grep main.py | grep -v grep

# Check logs for errors
tail -n 20 ~/junctionnow-radio-bot/bot-error.log
```

### Restart if Unhealthy
```bash
# Stop and start the service
launchctl stop com.junctionnow.radio
sleep 2
launchctl start com.junctionnow.radio
```

## 🔄 Common Workflows

### Complete Restart After Code Changes
```bash
# Stop the service
launchctl stop com.junctionnow.radio

# Copy updated files
cp main.py ~/junctionnow-radio-bot/

# Start the service
launchctl start com.junctionnow.radio

# Check status
launchctl list | grep com.junctionnow.radio
```

### Emergency Stop and Disable
```bash
launchctl stop com.junctionnow.radio
launchctl unload ~/Library/LaunchAgents/com.junctionnow.radio.plist
```

### Re-enable After Emergency Stop
```bash
launchctl load ~/Library/LaunchAgents/com.junctionnow.radio.plist
launchctl start com.junctionnow.radio
```

## 📋 Useful Aliases (Optional)

Add these to your `~/.zshrc` or `~/.bash_profile` for convenience:

```bash
# Bot management aliases
alias bot-start='launchctl start com.junctionnow.radio'
alias bot-stop='launchctl stop com.junctionnow.radio'
alias bot-restart='launchctl stop com.junctionnow.radio && sleep 2 && launchctl start com.junctionnow.radio'
alias bot-status='launchctl list | grep com.junctionnow.radio'
alias bot-logs='tail -f ~/junctionnow-radio-bot/bot.log'
alias bot-errors='tail -f ~/junctionnow-radio-bot/bot-error.log'
alias bot-enable='launchctl load ~/Library/LaunchAgents/com.junctionnow.radio.plist'
alias bot-disable='launchctl unload ~/Library/LaunchAgents/com.junctionnow.radio.plist'
```

After adding aliases, run: `source ~/.zshrc` or `source ~/.bash_profile`

## 🚨 Emergency Commands

### Force Kill if Service Won't Stop
```bash
pkill -f main.py
```

### Remove Service Completely
```bash
launchctl stop com.junctionnow.radio
launchctl unload ~/Library/LaunchAgents/com.junctionnow.radio.plist
rm ~/Library/LaunchAgents/com.junctionnow.radio.plist
```

### Check All launchd Services
```bash
launchctl list
```

## 🔍 Debugging

### Check launchd Logs
```bash
log show --predicate 'process == "launchd"' --last 1h
```

### Check System Logs for Bot
```bash
log show --predicate 'process == "python3"' --last 1h
```

### Test Bot Manually
```bash
cd ~/junctionnow-radio-bot
python3 main.py
```

## 📱 macOS-Specific Features

### Check launchd Service Details
```bash
launchctl print system/com.junctionnow.radio
```

### View Service Properties
```bash
launchctl print gui/$(id -u)/com.junctionnow.radio
```

### Check if Service is Loaded
```bash
launchctl list | grep -q com.junctionnow.radio && echo "Loaded" || echo "Not loaded"
```

---

## 💡 Tips

- Always check logs first when troubleshooting: `tail -f ~/junctionnow-radio-bot/bot.log`
- The service will automatically restart if it crashes (KeepAlive is enabled)
- Logs are stored in the bot directory for easy access
- The bot will start automatically after system reboot once loaded
- Use `launchctl list` to see all loaded services
- macOS launchd is equivalent to Linux systemd for service management

## 🔄 Migration to Linux

When you're ready to deploy to a Linux server:

1. Copy your bot files to the Linux server
2. Use the Linux deployment script: `./deploy.sh`
3. Use the Linux command guide: `BOT_COMMANDS.md`
4. The systemd setup provides better resource management and monitoring 