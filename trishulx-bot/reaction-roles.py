#!/usr/bin/env python3
"""TrishulX Bot — Reaction roles + Welcome DM + Full Moderation"""

import asyncio
import json
import time
import re
from collections import defaultdict
import discord
from discord import Intents, ui, ButtonStyle, Interaction

with open("/home/ubuntu/.openclaw/openclaw.json") as f:
    config = json.load(f)

TOKEN = config["channels"]["discord"]["accounts"]["default"]["token"]
GUILD_ID = 1363577385202483280

# Channel IDs
INTRODUCTIONS_CH = 1474487471671611633
RULES_CH = 1474487465359442033
WELCOME_CH = 1474494105815089264
MOD_LOG_CH = 1474503994335301887

# Message IDs to watch
RULES_MSG_ID = 1474487572175781979
ROLES_MSG_ID = 1474487616606048256

# Role IDs
PARTICIPANT_ROLE_ID = 1474487432807448858
ORGANIZER_ROLE_ID = 1474487425995636990
MENTOR_ROLE_ID = 1474487429246357615

# Emoji -> Role ID mapping
RULES_REACTIONS = {
    "✅": 1474487455230202010,           # Verified
}

ROLES_REACTIONS = {
    "💻": 1474487436670144594,           # Developer
    "🎨": 1474487441288204424,           # Designer
    "🤖": 1474487444551499897,           # AI/ML
    "🌱": 1474487447793701069,           # Beginner
    "🔥": 1474487451547340977,           # Hackday: Pixel Gemini
}

# Current active hackdays
ACTIVE_HACKDAYS = [
    {
        "name": "Pixel Gemini",
        "emoji": "🔥",
        "role_id": 1474487451547340977,
        "description": "Build with Google Gemini — AI-powered pixel art, image generation, and creative tools!",
    }
]

# === MODERATION CONFIG ===

BAD_WORDS = [
    "nigger", "nigga", "faggot", "fag", "retard", "kys", "kill yourself",
    "chutiya", "madarchod", "behenchod", "bhosdike", "randi", "gaand",
    "fuck you", "stfu", "bitch ass", "dick head", "asshole",
]

# Anti-spam: max messages in window
SPAM_MAX_MESSAGES = 5
SPAM_WINDOW_SECONDS = 10
MUTE_DURATION_SECONDS = 300  # 5 min mute

# Warn system
warns_db = defaultdict(list)  # user_id -> [timestamps]
WARN_MUTE_THRESHOLD = 3

# Spam tracker
message_tracker = defaultdict(list)  # user_id -> [timestamps]

# ========================

intents = Intents.default()
intents.members = True
intents.reactions = True
intents.guilds = True
intents.message_content = True

PG_HELP_CH = 1474487508791459860

# Help ticket counter
ticket_counter = {"count": 0}


class HelpTicketModal(ui.Modal, title="🆘 Help Request"):
    topic = ui.TextInput(label="What do you need help with?", placeholder="e.g. API not returning data, build error...", style=discord.TextStyle.short, max_length=100)
    description = ui.TextInput(label="Describe your issue", placeholder="Give details about what's happening...", style=discord.TextStyle.paragraph, max_length=1000)
    tried = ui.TextInput(label="What have you tried?", placeholder="e.g. Checked docs, restarted server...", style=discord.TextStyle.paragraph, max_length=500, required=False)
    tech = ui.TextInput(label="Tech stack", placeholder="e.g. Python, React, Gemini API...", style=discord.TextStyle.short, max_length=200, required=False)

    async def on_submit(self, interaction: Interaction):
        ticket_counter["count"] += 1
        ticket_num = ticket_counter["count"]

        embed = discord.Embed(
            title=f"🎫 Help Ticket #{ticket_num}",
            color=0xff6b6b,
        )
        embed.add_field(name="📌 Topic", value=self.topic.value, inline=False)
        embed.add_field(name="📝 Description", value=self.description.value, inline=False)
        if self.tried.value:
            embed.add_field(name="🔄 Already Tried", value=self.tried.value, inline=False)
        if self.tech.value:
            embed.add_field(name="⚙️ Tech Stack", value=self.tech.value, inline=False)
        embed.set_footer(text=f"Submitted by {interaction.user.display_name}")
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url if interaction.user.display_avatar else None)

        # Create a thread for this ticket
        ch = interaction.guild.get_channel(PG_HELP_CH)
        msg = await ch.send(embed=embed)
        thread = await msg.create_thread(name=f"Ticket #{ticket_num}: {self.topic.value[:50]}")
        await thread.send(f"{interaction.user.mention} your help ticket is open! Others can reply here to help. 🙌")

        await interaction.response.send_message(
            f"✅ Your help ticket #{ticket_num} has been submitted! Check the thread in <#{PG_HELP_CH}>.",
            ephemeral=True
        )
        print(f"  🎫 Help ticket #{ticket_num} from {interaction.user.display_name}: {self.topic.value}")


