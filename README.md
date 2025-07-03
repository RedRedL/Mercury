# Minecraft Discord Bot with HermesAPI Integration

A Python Discord bot that integrates with the HermesAPI to provide real-time Minecraft server monitoring and communication features.

## Features

### ✅ Currently Implemented
- **Join/Leave Notifications**: Real-time notifications when players join or leave the server
- **Online Player Dashboard**: Shows current player count and list of online players
- **Server Status Monitoring**: Check if the Minecraft server is online and responsive
- **Discord Commands**: Easy-to-use commands for server information
- **Bi-directional Chat Relay**: Forward messages between Discord and Minecraft using HermesAPI chat endpoints

### 🚧 Planned Features
- Additional server monitoring features
- Player statistics and tracking
- Enhanced command features

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

#### Chat Relay
Real-time bidirectional chat between Discord and Minecraft:
- Discord messages are forwarded to Minecraft with `[Discord] Username` prefix
- Minecraft chat messages appear as embedded messages in Discord
- Messages react with ✅ when successfully sent or ❌ if failed

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
| `POST /chat/send` | Send Discord messages to Minecraft chat |
| `GET /chat/stream` | SSE stream for Minecraft chat messages |

## Chat Integration

The bot now supports bi-directional chat relay with HermesAPI's chat endpoints:

### Features:
- **Discord to Minecraft**: Messages sent in the designated Discord channel are forwarded to Minecraft chat with the format `[Discord] Username: message`
- **Minecraft to Discord**: Chat messages from Minecraft players are forwarded to Discord as embedded messages
- **Loop Prevention**: Messages sent from Discord are properly tagged to prevent infinite message loops
- **Real-time Streaming**: Uses Server-Sent Events (SSE) for real-time chat message streaming

### Chat Message Flow:
1. User types message in Discord channel
2. Bot forwards message to Minecraft via `POST /chat/send`
3. Message appears in Minecraft chat as `[Discord] Username: message`
4. When Minecraft players chat, messages are streamed via `GET /chat/stream`
5. Bot receives chat events and forwards them to Discord as embedded messages

### Endpoints Used:
- `POST /chat/send` - Send Discord messages to Minecraft chat
- `GET /chat/stream` - Receive Minecraft chat messages in real-time

The chat integration supports both JSON and plain text formats for maximum compatibility with different HermesAPI implementations.

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

5. **Chat messages not forwarding**:
   - Check that HermesAPI has the chat endpoints implemented (`/chat/send` and `/chat/stream`)
   - Verify the bot has permissions to read messages and add reactions
   - Check console logs for error messages about chat API calls
   - Ensure your HermesAPI version supports chat functionality

6. **Messages appearing twice or in loops**:
   - The bot has loop prevention built-in
   - If you see duplicate messages, check for multiple bot instances running
   - Messages from Discord are tagged with `[Discord]` to prevent loops

### Logs

The bot provides detailed logging. Check the console output for:
- Connection status to Discord and HermesAPI
- Player join/leave events from SSE streams
- Chat message forwarding (both directions)
- API request/response information for chat endpoints
- Error messages and stack traces
- SSE stream connection status for both player events and chat messages

## Contributing

This bot now includes full chat integration with HermesAPI and is ready for production use. As HermesAPI continues to evolve, the bot can be easily extended with new features.

Feel free to contribute by:
- Adding new commands and features
- Improving error handling and user experience
- Adding support for future HermesAPI capabilities
- Enhancing the chat integration with features like message formatting, commands, etc.
- Improving the user interface and Discord embed designs

The chat integration is designed to be robust and includes:
- Automatic reconnection for SSE streams
- Loop prevention for chat messages
- Support for both JSON and plain text chat formats
- Comprehensive error handling and logging

## License

This project is under a MIT license. Additionally respect the licenses of all dependencies and the HermesAPI project. 
