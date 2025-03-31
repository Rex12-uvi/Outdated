import discord
import asyncio
import random
import os
from datetime import datetime
from discord.ext import commands

# Securely fetch the bot token and owner ID from Render/Replit Secrets
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")

# Ensure OWNER_ID is set before converting to integer
if OWNER_ID is None:
    print("❌ ERROR: OWNER_ID is missing! Set it in Render/Replit Secrets.")
    exit()
else:
    OWNER_ID = int(OWNER_ID)  # Convert to integer

CHANNEL_ID = 1352920497301618718  # Replace with your actual Discord channel ID

# Set bot prefix
bot = commands.Bot(command_prefix=".", intents=discord.Intents.default())

# Variable to track the number of vouches
vouch_count = 0

async def send_vouch_messages():
    """Sends MM deal messages every 10 minutes"""
    global vouch_count
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)

    if channel is None:
        print("❌ ERROR: Invalid CHANNEL_ID. Check if it's correct.")
        return

    while not bot.is_closed():
        # Generate a random price ($0 - $50) and a 7-digit Deal ID
        price = round(random.uniform(0, 50), 2)
        deal_id = random.randint(1000000, 9999999)

        # Create the embed message
        embed = discord.Embed(
            title="✅ SUCCESSFUL MM DEAL",
            description=f"> `PRICE` ~ `${price}`\n> `MM ID` ~ `{deal_id}`",
            color=discord.Color.from_rgb(44, 47, 51)  # Light black color
        )
        embed.set_footer(text="REDOX MM | SERVICES")
        embed.timestamp = datetime.utcnow()

        # Send the embed message
        await channel.send(embed=embed)
        vouch_count += 1  # Increment vouch count
        print(f"✅ Sent MM deal: PRICE: ${price}, DEAL ID: {deal_id} (Total Vouches: {vouch_count})")
        
        # Wait exactly 10 minutes before sending the next message
        await asyncio.sleep(600)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

    # Set bot status to Idle with "Helping in REDOX MM"
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Game(name="Helping in REDOX MM")
    )

    # Start the message loop
    bot.loop.create_task(send_vouch_messages())

# Owner-Only Command: .allvouch
@bot.command()
async def allvouch(ctx):
    """Displays total vouches done by the bot. Only the owner can run this command."""
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ You are not authorized to use this command!")
        return

    embed = discord.Embed(
        title="📊 Total Vouches",
        description=f"🔹 **Total Successful MM Deals:** `{vouch_count}`",
        color=discord.Color.from_rgb(44, 47, 51)
    )
    embed.set_footer(text="REDOX MM | SERVICES")
    await ctx.send(embed=embed)

# Ensure the bot does not run if the token is missing
if TOKEN is None:
    print("❌ ERROR: Bot token is missing! Set it in Render Secrets.")
else:
    bot.run(TOKEN)