class HelpButtonView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="🆘 Submit Help Request", style=ButtonStyle.danger, custom_id="help_ticket_btn")
    async def help_button(self, interaction: Interaction, button: ui.Button):
        await interaction.response.send_modal(HelpTicketModal())


class HackdayJoinView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        for hd in ACTIVE_HACKDAYS:
            btn = ui.Button(
                label=f"Join {hd['name']} {hd['emoji']}",
                style=ButtonStyle.primary,
                custom_id=f"join_hackday_{hd['role_id']}"
            )
            btn.callback = self.make_callback(hd)
            self.add_item(btn)

        skip_btn = ui.Button(
            label="Just browsing 👀",
            style=ButtonStyle.secondary,
            custom_id="skip_hackday"
        )
        skip_btn.callback = self.skip_callback
        self.add_item(skip_btn)

    def make_callback(self, hackday):
        async def callback(interaction: Interaction):
            guild = interaction.client.get_guild(GUILD_ID)
            member = guild.get_member(interaction.user.id)
            if not member:
                member = await guild.fetch_member(interaction.user.id)

            hackday_role = guild.get_role(hackday["role_id"])
            participant_role = guild.get_role(PARTICIPANT_ROLE_ID)

            if hackday_role and hackday_role not in member.roles:
                await member.add_roles(hackday_role)
            if participant_role and participant_role not in member.roles:
                await member.add_roles(participant_role)

            await interaction.response.edit_message(
                content=f"🎉 You're in for **{hackday['name']}**! The hackday channels are now unlocked.\n\n"
                        f"📜 Head to <#{RULES_CH}> to read the rules and get verified.\n"
                        f"👋 Introduce yourself in <#{INTRODUCTIONS_CH}>!\n\n"
                        f"Good luck and have fun building! 🚀",
                view=None
            )
            print(f"  🎯 {member.display_name} joined {hackday['name']}")
        return callback

    async def skip_callback(self, interaction: Interaction):
        await interaction.response.edit_message(
            content=f"No worries! You can always join a hackday later from <#{RULES_CH}>.\n\n"
                    f"📜 Read the rules and react ✅ to get verified.\n"
                    f"👋 Say hi in <#{INTRODUCTIONS_CH}>!\n\n"
                    f"Welcome to TrishulX! 🙌",
            view=None
        )
        print(f"  👀 {interaction.user.display_name} skipped hackday")


client = discord.Client(intents=intents)


def is_mod(member):
    """Check if member is organizer or mentor"""
    role_ids = [r.id for r in member.roles]
    return ORGANIZER_ROLE_ID in role_ids or MENTOR_ROLE_ID in role_ids or member.guild_permissions.administrator


async def log_mod_action(guild, action, user, reason, moderator=None):
    """Log moderation action to mod-log channel"""
    ch = guild.get_channel(MOD_LOG_CH)
    if not ch:
        return
    mod_text = f" | By: {moderator}" if moderator else " | Auto-mod"
    await ch.send(f"🛡️ **{action}** | {user.mention} ({user.name}){mod_text}\n📝 Reason: {reason}")


async def mute_member(member, duration, reason):
    """Timeout a member"""
    try:
        until = discord.utils.utcnow() + __import__('datetime').timedelta(seconds=duration)
        await member.timeout(until, reason=reason)
        return True
    except Exception as e:
        print(f"  ❌ Mute failed for {member.display_name}: {e}")
        return False


@client.event
async def on_ready():
    print(f"TrishulX Bot online as {client.user}")
    guild = client.get_guild(GUILD_ID)
    if guild:
        print(f"Connected to: {guild.name} ({guild.member_count} members)")

    # Register persistent views
    client.add_view(HelpButtonView())
    client.add_view(HackdayJoinView())

    # Post help button in #pg-help if not already there
    pg_help = guild.get_channel(PG_HELP_CH) if guild else None
    if pg_help:
        # Check if button msg already exists
        found = False
        async for msg in pg_help.history(limit=20):
            if msg.author == client.user and msg.components:
                found = True
                break
        if not found:
            await pg_help.send(
                "# 🆘 Need Help?\n\n"
                "Don't just drop a message — submit a proper help request so people can actually help you!\n\n"
                "Click the button below to open the form. A thread will be created for your ticket.\n",
                view=HelpButtonView()
            )
            print("  📋 Help button posted in #pg-help")

    print("Moderation: ON | Reaction Roles: ON | Welcome DM: ON | Help Tickets: ON")


