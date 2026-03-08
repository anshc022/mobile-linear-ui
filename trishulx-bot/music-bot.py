#!/usr/bin/env python3
"""TrishulX Music Bot — Plays music in voice channels 24/7"""

import asyncio
import json
import discord
from discord import Intents, ui, ButtonStyle, Interaction
import yt_dlp
import os

with open("/home/ubuntu/.openclaw/openclaw.json") as f:
    config = json.load(f)

# Use Flare's bot token for music (keeps Echo free)
TOKEN = config["channels"]["discord"]["accounts"]["flare"]["token"]

GUILD_ID = 1363577385202483280
VOICE_CH = 1474526424055545886  # lounge voice
MUSIC_CONTROL_CH = 1474531009025540177  # music-control (admin/organizer only)

# YT-DLP options
YTDL_OPTS = {
    'format': 'bestaudio/best',
    'noplaylist': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0',
    'extract_flat': False,
}

FFMPEG_OPTS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -af "volume=0.3"'
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTS)

intents = Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

client = discord.Client(intents=intents)

# Queue and state
queue = []
current_song = None
voice_client = None
is_playing = False
current_stream_idx = 0
control_msg_id = None


class MusicControlView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="⏸️ Pause", style=ButtonStyle.primary, custom_id="music_pause")
    async def pause_btn(self, interaction: Interaction, button: ui.Button):
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await interaction.response.send_message("⏸️ Music paused!", ephemeral=True)
        else:
            await interaction.response.send_message("Nothing is playing", ephemeral=True)

    @ui.button(label="▶️ Resume", style=ButtonStyle.success, custom_id="music_resume")
    async def resume_btn(self, interaction: Interaction, button: ui.Button):
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await interaction.response.send_message("▶️ Resumed!", ephemeral=True)
        else:
            await interaction.response.send_message("Not paused", ephemeral=True)

    @ui.button(label="⏭️ Skip", style=ButtonStyle.secondary, custom_id="music_skip")
    async def skip_btn(self, interaction: Interaction, button: ui.Button):
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("⏭️ Skipped!", ephemeral=True)
        else:
            await interaction.response.send_message("Nothing to skip", ephemeral=True)

    @ui.button(label="📻 Switch Station", style=ButtonStyle.secondary, custom_id="music_radio")
    async def radio_btn(self, interaction: Interaction, button: ui.Button):
        global current_stream_idx
        current_stream_idx = (current_stream_idx + 1) % len(DEFAULT_STREAMS)
        if voice_client and voice_client.is_playing():
            voice_client.stop()
        await interaction.response.send_message(
            f"📻 Switching to: **{DEFAULT_STREAMS[current_stream_idx]['name']}**", ephemeral=True)

    @ui.button(label="⏹️ Stop", style=ButtonStyle.danger, custom_id="music_stop")
    async def stop_btn(self, interaction: Interaction, button: ui.Button):
        if voice_client:
            queue.clear()
            voice_client.stop()
            await interaction.response.send_message("⏹️ Stopped!", ephemeral=True)
        else:
            await interaction.response.send_message("Not connected", ephemeral=True)

# Free internet radio streams
DEFAULT_STREAMS = [
    {"url": "https://air.pc.cdn.bitgravity.com/air/live/pbaudio001/playlist.m3u8", "name": "📻 All India Radio"},
    {"url": "https://streams.ilovemusic.de/iloveradio109.mp3", "name": "🎵 Bollywood Hits"},
    {"url": "https://streams.ilovemusic.de/iloveradio17.mp3", "name": "🎵 Lofi Hip Hop"},
    {"url": "https://streams.ilovemusic.de/iloveradio21.mp3", "name": "🎵 Chillhop"},
    {"url": "https://stream.laut.fm/lofi", "name": "🎵 Laut.fm Lofi"},
    {"url": "http://hyades.shoutca.st:8043/stream", "name": "🌃 Nightride FM — Synthwave"},
    {"url": "https://streams.ilovemusic.de/iloveradio2.mp3", "name": "💃 Dance Radio"},
]
current_stream_idx = 0

async def get_audio_source(query):
    """Extract audio URL from YouTube"""
    loop = asyncio.get_event_loop()
    try:
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(query, download=False))
        if 'entries' in data:
            data = data['entries'][0]
        url = data.get('url')
        title = data.get('title', 'Unknown')
        return url, title
    except Exception as e:
        print(f"  ❌ YT-DLP error: {e}")
        return None, None


async def play_next(vc):
    """Play the next song in queue or stream radio"""
    global current_song, is_playing, current_stream_idx

    if not vc or not vc.is_connected():
        return

    if queue:
        query = queue.pop(0)
        print(f"  🎵 Loading: {query}")
        url, title = await get_audio_source(query)
        if url:
            current_song = title
            source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTS)
            def after_playing(error):
                if error:
                    print(f"  ❌ Playback error: {error}")
                asyncio.run_coroutine_threadsafe(play_next(vc), client.loop)
            vc.play(source, after=after_playing)
            is_playing = True
            print(f"  ▶️ Now playing: {title}")
            try:
                await update_voice_status(f"🎵 {title[:80]}")
            except:
                pass
        else:
            await play_next(vc)
    else:
        # Play radio stream
        stream = DEFAULT_STREAMS[current_stream_idx % len(DEFAULT_STREAMS)]
        current_song = stream["name"]
        print(f"  📻 Streaming: {stream['name']} — {stream['url']}")

        source = discord.FFmpegPCMAudio(stream["url"], **FFMPEG_OPTS)

        def after_stream(error):
            if error:
                print(f"  ❌ Stream error: {error}")
            # Try next stream on error/disconnect
            asyncio.run_coroutine_threadsafe(reconnect_stream(vc), client.loop)

        vc.play(source, after=after_stream)
        is_playing = True
        try:
            await update_voice_status(stream["name"])
        except:
            pass


