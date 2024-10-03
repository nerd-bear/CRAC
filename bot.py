import discord

from rich.console import Console
from rich.panel import Panel

import datetime
import os
import unicodedata
import tempfile

from PIL import Image, ImageDraw, ImageFont

BOT_PREFIX = "?"
BOT_NAME = "CRAC Bot"
BOT_VERSION = "0.4.2"

TOKEN = 'TOKEN_MASKED'
LOGGING_CHANNEL_ID = 'LOG_CHANNEL_ID_AS_A_STRING'

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
console = Console()

bot_active = True

async def get_info_text():
    guild_list = "\n".join([f"- {guild.name} (ID: {guild.id})" for guild in client.guilds])
    return f"""
    {BOT_NAME} v{BOT_VERSION}
    Logged in as {client.user.name} (ID: {client.user.id})
    Connected to {len(client.guilds)} guilds:
    {guild_list}
    Bot is ready to use. Ping: {round(client.latency * 1000)}ms
    Prefix: {BOT_PREFIX}
    Initialization complete.
    """

def get_char_image(char):
    # logger.info(f"Generating image for character '{char}'")
    try:
        img = Image.new('RGB', (200, 200), color='white')
        d = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 120)
        except IOError:
            font = ImageFont.load_default()

        d.text((100, 100), char, font=font, fill='black', anchor="mm")

        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            img.save(temp_file, format="PNG")
            temp_file_path = temp_file.name
        
        # logger.info(f"Successfully generated image for character '{char}' at {temp_file_path}")
        return temp_file_path
    except Exception as e:
        logger.error(f"Error generating image for character '{char}': {str(e)}")
        return None

class Logger:
    def __init__(self, path:str = 'C:/logs.log') -> None:
        self.path = path

    def _write_log(self, level: str, message: str):
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log_entry = f'[{timestamp}] {level}: {message}\n'
        with open(self.path, 'a', encoding='utf-8') as logfile:
            logfile.write(log_entry)

    def info(self, message: str = 'No content'):
        self._write_log('INFO', message)

    def warning(self, message: str = 'No content'):
        self._write_log('WARNING', message)
    
    def error(self, message: str = 'No content'):
        self._write_log('ERROR', message)

logger = Logger(path='./logs/output.log')

@client.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    info_text = await get_info_text()
    panel = Panel(info_text, title=f"{BOT_NAME} v{BOT_VERSION} Initialization Info", expand=False)
    
    console.print(panel)
    
    channel = client.get_channel(LOGGING_CHANNEL_ID)
    if channel:
        embed = discord.Embed(title=f"{BOT_NAME} v{BOT_VERSION} Initialization Info", description=info_text, color=0x00ff00, timestamp=datetime.datetime.utcnow())
        embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
        await channel.send(embed=embed)
    
    await client.change_presence(activity=discord.Game(name=f"Run {BOT_PREFIX}help for help"))

@client.event
async def on_message(message: discord.Message):
    global bot_active

    if message.author == client.user:
        return

    if not message.content.startswith(BOT_PREFIX):
        content = message.content.lower()
        if any(word in content for word in ["nigger", "nigga"]):
            await handle_inappropriate_word(message)
        return

    if not bot_active and message.content != f'{BOT_PREFIX}start':
        embed = discord.Embed(title="Bot Offline", description=f"{BOT_NAME} is currently offline. Use {BOT_PREFIX}start to activate.", color=0xff0000)
        embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
        await message.channel.send(embed=embed)
        return

    command = message.content.split()[0][len(BOT_PREFIX):]
    args = message.content.split()[1:]

    if command == 'help':
        await help_command(message)
    elif command == 'kick':
        await kick_command(message)
    elif command == 'ban':
        await ban_command(message)
    elif command == 'shutdown':
        await shutdown_command(message)
    elif command == 'start':
        await start_command(message)
    elif command == 'charinfo':
        await charinfo_command(message)
    elif command in ['play', 'stream', 'listen', 'watch']:
        await status_command(message, command)

async def handle_inappropriate_word(message: discord.Message):
    user = message.author
    channel = message.channel
    
    dm_embed = discord.Embed(title="Inappropriate Word Detected", description=f"{BOT_NAME} has detected an inappropriate word! Please do not send racist words in our server! Moderators have been informed!", color=0xff697a)
    dm_embed.add_field(name="Rules", value="Please read our rules before sending such messages!", inline=False)
    dm_embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
    
    try:
        await user.send(embed=dm_embed)
    except discord.errors.Forbidden:
        pass
    
    await message.delete()
    
    channel_embed = discord.Embed(title="Inappropriate Word Detected", description=f"User {user.mention} tried to send a word that is marked not allowed!", color=0xff697a)
    channel_embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
    await channel.send(embed=channel_embed)

