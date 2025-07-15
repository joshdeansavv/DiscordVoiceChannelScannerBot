#!/bin/bash

# JunctionNow Radio Bot - macOS Deployment Script
# This script sets up the bot to run locally on macOS using launchd

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SERVICE_NAME="com.junctionnow.radio"
BOT_USER=$(whoami)
BOT_DIR="$HOME/junctionnow-radio-bot"
PLIST_FILE="com.junctionnow.radio.plist"

echo -e "${GREEN}🚀 JunctionNow Radio Bot - macOS Deployment Script${NC}"
echo "========================================================"

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}❌ This script is for macOS only${NC}"
    echo "For Linux, use deploy.sh instead"
    exit 1
fi

# Check if main.py exists
if [[ ! -f "main.py" ]]; then
    echo -e "${RED}❌ main.py not found${NC}"
    echo "Please ensure you're running this script from the bot directory"
    exit 1
fi

# Create bot directory if it doesn't exist
echo -e "${YELLOW}📁 Setting up bot directory...${NC}"
if [[ ! -d "$BOT_DIR" ]]; then
    echo "Creating directory: $BOT_DIR"
    mkdir -p "$BOT_DIR"
fi

# Copy files to bot directory
echo -e "${YELLOW}📋 Copying bot files...${NC}"
cp main.py "$BOT_DIR/"
cp requirements.txt "$BOT_DIR/"
if [[ -f ".env" ]]; then
    cp .env "$BOT_DIR/"
fi

# Set proper permissions
echo -e "${YELLOW}🔒 Setting file permissions...${NC}"
chmod +x "$BOT_DIR/main.py"

# Install Python dependencies
echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"
cd "$BOT_DIR"
pip3 install -r requirements.txt

# Check for Discord token
if [[ ! -f "$BOT_DIR/.env" ]]; then
    echo -e "${YELLOW}⚠️  No .env file found${NC}"
    echo "Please create $BOT_DIR/.env with your Discord token:"
    echo "DISCORD_TOKEN=your_token_here"
    echo ""
    read -p "Press enter to continue with service installation..."
fi

# Create launchd plist file
echo -e "${YELLOW}⚙️  Creating launchd service...${NC}"
cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$SERVICE_NAME</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>$BOT_DIR/main.py</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>$BOT_DIR</string>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>$BOT_DIR/bot.log</string>
    
    <key>StandardErrorPath</key>
    <string>$BOT_DIR/bot-error.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PYTHONUNBUFFERED</key>
        <string>1</string>
    </dict>
    
    <key>ProcessType</key>
    <string>Background</string>
    
    <key>ThrottleInterval</key>
    <integer>10</integer>
</dict>
</plist>
EOF

# Copy plist to LaunchAgents directory
echo -e "${YELLOW}📋 Installing launchd service...${NC}"
cp "$PLIST_FILE" "$HOME/Library/LaunchAgents/"

# Load the service
echo -e "${YELLOW}🚀 Loading the service...${NC}"
launchctl load "$HOME/Library/LaunchAgents/$PLIST_FILE"

# Start the service
echo -e "${YELLOW}✅ Starting the service...${NC}"
launchctl start "$SERVICE_NAME"

# Check service status
echo -e "${GREEN}📊 Service Status:${NC}"
launchctl list | grep "$SERVICE_NAME" || echo "Service not found in list"

echo ""
echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo ""
echo "Bot management commands:"
echo "  Start:   launchctl start $SERVICE_NAME"
echo "  Stop:    launchctl stop $SERVICE_NAME"
echo "  Unload:  launchctl unload ~/Library/LaunchAgents/$PLIST_FILE"
echo "  Load:    launchctl load ~/Library/LaunchAgents/$PLIST_FILE"
echo "  Status:  launchctl list | grep $SERVICE_NAME"
echo "  Logs:    tail -f $BOT_DIR/bot.log"
echo ""
echo "For more commands, see BOT_COMMANDS.md"
echo ""

# Show recent logs if they exist
if [[ -f "$BOT_DIR/bot.log" ]]; then
    echo -e "${GREEN}📝 Recent logs:${NC}"
    tail -n 10 "$BOT_DIR/bot.log"
fi

echo ""
echo -e "${GREEN}✅ Bot is now running and will auto-start on system boot!${NC}"
echo ""
echo -e "${YELLOW}💡 Note: This is for local development on macOS.${NC}"
echo "For production deployment on Linux, use the systemd setup instead." 