#!/usr/bin/env python3
"""
Simple launcher script for the Minecraft Discord Bot
"""

import sys
import os
import subprocess

def check_requirements():
    """Check if all required files and environment variables are present"""
    required_files = ['discord_bot.py', 'requirements.txt', '.env']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        
        if '.env' in missing_files:
            print("\n💡 Create a .env file based on env.example")
        
        return False
    
    # Check environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = ['DISCORD_BOT_TOKEN', 'DISCORD_CHANNEL_ID']
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            print("❌ Missing required environment variables in .env:")
            for var in missing_vars:
                print(f"   - {var}")
            print("\n💡 Check your .env file and ensure all required variables are set")
            return False
            
    except ImportError:
        print("❌ python-dotenv not installed. Run: pip install -r requirements.txt")
        return False
    
    return True

def install_requirements():
    """Install requirements if needed"""
    try:
        import discord
        import aiohttp
        from aiohttp_sse_client import sse_client
        print("✅ All requirements are installed")
        return True
    except ImportError:
        print("📦 Installing requirements...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✅ Requirements installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install requirements")
            return False

def main():
    """Main launcher function"""
    print("🚀 Minecraft Discord Bot Launcher")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 11):
        print(f"❌ Python 3.11+ required, you have {sys.version}")
        return 1
    
    print(f"✅ Python {sys.version.split()[0]}")
    
    # Check requirements
    if not check_requirements():
        return 1
    
    # Install dependencies if needed
    if not install_requirements():
        return 1
    
    # Run the bot
    print("\n🤖 Starting Discord bot...")
    print("Press Ctrl+C to stop the bot")
    print("-" * 40)
    
    try:
        import discord_bot
        discord_bot.asyncio.run(discord_bot.main())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Bot crashed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 