async def help_command(message: discord.Message):
    logger.info(f"{message.author} ran command help")
    embed = discord.Embed(title=f"{BOT_NAME} v{BOT_VERSION} Help Information", description=f"Here are the available commands (prefix: {BOT_PREFIX}):", color=0x9effb8)
    embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')

    commands = {
        "help": {"desc": "Show this help message", "usage": f"{BOT_PREFIX}help"},
        "charinfo": {"desc": "Shows information and an image of the character provided", "usage": f"{BOT_PREFIX}charinfo [character]"},
        "kick": {"desc": "Kick a user from the server (Mod only)", "usage": f"{BOT_PREFIX}kick @user [reason]"},
        "ban": {"desc": "Ban a user from the server (Admin only)", "usage": f"{BOT_PREFIX}ban @user [reason]"},
        "shutdown": {"desc": "Shut down the bot (Admin only)", "usage": f"{BOT_PREFIX}shutdown"},
        "start": {"desc": "Start the bot (Admin only)", "usage": f"{BOT_PREFIX}start"},
        "play": {"desc": "Set bot status to playing (Admin only)", "usage": f"{BOT_PREFIX}play [game name]"},
        "stream": {"desc": "Set bot status to streaming (Admin only)", "usage": f"{BOT_PREFIX}stream [stream name]"},
        "listen": {"desc": "Set bot status to listening (Admin only)", "usage": f"{BOT_PREFIX}listen [song/podcast name]"},
        "watch": {"desc": "Set bot status to watching (Admin only)", "usage": f"{BOT_PREFIX}watch [movie/show name]"},
    }
    
    for cmd, info in commands.items():
        embed.add_field(name=f"{BOT_PREFIX}{cmd}", value=f"{info['desc']}\nUsage: `{info['usage']}`", inline=False)
    
    embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
    await message.channel.send(embed=embed)

async def kick_command(message: discord.Message):
    logger.info(f"{message.author} ran command kick")
    if not message.author.guild_permissions.kick_members:
        embed = discord.Embed(title="Permission Denied", description="You don't have permission to use this command.", color=0xff0000)
        embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
        await message.channel.send(embed=embed)
        return

    if len(message.mentions) < 1:
        embed = discord.Embed(title="Invalid Usage", description=f"Please mention a user to kick. Usage: {BOT_PREFIX}kick @user [reason]", color=0xff0000)
        embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
        await message.channel.send(embed=embed)
        return

    member = message.mentions[0]
    reason = " ".join(message.content.split()[2:]) or "No reason provided"

    try:
        await member.send(embed=discord.Embed(title="You've been Kicked", description=f"You were kicked from {message.guild.name}.\nReason: {reason}", color=0xff0000))
    except:
        pass

    await member.kick(reason=reason)
    embed = discord.Embed(title="User Kicked", description=f"{member.mention} has been kicked.\nReason: {reason}", color=0x00ff00)
    embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
    await message.channel.send(embed=embed)

async def ban_command(message):
    logger.info(f"{message.author} ran command ban")
    if not message.author.guild_permissions.ban_members:
        embed = discord.Embed(title="Permission Denied", description="You don't have permission to use this command.", color=0xff0000)
        embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
        await message.channel.send(embed=embed)
        return

    if len(message.mentions) < 1:
        embed = discord.Embed(title="Invalid Usage", description=f"Please mention a user to ban. Usage: {BOT_PREFIX}ban @user [reason]", color=0xff0000)
        embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
        await message.channel.send(embed=embed)
        return

    member = message.mentions[0]
    reason = " ".join(message.content.split()[2:]) or "No reason provided"

    try:
        await member.send(embed=discord.Embed(title="You've Been Banned", description=f"You were banned from {message.guild.name}.\nReason: {reason}", color=0xff0000))
    except discord.errors.Forbidden:
        pass

    await member.ban(reason=reason)
    embed = discord.Embed(title="User Banned", description=f"{member.mention} has been banned.\nReason: {reason}", color=0x00ff00)
    embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
    await message.channel.send(embed=embed)

