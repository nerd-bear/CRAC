import discord

from rich.console import Console
from rich.panel import Panel

import yt_dlp

import datetime
import os
import unicodedata
import tempfile
import asyncio
import random
import requests
import base64

from PIL import Image, ImageDraw, ImageFont


BOT_PREFIX = "?"
BOT_NAME = "CRAC Bot"
BOT_VERSION = "0.4.3"

TOKEN = "TOKEN_MASKED"
LOGGING_CHANNEL_ID = 'LOG_CHANNEL_ID_AS_A_INT'

SPEECHIFY_TOKEN = "SPEECHIFY_TOKEN"
API_BASE_URL = "https://api.sws.speechify.com"
VOICE_ID = "george"

intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)
console = Console()

bot_active = True


async def get_info_text():
    guild_list = "\n".join(
        [f"- {guild.name} (ID: {guild.id})" for guild in client.guilds]
    )
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
        img = Image.new("RGB", (200, 200), color="white")
        d = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 120)
        except IOError:
            font = ImageFont.load_default()

        d.text((100, 100), char, font=font, fill="black", anchor="mm")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            img.save(temp_file, format="PNG")
            temp_file_path = temp_file.name

        # logger.info(f"Successfully generated image for character '{char}' at {temp_file_path}")
        return temp_file_path
    except Exception as e:
        logger.error(f"Error generating image for character '{char}': {str(e)}")
        return None


def text_to_speech(text, output_file):
    body = {"input": text, "voice_id": VOICE_ID, "audio_format": "mp3"}

    headers = {
        "Authorization": f"Bearer {SPEECHIFY_TOKEN}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        url=f"{API_BASE_URL}/v1/audio/speech", json=body, headers=headers
    )

    if response.status_code == 200:
        audio_data = base64.b64decode(response.json()["audio_data"])
        with open(output_file, "wb") as f:
            f.write(audio_data)
    else:
        print(f"Error: {response.status_code}, {response.text}")


class Logger:
    def __init__(self, path: str = "./logs/output.log") -> None:
        self.path = path

    def _write_log(self, level: str, message: str):
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        with open(self.path, "a", encoding="utf-8") as logfile:
            logfile.write(log_entry)

    def info(self, message: str = "No content"):
        self._write_log("INFO", message)

    def warning(self, message: str = "No content"):
        self._write_log("WARNING", message)

    def error(self, message: str = "No content"):
        self._write_log("ERROR", message)


logger = Logger()


