#!/bin/bash

# JunctionNow Radio Bot - Deployment Script
# This script sets up the systemd service for the Discord bot

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SERVICE_NAME="junctionnow-radio"
BOT_USER="joshua"
BOT_DIR="/home/joshua/junctionnow-radio-bot"
SERVICE_FILE="junctionnow-radio.service"

echo -e "${GREEN}🚀 JunctionNow Radio Bot Deployment Script${NC}"
echo "=================================================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}❌ This script should not be run as root${NC}"
   echo "Please run as the bot user (joshua) and use sudo when needed"
   exit 1
fi

# Check if systemd is available
if ! command -v systemctl &> /dev/null; then
    echo -e "${RED}❌ systemctl not found. This script requires systemd.${NC}"
    exit 1
fi

# Check if service file exists
if [[ ! -f "$SERVICE_FILE" ]]; then
    echo -e "${RED}❌ Service file '$SERVICE_FILE' not found${NC}"
    echo "Please ensure you're running this script from the bot directory"
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
chown -R "$BOT_USER:$BOT_USER" "$BOT_DIR"

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

# Copy service file to systemd directory
echo -e "${YELLOW}⚙️  Installing systemd service...${NC}"
sudo cp "$SERVICE_FILE" "/etc/systemd/system/"

# Reload systemd
echo -e "${YELLOW}🔄 Reloading systemd...${NC}"
sudo systemctl daemon-reload

# Enable the service
echo -e "${YELLOW}✅ Enabling service for auto-start...${NC}"
sudo systemctl enable "$SERVICE_NAME"

# Start the service
echo -e "${YELLOW}🚀 Starting the service...${NC}"
sudo systemctl start "$SERVICE_NAME"

# Check service status
echo -e "${GREEN}📊 Service Status:${NC}"
sudo systemctl status "$SERVICE_NAME" --no-pager

echo ""
echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo ""
echo "Bot management commands:"
echo "  Start:   sudo systemctl start $SERVICE_NAME"
echo "  Stop:    sudo systemctl stop $SERVICE_NAME"
echo "  Restart: sudo systemctl restart $SERVICE_NAME"
echo "  Status:  sudo systemctl status $SERVICE_NAME"
echo "  Logs:    sudo journalctl -u $SERVICE_NAME -f"
echo ""
echo "For more commands, see BOT_COMMANDS.md"
echo ""

# Show recent logs
echo -e "${GREEN}📝 Recent logs:${NC}"
sudo journalctl -u "$SERVICE_NAME" -n 10 --no-pager

echo ""
echo -e "${GREEN}✅ Bot is now running and will auto-start on system boot!${NC}" 