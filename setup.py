#!/usr/bin/env python3
"""
Setup script for JunctionNow Radio Discord Bot
"""

import os

def main():
    print("🎵 JunctionNow Radio Discord Bot Setup")
    print("=" * 40)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("✅ .env file already exists!")
        return
    
    print("\n📝 Please enter your Discord bot token:")
    print("(You can get this from https://discord.com/developers/applications)")
    print("(The token will be saved in a .env file)")
    
    token = input("\nDiscord Bot Token: ").strip()
    
    if not token:
        print("❌ No token provided. Setup cancelled.")
        return
    
    # Create .env file
    try:
        with open('.env', 'w') as f:
            f.write(f"DISCORD_TOKEN={token}\n")
        print("✅ .env file created successfully!")
        print("🔒 Your token has been saved securely.")
        print("\n🚀 You can now run: python main.py")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        print("Please create it manually with: DISCORD_TOKEN=your_token_here")

if __name__ == "__main__":
    main() 