@client.event
async def on_member_join(member):
    """Auto-assign roles + welcome new members"""
    if member.guild.id != GUILD_ID:
        return

    print(f"  👋 New member: {member.display_name}")

    # Auto-assign roles
    auto_roles = [
        1474487455230202010,  # Verified
    ]
    for role_id in auto_roles:
        role = member.guild.get_role(role_id)
        if role:
            try:
                await member.add_roles(role)
                print(f"  ✅ Auto-assigned {role.name} to {member.display_name}")
            except Exception as e:
                print(f"  ❌ Failed to assign {role.name}: {e}")

    # Welcome message in #welcome
    welcome_ch = member.guild.get_channel(WELCOME_CH)
    if welcome_ch:
        await welcome_ch.send(
            f"Welcome {member.mention} to **TrishulX**! 🔱\n\n"
            f"🚀 **TEJAS (Quarterly Challenge)** is LIVE!\n"
            f"📅 March 21 | 5:00 PM IST\n"
            f"🔗 Register: <https://events.mlh.io/events/13851-tejas>\n\n"
            f"Head to <#1478658310960975886> for details.\n"
            f"Let's build! 🔥"
        )

    # Also try DM
    try:
        await member.send(
            f"# Welcome to TrishulX! 🔱\n\n"
            f"Hey {member.display_name}! You joined at the perfect time.\n\n"
            f"**TEJAS (MLH Digital Challenge)** is happening on **March 21**!\n"
            f"It's an overnight hackathon to build with AI + Notion.\n\n"
            f"👉 **Register here:** https://events.mlh.io/events/13851-tejas\n"
            f"👉 **Join WhatsApp:** https://chat.whatsapp.com/G47Pc9Z7ws5DEn4adR0aAP\n\n"
            f"Check <#1478658310960975886> in the server for updates. See you there! 🚀"
        )
        print(f"  ✉️ Welcome DM sent to {member.display_name}")
    except discord.Forbidden:
        print(f"  ⚠️ Can't DM {member.display_name} (DMs disabled)")


@client.event
async def on_message(message):
    """Message handler — moderation + commands"""
    if message.author.bot:
        return
    if not message.guild or message.guild.id != GUILD_ID:
        return

    member = message.guild.get_member(message.author.id)
    if not member:
        return

    # Skip mods
    if is_mod(member):
        # But still handle commands
        await handle_commands(message, member)
        return

    content_lower = message.content.lower()

    # --- BAD WORD FILTER ---
    for word in BAD_WORDS:
        if word in content_lower:
            await message.delete()
            warns_db[member.id].append(time.time())
            warn_count = len(warns_db[member.id])

            try:
                await member.send(
                    f"⚠️ Your message in TrishulX was removed for containing inappropriate language.\n"
                    f"Warning {warn_count}/3. {'Next violation = mute.' if warn_count < 3 else ''}"
                )
            except discord.Forbidden:
                pass

            await log_mod_action(message.guild, "BAD WORD + WARN", member,
                                 f"Used banned word. Warning #{warn_count}")

            if warn_count >= WARN_MUTE_THRESHOLD:
                if await mute_member(member, MUTE_DURATION_SECONDS, "3 warnings reached"):
                    await log_mod_action(message.guild, "AUTO-MUTE", member,
                                         f"Reached {WARN_MUTE_THRESHOLD} warnings. Muted for 5 min.")
                    warns_db[member.id] = []  # reset after mute

            print(f"  🚫 Bad word from {member.display_name} — warn #{warn_count}")
            return

    # --- ANTI-SPAM ---
    now = time.time()
    message_tracker[member.id].append(now)
    # Clean old entries
    message_tracker[member.id] = [t for t in message_tracker[member.id]
                                   if now - t < SPAM_WINDOW_SECONDS]

    if len(message_tracker[member.id]) > SPAM_MAX_MESSAGES:
        # Delete recent messages
        async for msg in message.channel.history(limit=20):
            if msg.author.id == member.id:
                try:
                    await msg.delete()
                except:
                    pass

        if await mute_member(member, MUTE_DURATION_SECONDS, "Spam detected"):
            try:
                await member.send(
                    "🔇 You've been muted in TrishulX for 5 minutes for spamming. Chill out!"
                )
            except discord.Forbidden:
                pass

            await log_mod_action(message.guild, "ANTI-SPAM MUTE", member,
                                 f"Sent {len(message_tracker[member.id])} messages in {SPAM_WINDOW_SECONDS}s")
            message_tracker[member.id] = []
            print(f"  🔇 Spam mute: {member.display_name}")
        return

    # --- LINK/INVITE FILTER (extra safety beyond perms) ---
    invite_pattern = r"(discord\.gg/|discord\.com/invite/|discordapp\.com/invite/)"
    if re.search(invite_pattern, content_lower):
        await message.delete()
        try:
            await member.send("🚫 Posting Discord invite links is not allowed in TrishulX.")
        except discord.Forbidden:
            pass
        await log_mod_action(message.guild, "INVITE LINK REMOVED", member, "Posted Discord invite link")
        print(f"  🔗 Invite link removed from {member.display_name}")
        return


