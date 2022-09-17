from re import A
import time
import discord
from discord.ext import commands

import os
import random
from dotenv import load_dotenv

import asyncio
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="./",
                   activity=discord.Game(name="What's your reaction time?"),
                   intents=intents
                   )

TOKEN = os.environ["TOKEN"]
SERVERS = [941803156633956362]
EMOJIS = [  # add more emojis if you want more choices

    "⚫",
    "🔵",
    "🟤",
    "🟠",
    "🟣",
    "⚪",
    "🟡",
    "🟢",
    "🔴"
]


@bot.event
async def on_ready():
    print("Logged in as {}".format(bot.user))


@bot.slash_command(name="start_reaction", guild_ids=SERVERS)
async def start_reaction(ctx: discord.ApplicationContext):
    v = discord.ui.View(timeout=10, disable_on_timeout=True)

    async def on_timeout() -> None:

        await m.edit(view=None, embed=discord.Embed(
            title="Cancelled",
            description="It took more then 10 seconds to respond",
            colour=discord.Color.red()
        ))
    v.on_timeout = on_timeout
    rand_btn = random.choice(EMOJIS)
    for emoji in EMOJIS:
        if emoji == rand_btn:
            async def now_callback(interaction: discord.Interaction) -> None:
                if interaction.user != ctx.user:
                    await interaction.response.send_message("This was not meant for you!", ephemeral=True)
                    return
                difference = float(time.time() - now)
                success_embed = discord.Embed(
                    title=f"Time: {difference:.3f} seconds", description=f"It took {difference:.3f} seconds to click on the button", colour=discord.Color.green())
                success_embed.set_footer(text="From {}".format(ctx.author))

                await interaction.response.send_message(embed=success_embed)

                await m.delete()
                v.stop()
            succ = discord.ui.Button(
                emoji=rand_btn, style=discord.ButtonStyle.gray)
            v.add_item(succ)
            succ.callback = now_callback
        else:
            d = discord.ui.Button(style=discord.ButtonStyle.gray, emoji=emoji)
            v.add_item(d)

            async def fail_callback(interaction: discord.Interaction) -> None:
                if interaction.user != ctx.user:
                    await interaction.response.send_message("This was not meant for you", ephemeral=True)
                    return
                failed_embed = discord.Embed(
                    title="Failed", description=f"You Failed bruh! the button was {rand_btn}", colour=discord.Color.red())
                failed_embed.set_footer(text="For {}".format(ctx.author))
                await interaction.response.send_message(embed=failed_embed)
                await m.delete()

                v.stop()
            d.callback = fail_callback
    m = await ctx.respond(
        embed=discord.Embed(title="Starting after 6 second(s)",
                            description="Get ready!", colour=discord.Color.green())
    )
    i = 5 # duration to wait
    while i != 0:
        await asyncio.sleep(1)
        await m.edit_original_message(embed=discord.Embed(title="Starting after {} seconds".format(i), description="Get ready!", colour=discord.Color.green()))
        i -= 1
    embed = discord.Embed(
        title="Reaction game", description=f"Lets do a reaction game\nthe emoji that i choose is...\n click the button with the {rand_btn} below", color=discord.Color.random())

    m = await m.edit_original_message(embed=embed, view=v)
    now = time.time()
try:
    bot.run(TOKEN)
except discord.errors.LoginFailure:
    print("Invalid token passed")
