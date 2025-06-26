#!/usr/bin/env python3
"""
Setup script for Minecraft Discord Bot
Helps users configure the bot quickly
"""

import os
import shutil

def create_env_file():
    """Interactive setup for .env file"""
    print("🔧 Setting up environment configuration...")
    print("=" * 50)
    
    if os.path.exists('.env'):
        response = input("⚠️  .env file already exists. Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("✅ Keeping existing .env file")
            return
    
    # Copy example file as starting point
    if os.path.exists('env.example'):
        shutil.copy('env.example', '.env')
        print("✅ Created .env file from template")
    else:
        # Create from scratch
        with open('.env', 'w') as f:
            f.write("# Discord Bot Configuration\n")
            f.write("DISCORD_BOT_TOKEN=your_discord_bot_token_here\n")
            f.write("DISCORD_CHANNEL_ID=your_channel_id_here\n\n")
            f.write("# HermesAPI Configuration\n")
            f.write("HERMES_API_BASE_URL=http://localhost:8080\n")
            f.write("HERMES_API_KEY=your_api_key_here_if_required\n")
        print("✅ Created new .env file")
    
    print("\n📝 Please edit the .env file with your actual values:")
    print("   1. DISCORD_BOT_TOKEN - Get this from Discord Developer Portal")
    print("   2. DISCORD_CHANNEL_ID - Right-click channel in Discord > Copy ID")
    print("   3. HERMES_API_BASE_URL - URL where your HermesAPI is running")
    print("   4. HERMES_API_KEY - Only if your API requires authentication")

def show_discord_setup_guide():
    """Show Discord bot setup instructions"""
    print("\n🤖 Discord Bot Setup Guide")
    print("=" * 50)
    print("1. Go to https://discord.com/developers/applications")
    print("2. Click 'New Application' and give it a name")
    print("3. Go to 'Bot' section and click 'Add Bot'")
    print("4. Copy the 'Token' and put it in your .env file")
    print("5. Under 'Privileged Gateway Intents', enable 'Message Content Intent'")
    print("6. Go to 'OAuth2' > 'URL Generator'")
    print("7. Select 'bot' scope and these permissions:")
    print("   - Send Messages")
    print("   - Use Slash Commands")
    print("   - Read Message History")
    print("   - Add Reactions")
    print("   - Embed Links")
    print("8. Use the generated URL to invite the bot to your Discord server")

def show_hermes_setup_guide():
    """Show HermesAPI setup instructions"""
    print("\n⚙️  HermesAPI Setup Guide")
    print("=" * 50)
    print("1. Download HermesAPI from: https://github.com/RedRedL/Hermes")
    print("2. Install Fabric Loader on your Minecraft server (1.21.1)")
    print("3. Place the HermesAPI .jar file in your server's 'mods' folder")
    print("4. Start your Minecraft server")
    print("5. The API will be available at http://your-server:8080")
    print("6. Test it with: curl http://your-server:8080/players/count")

def main():
    """Main setup function"""
    print("🚀 Minecraft Discord Bot Setup")
    print("=" * 50)
    
    # Create .env file
    create_env_file()
    
    # Ask if user wants setup guides
    print("\n❓ Do you need setup help?")
    
    if input("   Show Discord bot setup guide? (y/N): ").strip().lower() == 'y':
        show_discord_setup_guide()
    
    if input("   Show HermesAPI setup guide? (y/N): ").strip().lower() == 'y':
        show_hermes_setup_guide()
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file with your actual values")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the bot: python discord_bot.py")
    print("   Or use the launcher: python run_bot.py")

if __name__ == "__main__":
    main() 