@client.event
async def on_ready():
    os.system("cls" if os.name == "nt" else "clear")
    info_text = await get_info_text()
    panel = Panel(
        info_text, title=f"{BOT_NAME} v{BOT_VERSION} Initialization Info", expand=False
    )

    console.print(panel)

    channel = client.get_channel(LOGGING_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title=f"{BOT_NAME} v{BOT_VERSION} Initialization Info",
            description=info_text,
            color=0x00FF00,
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await channel.send(embed=embed)

    await client.change_presence(
        activity=discord.Game(name=f"Run {BOT_PREFIX}help for help")
    )


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

    if not bot_active and message.content != f"{BOT_PREFIX}start":
        embed = discord.Embed(
            title="Bot Offline",
            description=f"{BOT_NAME} is currently offline. Use {BOT_PREFIX}start to activate.",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    command = message.content.split()[0][len(BOT_PREFIX) :]
    args = message.content.split()[1:]

    if command == "help":
        await help_command(message)

    elif command == "timeout":
        await timeout_command(message)

    elif command == "kick":
        await kick_command(message)

    elif command == "ban":
        await ban_command(message)

    elif command == "unban":
        await unban_command(message)

    elif command == "shutdown":
        await shutdown_command(message)

    elif command == "start":
        await start_command(message)

    elif command == "charinfo":
        await charinfo_command(message)

    elif command == "join":
        await join_vc_command(message)

    elif command == "leave":
        await leave_vc_command(message)

    elif command == "tts":
        await tts_command(message)

    elif command == "play":
        await play_command(message)

    elif command == "profile":
        await profile_command(message)

    elif command in ["play", "stream", "listen", "watch"]:
        await status_command(message, command)


async def handle_inappropriate_word(message: discord.Message):
    user = message.author
    channel = message.channel

    dm_embed = discord.Embed(
        title="Inappropriate Word Detected",
        description=f"{BOT_NAME} has detected an inappropriate word! Please do not send racist words in our server! Moderators have been informed!",
        color=0xFF697A,
    )
    dm_embed.add_field(
        name="Rules",
        value="Please read our rules before sending such messages!",
        inline=False,
    )
    dm_embed.set_footer(
        text="This bot is created and hosted by Nerd Bear",
        icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
    )

    try:
        await user.send(embed=dm_embed)
    except discord.errors.Forbidden:
        pass

    await message.delete()

    channel_embed = discord.Embed(
        title="Inappropriate Word Detected",
        description=f"User {user.mention} tried to send a word that is marked not allowed!",
        color=0xFF697A,
    )
    channel_embed.set_footer(
        text="This bot is created and hosted by Nerd Bear",
        icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
    )
    await channel.send(embed=channel_embed)


async def help_command(message: discord.Message):
    logger.info(f"{message.author} ran command help")
    embed = discord.Embed(
        title=f"{BOT_NAME} v{BOT_VERSION} Help Information",
        description=f"Here are the available commands (prefix: {BOT_PREFIX}):",
        color=0x9EFFB8,
    )
    embed.set_footer(
        text="This bot is created and hosted by Nerd Bear",
        icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
    )

    commands = {
        "help": {"desc": "Show this help message", "usage": f"{BOT_PREFIX}help"},
        "charinfo": {
            "desc": "Shows information and a image of the character provided",
            "usage": f"{BOT_PREFIX}charinfo [character]",
        },
        "tts": {
            "desc": "Join the vc you are in and uses Text-to-Speech to say your text",
            "usage": f"{BOT_PREFIX}tts [input_text]",
        },
        "play": {
            "desc": "Plays a song in the voice channel you are in",
            "usage": f"{BOT_PREFIX}play [youtube_url]",
        },
        "profile": {
            "desc": "Gets information about the user.",
            "usage": f"{BOT_PREFIX}profile @user",
        },
        "timeout": {
            "desc": "Timeout a user for a specified duration (Mod only)",
            "usage": f"{BOT_PREFIX}timeout @user <duration> <unit> [reason]",
        },
        "kick": {
            "desc": "Kick a user from the server (Mod only)",
            "usage": f"{BOT_PREFIX}kick @user [reason]",
        },
        "ban": {
            "desc": "Ban a user from the server (Admin only)",
            "usage": f"{BOT_PREFIX}ban @user [reason]",
        },
        "unban": {
            "desc": "Unbans a user from the server (Admin only)",
            "usage": f"{BOT_PREFIX}unban @user",
        },
        "shutdown": {
            "desc": "Shut down the bot (Admin only)",
            "usage": f"{BOT_PREFIX}shutdown",
        },
        "start": {"desc": "Start the bot (Admin only)", "usage": f"{BOT_PREFIX}start"},
        "play": {
            "desc": "Set bot status to playing (Admin only)",
            "usage": f"{BOT_PREFIX}play [game name]",
        },
        "stream": {
            "desc": "Set bot status to streaming (Admin only)",
            "usage": f"{BOT_PREFIX}stream [stream name]",
        },
        "listen": {
            "desc": "Set bot status to listening (Admin only)",
            "usage": f"{BOT_PREFIX}listen [song/podcast name]",
        },
        "watch": {
            "desc": "Set bot status to watching (Admin only)",
            "usage": f"{BOT_PREFIX}watch [movie/show name]",
        },
    }

    for cmd, info in commands.items():
        embed.add_field(
            name=f"{BOT_PREFIX}{cmd}",
            value=f"{info['desc']}\nUsage: `{info['usage']}`",
            inline=False,
        )

    embed.set_footer(
        text="This bot is created and hosted by Nerd Bear",
        icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
    )
    await message.channel.send(embed=embed)


async def kick_command(message: discord.Message):
    logger.info(f"{message.author} ran command kick")
    if not message.author.guild_permissions.kick_members:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    if len(message.mentions) < 1:
        embed = discord.Embed(
            title="Invalid Usage",
            description=f"Please mention a user to kick. Usage: {BOT_PREFIX}kick @user [reason]",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    member = message.mentions[0]
    reason = " ".join(message.content.split()[2:]) or "No reason provided"

    try:
        await member.send(
            embed=discord.Embed(
                title="You've wBeen Kicked",
                description=f"You were kicked from {message.guild.name}.\nReason: {reason}",
                color=0xFF0000,
            )
        )
    except:
        pass

    await member.kick(reason=reason)
    embed = discord.Embed(
        title="User Kicked",
        description=f"{member.mention} has been kicked.\nReason: {reason}",
        color=0x00FF00,
    )
    embed.set_footer(
        text="This bot is created and hosted by Nerd Bear",
        icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
    )
    await message.channel.send(embed=embed)


async def ban_command(message: discord.Message):
    logger.info(f"{message.author} ran command ban")
    if not message.author.guild_permissions.ban_members:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    if len(message.mentions) < 1:
        embed = discord.Embed(
            title="Invalid Usage",
            description=f"Please mention a user to ban. Usage: {BOT_PREFIX}ban @user [reason]",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    member = message.mentions[0]
    reason = " ".join(message.content.split()[2:]) or "No reason provided"

    try:
        await member.send(
            embed=discord.Embed(
                title="You've Been Banned",
                description=f"You were banned from {message.guild.name}.\nReason: {reason}",
                color=0xFF0000,
            )
        )
    except:
        pass

    await member.ban(reason=reason)
    embed = discord.Embed(
        title="User Banned",
        description=f"{member.mention} has been banned.\nReason: {reason}",
        color=0x00FF00,
    )
    embed.set_footer(
        text="This bot is created and hosted by Nerd Bear",
        icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
    )
    await message.channel.send(embed=embed)


async def shutdown_command(message: discord.Message):
    logger.info(f"{message.author} ran command shutdown")
    global bot_active
    if not message.author.guild_permissions.administrator:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    bot_active = False
    await client.change_presence(status=discord.Status.invisible)
    embed = discord.Embed(
        title=f"{BOT_NAME} Shutting Down",
        description=f"{BOT_NAME} is now offline.",
        color=0xFF0000,
        timestamp=datetime.datetime.utcnow(),
    )
    embed.set_footer(
        text="This bot is created and hosted by Nerd Bear",
        icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
    )
    await message.channel.send(embed=embed)


async def start_command(message: discord.Message):
    logger.info(f"{message.author} ran command start")
    global bot_active
    if not message.author.guild_permissions.administrator:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    bot_active = True
    await client.change_presence(status=discord.Status.online)
    embed = discord.Embed(
        title=f"{BOT_NAME} Starting Up",
        description=f"{BOT_NAME} is now online.",
        color=0x00FF00,
        timestamp=datetime.datetime.utcnow(),
    )
    embed.set_footer(
        text="This bot is created and hosted by Nerd Bear",
        icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
    )
    await message.channel.send(embed=embed)


async def status_command(message: discord.Message, status_type):
    logger.info(f"{message.author} ran command a status change command")
    if not message.author.guild_permissions.administrator:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    status_text = " ".join(message.content.split()[1:])
    if status_type == "play":
        activity = discord.Game(name=status_text)
    elif status_type == "stream":
        activity = discord.Streaming(name=status_text, url="https://www.twitch.tv/")
    elif status_type == "listen":
        activity = discord.Activity(
            type=discord.ActivityType.listening, name=status_text
        )
    elif status_type == "watch":
        activity = discord.Activity(
            type=discord.ActivityType.watching, name=status_text
        )

    await client.change_presence(activity=activity)
    embed = discord.Embed(
        title="Status Updated",
        description=f"Bot status updated to: {status_type.capitalize()} {status_text}",
        color=0x00FF00,
    )
    embed.set_footer(
        text="This bot is created and hosted by Nerd Bear",
        icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
    )
    await message.channel.send(embed=embed)


async def charinfo_command(message: discord.Message):
    logger.info(f"{message.author} ran command charinfo")

    try:
        argument_text = " ".join(message.content.split()[1:])
        char_text = argument_text[0]
    except IndexError:
        await message.channel.send(
            embed=discord.Embed(
                title="ERROR",
                color=0xFF123D,
                description="Please provide a character to get information about.",
            )
        )
        return

    unicode_value = ord(char_text)
    char_name = unicodedata.name(char_text, "Could not find name!")
    char_category = unicodedata.category(char_text)

    unicode_escape = f"\\u{unicode_value:04x}"
    unicode_escape_full = f"\\U{unicode_value:08x}"
    python_escape = repr(char_text)

    embed = discord.Embed(
        color=0xB3D0FF,
        title="Character info",
        type="rich",
        description=f"Information on character: {char_text}",
    )

    embed.add_field(name="Original character", value=char_text, inline=True)
    embed.add_field(name="Character name", value=char_name, inline=True)
    embed.add_field(name="Character category", value=char_category, inline=True)
    embed.add_field(name="Unicode value", value=f"U+{unicode_value:04X}", inline=True)
    embed.add_field(name="Unicode escape", value=unicode_escape, inline=True)
    embed.add_field(name="Full Unicode escape", value=unicode_escape_full, inline=True)
    embed.add_field(name="Python escape", value=python_escape, inline=True)

    embed.set_footer(
        text="This bot is created and hosted by Nerd Bear",
        icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
    )

    image_path = get_char_image(char_text)
    # logger.info(f"Image file path for character '{char_text}': {image_path}")

    if image_path:
        file = discord.File(image_path, filename="character.png")
        embed.set_thumbnail(url="attachment://character.png")
        # logger.info(f"Attaching image file for character '{char_text}'")
    else:
        file = None
        logger.warning(f"Failed to generate image for character '{char_text}'")

    embed.set_footer(
        text="This bot is created and hosted by Nerd Bear",
        icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
    )

    await message.channel.send(embed=embed, file=file)
    # logger.info(f"Character info embed sent for character '{char_text}'")

    if image_path and os.path.exists(image_path):
        os.remove(image_path)
        # logger.info(f"Temporary image file for character '{char_text}' removed")


async def unban_command(message: discord.Message):
    logger.info(f"{message.author} ran command unban")

    if not message.author.guild_permissions.administrator:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    if len(message.mentions) < 1:
        embed = discord.Embed(
            title="Invalid Usage",
            description=f"Please mention a user to unban. Usage: {BOT_PREFIX}unban @user",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    member = message.mentions[0]
    invite = message.channel.create_invite(reason="Invite unbanned user")

    try:
        await member.send(
            embed=discord.Embed(
                title="You've Been unbanned",
                description=f"You were unbanned from {message.guild.name}",
                color=0x00FF00,
            ).add_field(name="Invite link", value=invite)
        )
    except:
        pass

    try:
        await message.guild.unban(user=member)

    except discord.errors.Forbidden as e:
        embed = discord.Embed(
            title="Forbidden", description=f"Could not unban, {e}", color=0xFF0000
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    except discord.errors.NotFound as e:
        embed = discord.Embed(
            title="Not found", description=f"Could not unban, {e}", color=0xFF0000
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    except discord.errors.HTTPException as e:
        embed = discord.Embed(
            title="Unknown", description=f"Could not unban, {e}", color=0xFF0000
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    embed = discord.Embed(
        title="User Unbanned",
        description=f"{member.mention} has been unbanned.",
        color=0xFF0000,
    )
    embed.set_footer(
        text="This bot is created and hosted by Nerd Bear",
        icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
    )
    await message.channel.send(embed=embed)


async def timeout_command(message: discord.Message):
    logger.info(f"{message.author} ran command timeout")

    if not message.author.guild_permissions.moderate_members:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    args = message.content.split()[1:]
    if len(args) < 3:
        embed = discord.Embed(
            title="Invalid Usage",
            description=f"Usage: {BOT_PREFIX}timeout @user <duration> <unit> [reason]",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    member = message.mentions[0] if message.mentions else None
    if not member:
        embed = discord.Embed(
            title="Invalid Usage",
            description="Please mention a user to timeout.",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    try:
        duration = int(args[1])
        unit = args[2].lower()

    except ValueError:
        embed = discord.Embed(
            title="Invalid Usage",
            description="Duration must be a number.",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    reason = " ".join(args[3:]) if len(args) > 3 else "No reason provided"

    if message.author.top_role <= member.top_role:
        embed = discord.Embed(
            title="Permission Denied",
            description="You cannot timeout this user as they have an equal or higher role.",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    time_units = {"s": "seconds", "m": "minutes", "h": "hours", "d": "days"}
    if unit not in time_units:
        embed = discord.Embed(
            title="Invalid Usage",
            description="Invalid time unit. Use 's' for seconds, 'm' for minutes, 'h' for hours, or 'd' for days.",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    time_delta = datetime.timedelta(**{time_units[unit]: duration})

    try:
        await member.timeout(time_delta, reason=reason)
        embed = discord.Embed(
            title="User Timed Out",
            description=f"{member.mention} has been timed out for {duration}{unit}.\nReason: {reason}",
            color=0x00FF00,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)

    except discord.errors.Forbidden:
        embed = discord.Embed(
            title="Permission Error",
            description="I don't have permission to timeout this user.",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)

    except discord.errors.HTTPException:
        embed = discord.Embed(
            title="Error",
            description="Failed to timeout the user. The duration might be too long.",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)

    try:
        await member.timeout(time_delta, reason=reason)
        embed = discord.Embed(
            title="You were timed out",
            description=f"You (aka {member.mention}) have been timed out for {duration}{unit}.",
            color=0x00FF00,
        )
        embed.add_field(name="reason", value=reason, inline=True)
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await member.send(embed=embed)

    except:
        pass


async def join_vc_command(message: discord.Message):
    logger.info(f"{message.author} ran command join")
    try:
        channel = client.get_channel(message.author.voice.channel.id)
        await channel.connect()
    except Exception as e:
        print(e)


async def leave_vc_command(message: discord.Message):
    logger.info(f"{message.author} ran command leave")
    try:
        await message.guild.voice_client.disconnect()
    except Exception as e:
        pass


async def tts_command(message: discord.Message):
    logger.info(f"{message.author} ran command tts")
    text = " ".join(message.content.split()[1:])

    if not text:
        await message.channel.send("Please provide some text for the TTS.")
        return

    output_file = f"./temp/audio/{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}.mp3"

    try:
        text_to_speech(text, output_file)
    except Exception as e:
        embed = discord.Embed(
            title="Error occurred",
            description=f"A issue occurred during the generation of the Text-to-Speech mp3 file!. Usage: {BOT_PREFIX}tts [message]",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    try:
        voice_channel = message.author.voice.channel
    except:
        embed = discord.Embed(
            title="Join voice channel",
            description=f"Please join a voice channel to use this command!. Usage: {BOT_PREFIX}tts [message]",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    try:
        vc = await voice_channel.connect()
    except discord.ClientException:
        vc = message.guild.voice_client

    if vc.is_playing():
        vc.stop()

    vc.play(
        discord.FFmpegPCMAudio(source=output_file),
        after=lambda e: asyncio.run_coroutine_threadsafe(vc.disconnect(), client.loop),
    )

    while vc.is_playing():
        await asyncio.sleep(0.1)

    if os.path.exists(output_file):
        os.remove(output_file)

    embed = discord.Embed(
        title="Ended TTS",
        description=f"Successfully generated and played TTS file. Disconnecting from <#{voice_channel.id}>",
        color=0x00FF00,
    )
    embed.set_footer(
        text="This bot is created and hosted by Nerd Bear",
        icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
    )
    await message.channel.send(embed=embed)
    return


async def play_command(message: discord.Message):
    logger.info(f"{message.author} ran command play")
    args = message.content.split(" ", 1)
    if len(args) < 2:
        await message.channel.send("Please provide a YouTube URL or search term.")
        return

    query = args[1]

    try:
        voice_channel = message.author.voice.channel
        if not voice_channel:
            raise AttributeError
    except AttributeError:
        embed = discord.Embed(
            title="Join voice channel",
            description="Please join a voice channel to use this command!",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    try:
        vc = await voice_channel.connect()
    except discord.ClientException:
        vc = message.guild.voice_client

    if vc.is_playing():
        vc.stop()

    try:
        with yt_dlp.YoutubeDL({"format": "bestaudio", "noplaylist": "True"}) as ydl:
            info = ydl.extract_info(query, download=False)
            URL = info["url"]
            title = info["title"]
            message.channel.send(content=info)
    except Exception as e:
        embed = discord.Embed(
            title="Error occurred",
            description=f"An issue occurred while trying to fetch the audio: {str(e)}",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    vc.play(
        discord.FFmpegPCMAudio(
            URL,
            **{
                "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                "options": "-vn",
            },
        )
    )

    embed = discord.Embed(
        title="Now Playing",
        description=f"Now playing: {title}",
        color=0x00FF00,
    )
    embed.set_footer(
        text="This bot is created and hosted by Nerd Bear",
        icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
    )
    await message.channel.send(embed=embed)


async def profile_command(message: discord.Message):
    if len(message.mentions) < 0:
        embed = discord.Embed(
            title="Invalid Usage",
            description=f"Usage: {BOT_PREFIX}profile @user",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    try:
        user = message.mentions[0]

    except Exception as e:
        embed = discord.Embed(
            title="Invalid Usage",
            description=f"Usage: {BOT_PREFIX}profile @user",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    try:
        fetched_user = await client.fetch_user(user.id)

    except discord.errors.NotFound as e:
        embed = discord.Embed(
            title="Not found",
            description=f"Error occurred while fetching user. Usage: {BOT_PREFIX}profile @user",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    except discord.errors.HTTPException as e:
        embed = discord.Embed(
            title="Unknown Error",
            description=f"Error occurred while fetching user, but this exception does not have defined behavior. Usage: {BOT_PREFIX}profile @user",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    if user not in message.guild.members:
        embed = discord.Embed(
            title="Member not in guild!",
            description=f"Please make sure that the user you are searching for exists and is in this guild. Usage: {BOT_PREFIX}profile @user",
            color=0xFF0000,
        )
        embed.set_footer(
            text="This bot is created and hosted by Nerd Bear",
            icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
        )
        await message.channel.send(embed=embed)
        return

    avatar = user.avatar
    name = user.display_name
    username = user.name
    user_id = user.id
    status = user.status
    creation = user.created_at.strftime("%d/%m/%y %H:%M:%S")
    # badges   = user.public_flags
    banner_url = None

    # badges_str = str(badges.all()).replace('[<UserFlags.', '').replace('>]', '').replace('_',' ').replace(':', '').title()
    # badges_str = ''.join([i for i in badges_str if not i.isdigit()])

    try:
        banner_url = fetched_user.banner.url
    except:
        pass

    if status == discord.enums.Status(value="dnd"):
        status = "⛔ Do not disturb"

    elif status == discord.enums.Status(value="online"):
        status = "🟢 Online"

    elif status == discord.enums.Status(value="idle"):
        status = "🟡 Idle"

    else:
        status = "⚫ Offline"

    embed = discord.Embed(
        title=f"{name}'s Profile",
        description="Users public discord information, please don't use for bad or illegal purposes!",
    )
    embed.add_field(name="Display Name", value=name, inline=True)
    embed.add_field(name="Username", value=username, inline=True)
    embed.add_field(name="User ID", value=user_id, inline=True)
    embed.add_field(name="Creation Time", value=creation, inline=True)
    embed.add_field(name="Status", value=status, inline=True)
    # embed.add_field(name='Badges',        value=badges_str, inline=True)
    embed.set_thumbnail(
        url=(
            avatar
            if avatar
            else "https://i.pinimg.com/474x/d6/c1/09/d6c109542c43e5b7c6699761c8c78d16.jpg"
        )
    )
    embed.set_footer(
        text="This bot is created and hosted by Nerd Bear",
        icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
    )
    embed.set_image(url=(banner_url if banner_url != None else ""))
    embed.color = 0x5865F2
    embed.colour = 0x5865F2

    await message.channel.send(embed=embed)


@client.event
async def on_message_delete(message):
    if message.author == client.user:
        return

    channel = client.get_channel(LOGGING_CHANNEL_ID)
    if not channel:
        return

    embed = discord.Embed(
        title="Message Deleted", color=0xFF697A, timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="Author", value=message.author.mention)
    embed.add_field(name="Channel", value=message.channel.mention)
    embed.add_field(name="Content", value=message.content or "No content")

    if message.attachments:
        embed.add_field(
            name="Attachments", value="\n".join([a.url for a in message.attachments])
        )

    embed.set_footer(
        text="This bot is created and hosted by Nerd Bear",
        icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
    )
    await channel.send(embed=embed)


async def vc_mute_command():
    pass


@client.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author == client.user:
        return

    channel = client.get_channel(LOGGING_CHANNEL_ID)
    if not channel:
        return

    if before.content == after.content:
        return

    embed = discord.Embed(
        title="Message Edited", color=0xFCBA03, timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="Author", value=before.author.mention)
    embed.add_field(name="Channel", value=before.channel.mention)
    embed.add_field(name="Before", value=before.content or "No content")
    embed.add_field(name="After", value=after.content or "No content")

    embed.set_footer(
        text="This bot is created and hosted by Nerd Bear",
        icon_url="https://as2.ftcdn.net/v2/jpg/01/17/00/87/1000_F_117008730_0Dg5yniuxPQLz3shrJvLIeBsPfPRBSE1.jpg",
    )
    await channel.send(embed=embed)


client.run(TOKEN)
