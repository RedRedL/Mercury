# Minecraft Discord Bot with HermesAPI Integration

A Python Discord bot that integrates with the HermesAPI to provide real-time Minecraft server monitoring and communication features.

## Features

### ✅ Currently Implemented
- **Join/Leave Notifications**: Real-time notifications when players join or leave the server
- **Online Player Dashboard**: Shows current player count and list of online players
- **Server Status Monitoring**: Check if the Minecraft server is online and responsive
- **Discord Commands**: Easy-to-use commands for server information

### 🚧 Planned Features
- **Bi-directional Chat Relay**: Forward messages between Discord and Minecraft (waiting for HermesAPI chat endpoints)

## Requirements

- Python 3.11+
- Discord bot token
- Minecraft server with HermesAPI mod installed
- HermesAPI running on your Minecraft server

## Installation

1. **Clone or download this project**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Fill in your configuration values in `.env`:
     ```env
     DISCORD_BOT_TOKEN=your_actual_discord_bot_token
     DISCORD_CHANNEL_ID=123456789012345678
     HERMES_API_BASE_URL=http://your-server:8080
     HERMES_API_KEY=your_api_key_if_required
     ```

4. **Create a Discord Bot**:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application and bot
   - Copy the bot token to your `.env` file
   - Invite the bot to your server with appropriate permissions

5. **Install HermesAPI on your Minecraft server**:
   - Download HermesAPI from [GitHub](https://github.com/RedRedL/Hermes)
   - Install on your Fabric Minecraft server
   - Ensure it's running on port 8080 (or update your config)

## Usage

### Running the Bot

```bash
python discord_bot.py
```

### Discord Commands

- `!mcplayers` or `!mconline` or `!mcwho` - Show current online players
- `!mcstatus` or `!mcserver` - Check server status and connectivity

### Features in Action

#### Join/Leave Notifications
The bot automatically monitors player connections and sends notifications:
- 🟢 When a player joins: "**PlayerName** joined the server"
- 🔴 When a player leaves: "**PlayerName** left the server"

#### Player Dashboard
Use `!mcplayers` to see:
- Current player count
- List of all online players

#### Server Status
Use `!mcstatus` to check:
- Server connectivity
- Current player count
- API endpoint status

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DISCORD_BOT_TOKEN` | Your Discord bot token | Yes | - |
| `DISCORD_CHANNEL_ID` | Channel ID for bot messages | Yes | - |
| `HERMES_API_BASE_URL` | HermesAPI base URL | No | `http://localhost:8080` |
| `HERMES_API_KEY` | API key if authentication is required | No | - |

### HermesAPI Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `GET /players/count` | Get online player count |
| `GET /players/names` | Get list of online player names |
| `GET /players/connections` | SSE stream for join/leave events |

## Future Chat Integration

The bot is designed to support bi-directional chat relay once HermesAPI adds chat endpoints. The structure is already in place:

- `forward_to_minecraft()` - Ready to send Discord messages to Minecraft
- `forward_from_minecraft()` - Ready to receive Minecraft chat messages

Expected future endpoints:
- `POST /chat/send` - Send message to Minecraft chat
- `GET /chat/stream` - SSE stream of chat messages

## Troubleshooting

### Common Issues

1. **Bot not connecting to Discord**:
   - Check your bot token in `.env`
   - Ensure the bot has proper permissions in your Discord server

2. **No player events received**:
   - Verify HermesAPI is running on your Minecraft server
   - Check the `HERMES_API_BASE_URL` in your `.env`
   - Ensure the Minecraft server is accessible from where the bot is running

3. **Commands not working**:
   - Ensure the bot has read/send message permissions in the designated channel
   - Check that `DISCORD_CHANNEL_ID` is correct

4. **API connection errors**:
   - Verify your Minecraft server is running
   - Check that HermesAPI mod is properly installed
   - Ensure port 8080 is accessible

### Logs

The bot provides detailed logging. Check the console output for:
- Connection status to Discord and HermesAPI
- SSE stream events
- API request/response information
- Error messages and stack traces

## Contributing

This bot is designed to work with the current HermesAPI implementation. As HermesAPI evolves and adds new features (like chat endpoints), the bot can be easily extended.

Feel free to contribute by:
- Adding new commands
- Improving error handling
- Adding features for future HermesAPI capabilities
- Improving the user interface

## License

This project is provided as-is for educational and personal use. Please respect the licenses of all dependencies and the HermesAPI project. 
