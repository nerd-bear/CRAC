# CRAC Bot Changelog

## Latest Updates

+ Added a launcher file
+ Moved bot file into separate directory
+ Added assets files 
+ Added 4 logo variation SVGs
+ Added command usage file
+ Added command history file
+ Added feedback file
+ Added crac.db folder
+ Added feedback command
+ Added nickname command
+ Removed all status commands
+ Removed all status commands from help embed
+ Updated profile command to grab "some" badges
+ Added nickname command to help embed
+ Added feedback command to help embed
+ Added setup script clear_feedback_table.py
+ Added setup script clear_history_table.py
+ Added setup script create_feedback_table.py
+ Added setup script create_history_table.py
+ Added guild check to nick command
+ Added exception handling to nick command
+ Fixed bugs in history db manager module
+ Removed logger class since it was replaced by new SQLite Database table
+ Updated the nickname command to be a mod-only command and require manage_nicknames permission
+ Added setup script create_usage_table.py
+ Added setup script clear_usage_table.py
+ Created Website directory in CWD of CRAC
+ Added home page to website folder
+ Added home page to commands folder
+ Added home page to versions folder
+ Added usage.py to db_manager library
+ Updated usage.py to have get_db_connection, execute_query, get_usage, get_all_usages and add_usage methods
+ Updated TTS command to use gTTS instead of Speechify, as it's free and open-source
+ Updated home page
+ Created terms of use page
+ Created privacy policy page
+ Updated versions page
+ Removed support page
+ Added load_config function
+ Added save_config function
+ Added std_cout_log function
+ Added log prints to loading of bot (Config loading, config var definition)
+ Updated bot to load config values from config.json
+ Fixed nickname command permissions to require admin or manage_nicknames
+ Updated TTS command, missing arguments to be an embed
+ Updated the command handler to not be case-sensitive
+ Added TTS mode in config

## Summary of Changes

1. **Structure and Organization**
   - Added launcher file and reorganized bot file
   - Created asset files including logo variations
   - Established website directory with various pages

2. **Database Management**
   - Implemented SQLite database (crac.db)
   - Added scripts for creating and clearing database tables
   - Replaced logger class with SQLite database for logging

3. **Commands**
   - Added feedback and nickname commands
   - Removed status commands
   - Updated profile command functionality
   - Improved nickname command with permissions and exception handling

4. **Configuration and Logging**
   - Implemented config loading and saving functions
   - Added standard console output logging
   - Updated bot to use config values from config.json

5. **Text-to-Speech**
   - Switched from Speechify to gTTS for TTS functionality
   - Added TTS mode configuration option

6. **Command Handling**
   - Made command handling case-insensitive
   - Updated help embed to reflect command changes

7. **Website**
   - Created home, commands, versions, terms of use, and privacy policy pages
   - Removed support page

These updates significantly improve the bot's functionality, organization, and user interface while also enhancing its configurability and maintainability.