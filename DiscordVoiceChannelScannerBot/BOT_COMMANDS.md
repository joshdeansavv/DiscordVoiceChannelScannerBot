# JunctionNow Radio Bot - Terminal Commands

This guide provides all the terminal commands needed to manage your Discord bot service.

## Prerequisites

Ensure you're on a Linux system with systemd and have the bot files in `/home/joshua/junctionnow-radio-bot/`.

## 🚀 Initial Setup

### 1. Install the Service
```bash
# Copy the service file to systemd directory
sudo cp junctionnow-radio.service /etc/systemd/system/

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable junctionnow-radio.service
```

### 2. Create Environment File (if needed)
```bash
# Create .env file with your Discord token
echo "DISCORD_TOKEN=your_token_here" > /home/joshua/junctionnow-radio-bot/.env
```

## 🎮 Basic Service Management

### Start the Bot
```bash
sudo systemctl start junctionnow-radio
```

### Stop the Bot
```bash
sudo systemctl stop junctionnow-radio
```

### Restart the Bot
```bash
sudo systemctl restart junctionnow-radio
```

### Check Bot Status
```bash
sudo systemctl status junctionnow-radio
```

## 🔄 Auto-Start Management

### Enable Auto-Start on Boot
```bash
sudo systemctl enable junctionnow-radio
```

### Disable Auto-Start on Boot
```bash
sudo systemctl disable junctionnow-radio
```

### Check if Auto-Start is Enabled
```bash
sudo systemctl is-enabled junctionnow-radio
```

## 📝 Logging & Monitoring

### View Real-Time Logs
```bash
sudo journalctl -u junctionnow-radio -f
```

### View Recent Logs
```bash
sudo journalctl -u junctionnow-radio -n 50
```

### View Logs Since Boot
```bash
sudo journalctl -u junctionnow-radio -b
```

### View Logs for Specific Time Period
```bash
# Last hour
sudo journalctl -u junctionnow-radio --since "1 hour ago"

# Last 24 hours
sudo journalctl -u junctionnow-radio --since "24 hours ago"

# Today
sudo journalctl -u junctionnow-radio --since today
```

## 🔧 Troubleshooting

### Check Service Configuration
```bash
sudo systemctl cat junctionnow-radio
```

### Reload Service After Configuration Changes
```bash
sudo systemctl daemon-reload
sudo systemctl restart junctionnow-radio
```

### Check Service Dependencies
```bash
sudo systemctl list-dependencies junctionnow-radio
```

### Manual Test (Run Without systemd)
```bash
cd /home/joshua/junctionnow-radio-bot
python3 main.py
```

### Check Python Dependencies
```bash
cd /home/joshua/junctionnow-radio-bot
pip3 install -r requirements.txt
```

## 📊 Performance Monitoring

### Check Resource Usage
```bash
sudo systemctl show junctionnow-radio --property=MainPID
sudo ps aux | grep junctionnow-radio
```

### Monitor Memory Usage
```bash
sudo systemctl status junctionnow-radio | grep Memory
```

## 🔒 Security & Permissions

### Check File Permissions
```bash
ls -la /home/joshua/junctionnow-radio-bot/
```

### Fix Permissions if Needed
```bash
sudo chown -R joshua:joshua /home/joshua/junctionnow-radio-bot/
chmod +x /home/joshua/junctionnow-radio-bot/main.py
```

## 🏥 Service Health Check

### Quick Health Check
```bash
# Check if service is running
sudo systemctl is-active junctionnow-radio

# Check if service is enabled
sudo systemctl is-enabled junctionnow-radio

# Full status
sudo systemctl status junctionnow-radio
```

### Restart if Unhealthy
```bash
# Check if running, restart if not
sudo systemctl is-active junctionnow-radio >/dev/null 2>&1 || sudo systemctl restart junctionnow-radio
```

## 🔄 Common Workflows

### Complete Restart After Code Changes
```bash
sudo systemctl stop junctionnow-radio
sudo systemctl daemon-reload
sudo systemctl start junctionnow-radio
sudo systemctl status junctionnow-radio
```

### Emergency Stop and Disable
```bash
sudo systemctl stop junctionnow-radio
sudo systemctl disable junctionnow-radio
```

### Re-enable After Emergency Stop
```bash
sudo systemctl enable junctionnow-radio
sudo systemctl start junctionnow-radio
```

## 📋 Useful Aliases (Optional)

Add these to your `~/.bashrc` for convenience:

```bash
# Bot management aliases
alias bot-start='sudo systemctl start junctionnow-radio'
alias bot-stop='sudo systemctl stop junctionnow-radio'
alias bot-restart='sudo systemctl restart junctionnow-radio'
alias bot-status='sudo systemctl status junctionnow-radio'
alias bot-logs='sudo journalctl -u junctionnow-radio -f'
alias bot-enable='sudo systemctl enable junctionnow-radio'
alias bot-disable='sudo systemctl disable junctionnow-radio'
```

After adding aliases, run: `source ~/.bashrc`

## 🚨 Emergency Commands

### Force Kill if Service Won't Stop
```bash
sudo systemctl kill junctionnow-radio
```

### Reset Failed State
```bash
sudo systemctl reset-failed junctionnow-radio
```

### Completely Remove Service
```bash
sudo systemctl stop junctionnow-radio
sudo systemctl disable junctionnow-radio
sudo rm /etc/systemd/system/junctionnow-radio.service
sudo systemctl daemon-reload
```

---

## 💡 Tips

- Always check logs first when troubleshooting: `sudo journalctl -u junctionnow-radio -f`
- The service will automatically restart on failure (up to 5 times in 5 minutes)
- Resource limits are set to prevent the bot from consuming too much memory/CPU
- The bot will start automatically after system reboot once enabled 