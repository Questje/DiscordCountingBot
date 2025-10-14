#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
"""Discord bot client and message handling."""

import os
import discord
import asyncio
import random
from datetime import datetime
from constants import LANGUAGE_FLAGS, ACHIEVEMENT_EMOJIS
from parser import parse_number_with_context
from utils import (get_mistake_message, get_streak_message, check_user_timeout,
                   apply_timeout)
import game_logic

# Load environment variables
from dotenv import load_dotenv
load_dotenv('.env')
TOKEN = os.getenv("TOKEN") 
CHANNEL_ID = 1250289722937315353  # DEV (Dev Server)
#CHANNEL_ID = 1413124693392625846   # PROD (Questje's Hangout - #counting)

# Discord client setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Bot state
bot_ready = False
processing_lock = asyncio.Lock()

def format_leaderboard_embed():
    """Format the leaderboard as a Discord embed."""
    embed = discord.Embed(
        title="📊 **COUNTING LEADERBOARD** 📊",
        description="Top 10 performers in the counting game",
        color=discord.Color.gold(),
        timestamp=datetime.now()
    )
    
    game_state = game_logic.get_game_state()
    user_stats = game_state['user_stats']
    
    if not user_stats:
        embed.add_field(
            name="No Data",
            value="No statistics available yet! Start counting!",
            inline=False
        )
        return embed
    
    sorted_users = sorted(
        user_stats.items(),
        key=lambda x: (x[1]['correct'], 
                      x[1]['correct'] / (x[1]['correct'] + x[1]['wrong']) 
                      if (x[1]['correct'] + x[1]['wrong']) > 0 else 0),
        reverse=True
    )
    
    leaderboard_lines = []
    for i, (_, s) in enumerate(sorted_users[:10], 1):
        total = s['correct'] + s['wrong']
        percentage = (s['correct'] / total * 100) if total > 0 else 0
        leaderboard_lines.append(
          # Temporary version without emojis
          f"**{i}.** {s['username']} - OK: **{s['correct']}** - FAIL: {s['wrong']} - {percentage:.1f}%"
          # f"**{i}.** {s['username']} • ✅ **{s['correct']}** • "
          # f"❌ {s['wrong']} • {percentage:.1f}%"
        )
    
    if leaderboard_lines:
        embed.add_field(
            name="🏆 **Rankings**",
            value="\n".join(leaderboard_lines),
            inline=False
        )
    
    total_attempts = sum(s['correct'] + s['wrong'] for s in user_stats.values())
    total_correct_stats = sum(s['correct'] for s in user_stats.values())
    
    embed.add_field(
        name="📈 **Statistics**",
        value=f"**Total Attempts:** {total_attempts}\n"
              f"**Total Players:** {len(user_stats)}\n"
              f"**Total Accuracy:** {(total_correct_stats / total_attempts * 100) if total_attempts > 0 else 0:.1f}%",
        inline=False
    )
    
    if game_state['testing_mode']:
        embed.add_field(
            name="🧪 **Testing Mode Active**",
            value="Same player can answer repeatedly",
            inline=False
        )
    
    embed.set_footer(text="Keep counting! Use !stats to see this again")
    return embed


