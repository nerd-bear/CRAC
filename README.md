# CRAC Bot

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Commands](#commands)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Configuration](#configuration)
7. [Project Structure](#project-structure)
8. [Dependencies](#dependencies)
9. [Development](#development)
10. [Contributing](#contributing)
11. [License](#license)
12. [Support](#support)
13. [Creator](#creator)

## Introduction

CRAC Bot is a versatile, all-purpose Discord bot designed to enhance server management and user interaction. Currently in active development, CRAC Bot offers a wide range of features from moderation tools to fun commands, making it a valuable addition to any Discord server.

## Features

1. **Server Moderation**
   - Kick users
   - Ban and unban users
   - Timeout users
   - Nickname management

2. **User Interaction**
   - Character information lookup
   - Text-to-speech functionality
   - Music playback from YouTube
   - User profile display

3. **Bot Management**
   - Customizable bot status
   - Start/shutdown commands
   - Feedback system

4. **Message Handling**
   - Logging of message edits and deletions
   - Inappropriate word detection and filtering

5. **Voice Channel Integration**
   - Join and leave voice channels
   - Play audio in voice channels

6. **Customization**
   - Configurable command prefix
   - Guild-specific settings

## Commands

Here's a detailed list of available commands:

1. `?help`: Displays a help message with all available commands and their usage.

2. `?kick @user [reason]`: Kicks the mentioned user from the server. Requires kick permissions.
   
3. `?ban @user [reason]`: Bans the mentioned user from the server. Requires ban permissions.
   
4. `?unban @user`: Unbans the specified user from the server. Requires ban permissions.
   
5. `?timeout @user <duration> <unit> [reason]`: Timeouts the mentioned user for the specified duration. Requires moderate members permission.
   
6. `?shutdown`: Shuts down the bot. Requires administrator permissions.
   
7. `?start`: Starts the bot if it's offline. Requires administrator permissions.
   
8. `?charinfo [character]`: Provides detailed information about the specified character, including Unicode data.
   
9. `?tts [message]`: Converts the given text to speech and plays it in the user's current voice channel.
   
10. `?play [youtube_url]`: Plays audio from the specified YouTube video in the user's current voice channel.
    
11. `?join`: Makes the bot join the user's current voice channel.
    
12. `?leave`: Makes the bot leave the current voice channel.
    
13. `?profile @user`: Displays detailed profile information about the mentioned user.
    
14. `?nick @user [new_nickname]`: Changes the nickname of the mentioned user. Requires manage nicknames permission.
    
15. `?feedback [message]`: Allows users to submit feedback about the bot, which is stored in a database.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/crac-bot.git
   ```

2. Navigate to the project directory:
   ```
   cd crac-bot
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your Discord bot token:
   - Create a new application in the [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a bot for your application and copy the bot token
   - Create a `config.json` file in the project root and add your token:
     ```json
     {
         "token": "YOUR_BOT_TOKEN_HERE"
     }
     ```

5. Set up the SQLite database:
   ```
   python setup/create_feedback_table.py
   python setup/create_history_table.py
   python setup/create_usage_table.py
   ```

## Usage

1. Run the bot:
   ```
   python launcher.py
   ```

2. Invite the bot to your Discord server:
   - Go to the OAuth2 URL generator in your Discord Developer Portal
   - Select the "bot" scope and the necessary permissions
   - Use the generated URL to invite the bot to your server

3. Once the bot is in your server, use `?help` to see all available commands.

## Configuration

The `config.json` file contains important settings for the bot:

```json
{
    "defaults": {
        "prefix": "?"
    },
    "bot_version": "0.4.5",
    "bot_name": "CRAC",
    "tts_mode": "fast",
    "guilds": {
        "1288144110880030795": {
            "prefix": "*"
        }
    }
}
```

- `defaults.prefix`: The default command prefix for the bot.
- `bot_version`: The current version of the bot.
- `bot_name`: The name of the bot.
- `tts_mode`: The mode for text-to-speech functionality ("fast" or "slow").
- `guilds`: Guild-specific settings, including custom prefixes.

## Project Structure

- `main/bot.py`: The main bot file containing command implementations and event handlers.
- `launcher.py`: The entry point for running the bot.
- `db_manager/`: Directory containing database management modules.
- `setup/`: Directory containing database setup scripts.
- `temp/audio/`: Directory for temporary audio files used by the TTS feature.
- `website/`: Directory containing HTML files for the bot's website.

## Dependencies

CRAC Bot relies on several Python libraries:

- discord.py: The core library for interacting with the Discord API.
- Pillow: Used for image manipulation in the `charinfo` command.
- gTTS: Google Text-to-Speech library for the TTS feature.
- yt_dlp: YouTube downloader used for the music playback feature.
- rich: Used for console output formatting and logging.
- langdetect: Used for language detection in the TTS feature.

For a complete list of dependencies, refer to the `requirements.txt` file.

## Development

CRAC Bot is under active development with nearly daily updates. The development process includes:

- Regular feature additions and improvements
- Bug fixes and performance optimizations
- Refactoring for better code organization and maintainability
- Implementation of user feedback and feature requests

Future development plans include:
- Implementing a music queue system
- Adding more fun and interactive commands
- Improving error handling and user feedback
- Enhancing the configuration system for more granular control

## Contributing

We welcome contributions to CRAC Bot! Here's how you can contribute:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them with clear, descriptive commit messages
4. Push your changes to your fork
5. Submit a pull request to the main repository

Please ensure your code adheres to the existing style conventions and includes appropriate tests.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for the full license text.

## Support

If you need help or want to report a bug, you can:

1. Open an issue on this GitHub repository
2. Join our support Discord server (link to be added)
3. Contact us via email at crac@nerd-bear.org

## Creator

CRAC Bot is created and maintained by Nerd Bear. For more information about the creator and other projects, visit [nerd-bear.org](https://nerd-bear.org).

---

CRAC Bot © 2024 by Nerd Bear. All rights reserved.
>>>>>>> 1fa1e22 (Update bot.py to v0.4.5)
