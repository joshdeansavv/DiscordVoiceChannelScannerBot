#!/usr/bin/env python3
"""
Discord Voice Channel Scanner Bot - Setup Script
Automatically installs dependencies and guides you through configuration.
"""

import os
import sys
import subprocess
import platform

def run_command(command):
    """Run a command and return success status."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. You have Python", sys.version)
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_dependencies():
    """Install Python dependencies."""
    print("📦 Installing Python dependencies...")
    success, output = run_command("pip3 install -r requirements.txt")
    if success:
        print("✅ Dependencies installed successfully")
        return True
    else:
        print("❌ Failed to install dependencies:")
        print(output)
        return False

def check_ffmpeg():
    """Check if FFmpeg is installed."""
    success, output = run_command("ffmpeg -version")
    if success:
        print("✅ FFmpeg is installed")
        return True
    else:
        print("⚠️  FFmpeg not found. Audio processing may not work.")
        print("Install FFmpeg:")
        if platform.system() == "Darwin":  # macOS
            print("  brew install ffmpeg")
        elif platform.system() == "Linux":
            print("  sudo apt install ffmpeg  # Ubuntu/Debian")
            print("  sudo yum install ffmpeg  # CentOS/RHEL")
        else:
            print("  Download from https://ffmpeg.org/download.html")
        return False

def create_env_file():
    """Create .env file if it doesn't exist."""
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    print("📝 Creating .env file...")
    try:
        with open('env.example', 'r') as f:
            example_content = f.read()
        
        with open('.env', 'w') as f:
            f.write(example_content)
        
        print("✅ .env file created from env.example")
        print("⚠️  Please edit .env file with your Discord bot credentials")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Discord Voice Channel Scanner Bot - Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Check FFmpeg
    check_ffmpeg()
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Edit .env file with your Discord bot credentials")
    print("2. Run: python3 main.py")
    print("\nFor detailed instructions, see README.md")
    print("For quick start, see QUICK_START.md")

if __name__ == "__main__":
    main() 