async def handle_commands(message, member):
    """Handle mod commands: !warn, !mute, !kick, !warns"""
    content = message.content.strip()

    if content.startswith("!warn "):
        if not message.mentions:
            return
        target = message.mentions[0]
        reason = content.split(maxsplit=2)[2] if len(content.split(maxsplit=2)) > 2 else "No reason given"
        warns_db[target.id].append(time.time())
        warn_count = len(warns_db[target.id])

        try:
            await target.send(f"⚠️ You've been warned in TrishulX. Reason: {reason}\nWarning {warn_count}/3.")
        except discord.Forbidden:
            pass

        await message.channel.send(f"⚠️ {target.mention} warned ({warn_count}/3). Reason: {reason}")
        await log_mod_action(message.guild, "MANUAL WARN", target, reason, moderator=member.display_name)

        if warn_count >= WARN_MUTE_THRESHOLD:
            target_member = message.guild.get_member(target.id)
            if target_member and await mute_member(target_member, MUTE_DURATION_SECONDS, f"3 warns: {reason}"):
                await message.channel.send(f"🔇 {target.mention} auto-muted (3 warnings reached).")
                await log_mod_action(message.guild, "AUTO-MUTE", target, "3 warnings", moderator="System")
                warns_db[target.id] = []

    elif content.startswith("!mute "):
        if not message.mentions:
            return
        target = message.mentions[0]
        target_member = message.guild.get_member(target.id)
        reason = content.split(maxsplit=2)[2] if len(content.split(maxsplit=2)) > 2 else "Manual mute"
        if target_member and await mute_member(target_member, MUTE_DURATION_SECONDS, reason):
            await message.channel.send(f"🔇 {target.mention} muted for 5 minutes. Reason: {reason}")
            await log_mod_action(message.guild, "MANUAL MUTE", target, reason, moderator=member.display_name)

    elif content.startswith("!kick "):
        if not message.mentions:
            return
        target = message.mentions[0]
        reason = content.split(maxsplit=2)[2] if len(content.split(maxsplit=2)) > 2 else "Kicked by moderator"
        target_member = message.guild.get_member(target.id)
        if target_member:
            try:
                await target.send(f"👢 You've been kicked from TrishulX. Reason: {reason}")
            except:
                pass
            await target_member.kick(reason=reason)
            await message.channel.send(f"👢 {target.mention} kicked. Reason: {reason}")
            await log_mod_action(message.guild, "KICK", target, reason, moderator=member.display_name)

    elif content.startswith("!warns"):
        if message.mentions:
            target = message.mentions[0]
            count = len(warns_db[target.id])
            await message.channel.send(f"📋 {target.mention} has {count} warning(s).")
        else:
            await message.channel.send("Usage: `!warns @user`")

    elif content == "!clearwarns" and message.mentions:
        target = message.mentions[0]
        warns_db[target.id] = []
        await message.channel.send(f"✅ Warnings cleared for {target.mention}.")
        await log_mod_action(message.guild, "WARNINGS CLEARED", target, "Manual clear", moderator=member.display_name)


# --- REACTION ROLE HANDLERS ---

@client.event
async def on_raw_reaction_add(payload):
    if payload.guild_id != GUILD_ID:
        return
    if payload.user_id == client.user.id:
        return

    emoji = str(payload.emoji)
    role_id = None

    if payload.message_id == RULES_MSG_ID:
        role_id = RULES_REACTIONS.get(emoji)
    elif payload.message_id == ROLES_MSG_ID:
        role_id = ROLES_REACTIONS.get(emoji)

    if role_id:
        guild = client.get_guild(GUILD_ID)
        member = guild.get_member(payload.user_id) or await guild.fetch_member(payload.user_id)
        role = guild.get_role(role_id)
        if member and role:
            await member.add_roles(role)
            print(f"  + {member.display_name} -> {role.name}")


@client.event
async def on_raw_reaction_remove(payload):
    if payload.guild_id != GUILD_ID:
        return
    if payload.user_id == client.user.id:
        return

    emoji = str(payload.emoji)
    role_id = None

    if payload.message_id == RULES_MSG_ID:
        role_id = RULES_REACTIONS.get(emoji)
    elif payload.message_id == ROLES_MSG_ID:
        role_id = ROLES_REACTIONS.get(emoji)

    if role_id:
        guild = client.get_guild(GUILD_ID)
        member = guild.get_member(payload.user_id) or await guild.fetch_member(payload.user_id)
        role = guild.get_role(role_id)
        if member and role:
            await member.remove_roles(role)
            print(f"  - {member.display_name} x {role.name}")


client.run(TOKEN)