async def reconnect_stream(vc):
    """Reconnect to next stream on failure"""
    global current_stream_idx
    await asyncio.sleep(3)
    current_stream_idx = (current_stream_idx + 1) % len(DEFAULT_STREAMS)
    await play_next(vc)


async def update_voice_status(text):
    """Update voice channel status"""
    try:
        headers = {
            "Authorization": f"Bot {TOKEN}",
            "Content-Type": "application/json"
        }
        import aiohttp
        async with aiohttp.ClientSession() as session:
            await session.put(
                f"https://discord.com/api/v10/channels/{VOICE_CH}/voice-status",
                headers=headers,
                json={"status": text[:500]}
            )
    except:
        pass


@client.event
async def on_ready():
    global voice_client
    print(f"Music Bot online as {client.user}")

    guild = client.get_guild(GUILD_ID)
    if not guild:
        print("  ❌ Guild not found!")
        return

    vc_channel = guild.get_channel(VOICE_CH)
    if not vc_channel:
        print("  ❌ Voice channel not found!")
        return

    # Register persistent views
    client.add_view(MusicControlView())

    # Post control panel in music-control channel
    control_ch = guild.get_channel(MUSIC_CONTROL_CH)
    if control_ch:
        found = False
        async for msg in control_ch.history(limit=20):
            if msg.author == client.user and msg.components:
                found = True
                break
        if not found:
            await control_ch.send(
                "# 🎵 Music Controls\n\n"
                "Flare plays music when someone joins 🔊・lounge.\n"
                "Use the buttons below to control playback.\n",
                view=MusicControlView()
            )
            print("  🎛️ Music control panel posted in #music-control")

    # Check if anyone is already in the voice channel
    human_members = [m for m in vc_channel.members if not m.bot]
    if human_members:
        try:
            voice_client = await vc_channel.connect()
            print(f"  🔊 Connected (humans already in channel)")
            await play_next(voice_client)
        except Exception as e:
            print(f"  ❌ Failed to connect: {e}")
    else:
        print("  💤 No one in voice — waiting for someone to join")


@client.event
async def on_message(message):
    """Handle music commands"""
    global voice_client, is_playing

    if message.author.bot:
        return
    if not message.guild or message.guild.id != GUILD_ID:
        return

    content = message.content.strip().lower()

    if content.startswith("!play "):
        query = message.content[6:].strip()
        queue.append(query)
        await message.channel.send(f"🎵 Added to queue: **{query}**")
        if voice_client and not voice_client.is_playing():
            await play_next(voice_client)

    elif content == "!skip":
        if voice_client and voice_client.is_playing():
            voice_client.stop()  # triggers after callback which plays next
            await message.channel.send("⏭️ Skipped!")

    elif content == "!queue":
        if queue:
            q_list = "\n".join([f"  {i+1}. {s}" for i, s in enumerate(queue[:10])])
            await message.channel.send(f"📋 Queue:\n{q_list}")
        else:
            await message.channel.send("📋 Queue is empty — playing defaults")

    elif content == "!nowplaying" or content == "!np":
        if current_song:
            await message.channel.send(f"▶️ Now playing: **{current_song}**")
        else:
            await message.channel.send("Nothing playing right now")

    elif content == "!pause":
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await message.channel.send("⏸️ Paused")

    elif content == "!resume":
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await message.channel.send("▶️ Resumed")

    elif content == "!stop":
        if voice_client:
            queue.clear()
            voice_client.stop()
            await message.channel.send("⏹️ Stopped and cleared queue")

    elif content == "!radio":
        current_stream_idx = (current_stream_idx + 1) % len(DEFAULT_STREAMS)
        if voice_client and voice_client.is_playing():
            voice_client.stop()  # triggers next stream
        await message.channel.send(f"📻 Switching to: **{DEFAULT_STREAMS[current_stream_idx]['name']}**")

    elif content == "!stations":
        stations = "\n".join([f"  {i+1}. {s['name']}" for i, s in enumerate(DEFAULT_STREAMS)])
        await message.channel.send(f"📻 Available stations:\n{stations}\n\nUse `!radio` to switch")


@client.event
async def on_voice_state_update(member, before, after):
    """Join when human joins, leave when all humans leave"""
    global voice_client

    # Ignore bot's own state changes
    if member.bot:
        # If bot got disconnected, reset
        if member.id == client.user.id and before.channel and not after.channel:
            voice_client = None
        return

    guild = client.get_guild(GUILD_ID)
    if not guild:
        return
    vc_channel = guild.get_channel(VOICE_CH)
    if not vc_channel:
        return

    # Human joined pg-voice
    if after.channel and after.channel.id == VOICE_CH:
        if not voice_client or not voice_client.is_connected():
            try:
                voice_client = await vc_channel.connect()
                print(f"  🔊 {member.display_name} joined — starting music!")
                await play_next(voice_client)
            except Exception as e:
                print(f"  ❌ Failed to connect: {e}")

    # Human left pg-voice
    if before.channel and before.channel.id == VOICE_CH:
        human_members = [m for m in vc_channel.members if not m.bot]
        if not human_members and voice_client and voice_client.is_connected():
            print("  💤 No humans left — disconnecting")
            voice_client.stop()
            await voice_client.disconnect()
            voice_client = None


client.run(TOKEN)
