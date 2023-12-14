import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import wapo_api
import services

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix='!')
channel_id = 1184096292905943120


@bot.command()
async def wapo(ctx):
    print(ctx)

    print(ctx.channel.id)

    if channel_id == ctx.channel.id:
        message = await ctx.send('Fetching URL...')

        try:
            url = wapo_api.get_todays_wapo_url()
            await message.edit(content=url)
        except Exception as e:
            await ctx.send(f'Error fetching URL: {e}')


@bot.command()
async def solution(ctx, hint, word_length):
    print(ctx)
    print(ctx.channel.id)

    if channel_id == ctx.channel.id:
        message = await ctx.send('Calculating solution...')

        try:
            solution = services.get_solution(word_length)
            await message.edit(content=solution)
        except Exception as e:
            await ctx.send(f'Error calculating solution: {e}')

bot.run(os.getenv("DISCORD_TOKEN"))