def format_profile_embed(username, stats):
    """Format user profile as a Discord embed."""
    embed = discord.Embed(
        title=f"📊 Profile for {username}",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    
    correct = stats.get('correct', 0)
    wrong = stats.get('wrong', 0)
    total = correct + wrong
    accuracy = (correct / total * 100) if total > 0 else 0
    
    embed.add_field(
        name="📈 Statistics",
        value=f"**Correct:** {correct}\n**Wrong:** {wrong}\n**Accuracy:** {accuracy:.1f}%",
        inline=True
    )
    
    embed.add_field(
        name="🔥 Streaks",
        value=f"**Current:** {stats.get('streak', 0)}\n**Best Ever:** {stats.get('best_streak', 0)}",
        inline=True
    )
    
    unlocked_achievements = stats.get('achievements', set())
    if unlocked_achievements:
        sorted_achievements = sorted(list(unlocked_achievements))
        achievement_emojis = [ACHIEVEMENT_EMOJIS.get(ach, '') for ach in sorted_achievements]
        embed.add_field(
            name="🏆 Achievements",
            value=' '.join(emoji for emoji in achievement_emojis if emoji),
            inline=False
        )
    else:
        embed.add_field(
            name="🏆 Achievements",
            value="No achievements unlocked yet. Keep counting!",
            inline=False
        )
    
    embed.set_footer(text="Type !profile to see your own stats.")
    return embed


async def periodic_save_task():
    """Background task that saves state every 5 minutes."""
    await client.wait_until_ready()
    while not client.is_closed():
        await asyncio.sleep(300)
        game_logic.save_state()


@client.event
async def on_ready():
    """Handle bot ready event."""
    global bot_ready
    bot_ready = True
    print(f'✅ Logged in as {client.user}')
    game_logic.load_state()
    client.loop.create_task(periodic_save_task())
    
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        game_state = game_logic.get_game_state()
        await channel.send(
            f"🤖 **Questje's Counting Bot is ready!** Let's count together! "
            f"The next number is **{game_state['next_number']}**! 🎯"
        )
        print(f'📢 Sent greeting to channel {CHANNEL_ID}')
    else:
        print(f'❌ Could not find channel with ID {CHANNEL_ID}')


@client.event
async def on_message(message):
    """Handle incoming messages."""
    if message.author == client.user or message.channel.id != CHANNEL_ID:
        return
    
    async with processing_lock:
        game_state = game_logic.get_game_state()
        user_stats = game_state['user_stats']
        user_stat = user_stats.get(message.author.id, {})
        
        is_timeout, remaining = check_user_timeout(user_stat)
        if is_timeout:
            await message.add_reaction('⏰')
            await message.channel.send(
                f"⏰ {message.author.display_name}, you're in timeout for {remaining} more seconds!"
            )
            return
        
        content = message.content.strip()
        
        # Handle commands
        if content.lower() == '!testing':
            with game_logic.SHARED_DATA_LOCK:
                game_logic.testing_mode = not game_logic.testing_mode
            status = "enabled" if game_logic.testing_mode else "disabled"
            await message.channel.send(f"🧪 **Testing mode {status}!**")
            game_logic.save_state()
            return
        
        if content.lower() in ['!lb', '!stats', '!leaderboard']:
            embed = format_leaderboard_embed()
            await message.channel.send(embed=embed)
            game_logic.save_state()
            return
        
        if content.lower().startswith('!profile'):
            parts = content.split()
            target_user = None
            
            if message.mentions:
                mentioned_user = message.mentions[0]
                if mentioned_user.id in user_stats:
                    target_user = (user_stats[mentioned_user.id]['username'], 
                                 user_stats[mentioned_user.id])
            elif len(parts) == 1:
                if message.author.id in user_stats:
                    target_user = (user_stats[message.author.id]['username'], 
                                 user_stats[message.author.id])
            else:
                target_name = ' '.join(parts[1:]).lower().lstrip('@')
                for uid, stats in user_stats.items():
                    if stats['username'].lower() == target_name:
                        target_user = (stats['username'], stats)
                        break
            
            if target_user:
                embed = format_profile_embed(target_user[0], target_user[1])
                await message.channel.send(embed=embed)
            else:
                search_term = ""
                if message.mentions:
                    search_term = message.mentions[0].display_name
                elif len(parts) > 1:
                    search_term = ' '.join(parts[1:])
                
                if search_term:
                    await message.channel.send(
                        f"🤔 Couldn't find a user with stats named `{search_term}`. "
                        f"They need to count at least once!"
                    )
                else:
                    await message.channel.send(
                        "🤔 You don't have any stats yet! Start counting to build your profile."
                    )
            return
        
        # Parse number from message
        current_expected = game_state['next_number']
        parsed_number, types_used, parse_method, random_info, languages = parse_number_with_context(
            content, current_expected
        )
        
        if parse_method == 'evaluation_timeout':
            await message.add_reaction('🤯')
            await message.channel.send(
                f"🧠 {message.author.display_name}, that calculation was too complex "
                f"or took too long to process!"
            )
            return
        
        if random_info:
            announcements = [f"random({int(min_v)},{int(max_v)}) = {result}" 
                           for min_v, max_v, result in random_info]
            if announcements:
                await message.channel.send(f"🎲 Random rolls: {', '.join(announcements)}")
        
        if parsed_number is not None:
            with game_logic.SHARED_DATA_LOCK:
                is_correct = (parsed_number == current_expected)
                
                # Check for back-to-back answers
                if (is_correct and game_state['last_correct_user'] == message.author.id 
                    and not game_state['testing_mode']):
                    
                    violations = user_stat.get('back_to_back_violations', 0) + 1
                    game_logic.update_user_stats(message.author.id, message.author.display_name, False)
                    game_logic.user_stats[message.author.id]['back_to_back_violations'] = violations
                    
                    await message.add_reaction('🚫')
                    
                    if violations >= 5:
                        game_logic.user_stats[message.author.id] = apply_timeout(
                            game_logic.user_stats[message.author.id], 30
                        )
                        await message.channel.send(
                            f"⏰ {message.author.display_name}, you're in timeout! "
                            f"30 seconds for answering back-to-back 5 times!"
                        )
                    else:
                        await message.channel.send(
                            f"⚠️ Hey {message.author.display_name}! You can't answer twice in a row. "
                            f"That counts as a wrong answer!"
                        )
                    return
                
                if is_correct:
                    game_logic.process_correct_answer(
                        message.author.id, message.author.display_name,
                        parsed_number, content, types_used, parse_method, languages
                    )
                    
                    await message.add_reaction('✅')
                    
                    # Add language flag reactions for all detected languages
                    for lang in languages:
                        if lang in LANGUAGE_FLAGS:
                            await message.add_reaction(LANGUAGE_FLAGS[lang])
                    
                    # Check for polyglot achievement (4+ languages)
                    if len(languages) >= 4:
                        await message.channel.send(
                            f"🗣️ **POLYGLOT!** {message.author.display_name} just used {len(languages)} different languages in one expression! Amazing linguistic skills! 🌍"
                        )
                    
                    # Add achievement emoji reactions based on types used
                    added_emojis = set()  # Track added emojis to avoid duplicates
                    
                    for type_used in types_used:
                        if type_used in ACHIEVEMENT_EMOJIS and ACHIEVEMENT_EMOJIS[type_used] not in added_emojis:
                            try:
                                await message.add_reaction(ACHIEVEMENT_EMOJIS[type_used])
                                added_emojis.add(ACHIEVEMENT_EMOJIS[type_used])
                            except discord.errors.HTTPException:
                                pass  # Ignore if we can't add more reactions
                    
                    streak_message, new_milestone = get_streak_message(
                        game_logic.total_correct, game_logic.last_streak_milestone
                    )
                    if streak_message:
                        game_logic.last_streak_milestone = new_milestone
                        await message.channel.send(streak_message)
                    
                    print(f'✅ Correct: "{content}" → {parsed_number} by {message.author.display_name}')
                    print(f'   Types used: {types_used}')
                    print(f'   Languages: {languages}')
                
                else:
                    should_reset = random.choice([True, False])
                    game_logic.process_wrong_answer(
                        message.author.id, message.author.display_name, should_reset
                    )
                    
                    await message.add_reaction('❌')
                    pun_message = get_mistake_message(user_stat)
                    await message.channel.send(pun_message)
                    
                    if should_reset:
                        await message.channel.send(
                            f"🪙 **Coin flip: HEADS!** 💀 The game resets! Start from **1** again!"
                        )
                    else:
                        await message.channel.send(
                            f"🪙 **Coin flip: TAILS!** 😅 Phew, the counting continues!"
                        )
                    
                    print(f'❌ Wrong: "{content}" → {parsed_number}, expected {current_expected} '
                          f'by {message.author.display_name}')
        else:
            print(f'🔸 Ignoring non-parseable message: "{content}"')


def run():
    """Run the Discord bot."""
    print('🚀 Starting Discord Counting Bot...')
    client.run(TOKEN)