async def shutdown_command(message):
    logger.info(f"{message.author} ran command shutdown")
    global bot_active
    if not message.author.guild_permissions.administrator:
        embed = discord.Embed(title="Permission Denied", description="You don't have permission to use this command.", color=0xff0000)
        embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
        await message.channel.send(embed=embed)
        return

    bot_active = False
    await client.change_presence(status=discord.Status.invisible)
    embed = discord.Embed(title=f"{BOT_NAME} Shutting Down", description=f"{BOT_NAME} is now offline.", color=0xff0000, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
    await message.channel.send(embed=embed)

async def start_command(message):
    logger.info(f"{message.author} ran command start")
    global bot_active
    if not message.author.guild_permissions.administrator:
        embed = discord.Embed(title="Permission Denied", description="You don't have permission to use this command.", color=0xff0000)
        embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
        await message.channel.send(embed=embed)
        return

    bot_active = True
    await client.change_presence(status=discord.Status.online)
    embed = discord.Embed(title=f"{BOT_NAME} Starting Up", description=f"{BOT_NAME} is now online.", color=0x00ff00, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
    await message.channel.send(embed=embed)

async def status_command(message: discord.Message, status_type):
    logger.info(f"{message.author} ran command a status change command")
    if not message.author.guild_permissions.administrator:
        embed = discord.Embed(title="Permission Denied", description="You don't have permission to use this command.", color=0xff0000)
        embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
        await message.channel.send(embed=embed)
        return

    status_text = " ".join(message.content.split()[1:])
    if status_type == 'play':
        activity = discord.Game(name=status_text)
    elif status_type == 'stream':
        activity = discord.Streaming(name=status_text, url='https://www.twitch.tv/')
    elif status_type == 'listen':
        activity = discord.Activity(type=discord.ActivityType.listening, name=status_text)
    elif status_type == 'watch':
        activity = discord.Activity(type=discord.ActivityType.watching, name=status_text)

    await client.change_presence(activity=activity)
    embed = discord.Embed(title="Status Updated", description=f"Bot status updated to: {status_type.capitalize()} {status_text}", color=0x00ff00)
    embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
    await message.channel.send(embed=embed)

async def charinfo_command(message: discord.Message):
    logger.info(f"{message.author} ran command charinfo")

    try:
        argument_text = " ".join(message.content.split()[1:])
        char_text = argument_text[0]
    except IndexError:
        await message.channel.send(embed=discord.Embed(title='ERROR', color=0xff123d, description="Please provide a character to get information about."))
        return

    unicode_value = ord(char_text)
    char_name = unicodedata.name(char_text, "Could not find name!")
    char_category = unicodedata.category(char_text)

    unicode_escape = f"\\u{unicode_value:04x}"
    unicode_escape_full = f"\\U{unicode_value:08x}"
    python_escape = repr(char_text)

    embed = discord.Embed(color=0xb3d0ff, title='Character info', type='rich', description=f'Information on character: {char_text}')
    
    embed.add_field(name='Original character', value=char_text, inline=True)
    embed.add_field(name='Character name', value=char_name, inline=True)
    embed.add_field(name='Character category', value=char_category, inline=True)
    embed.add_field(name='Unicode value', value=f"U+{unicode_value:04X}", inline=True)
    embed.add_field(name='Unicode escape', value=unicode_escape, inline=True)
    embed.add_field(name='Full Unicode escape', value=unicode_escape_full, inline=True)
    embed.add_field(name='Python escape', value=python_escape, inline=True)

    embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
    
    image_path = get_char_image(char_text)
    # logger.info(f"Image file path for character '{char_text}': {image_path}")
    
    if image_path:
        file = discord.File(image_path, filename="character.png")
        embed.set_thumbnail(url="attachment://character.png")
        # logger.info(f"Attaching image file for character '{char_text}'")
    else:
        file = None
        logger.warning(f"Failed to generate image for character '{char_text}'")
    
    embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')

    await message.channel.send(embed=embed, file=file)
    # logger.info(f"Character info embed sent for character '{char_text}'")

    if image_path and os.path.exists(image_path):
        os.remove(image_path)
        # logger.info(f"Temporary image file for character '{char_text}' removed")

@client.event
async def on_message_delete(message):
    if message.author == client.user:
        return
    
    channel = client.get_channel(LOGGING_CHANNEL_ID)
    if not channel:
        return
    
    embed = discord.Embed(title="Message Deleted", color=0xff697a, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Author", value=message.author.mention)
    embed.add_field(name="Channel", value=message.channel.mention)
    embed.add_field(name="Content", value=message.content or "No content")
    
    if message.attachments:
        embed.add_field(name="Attachments", value="\n".join([a.url for a in message.attachments]))
    
    embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
    await channel.send(embed=embed)

@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        return
    
    channel = client.get_channel(LOGGING_CHANNEL_ID)
    if not channel:
        return
    
    if before.content == after.content:
        return
    
    embed = discord.Embed(title="Message Edited", color=0xfcba03, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Author", value=before.author.mention)
    embed.add_field(name="Channel", value=before.channel.mention)
    embed.add_field(name="Before", value=before.content or "No content")
    embed.add_field(name="After", value=after.content or "No content")
    
    embed.set_footer(text='This bot is created and hosted by Nerd Bear', icon_url='https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg')
    await channel.send(embed=embed)

client.run(TOKEN)
