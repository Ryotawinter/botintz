from datetime import datetime
import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
import os
token = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

saved_messages = {}
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    clear_builds.start()  # Start the task when the bot is ready
    await bot.tree.sync()

@tasks.loop(minutes=2)  # Runs every 1 minute
async def clear_builds():
    channel = bot.get_channel(1194425454094983279)
    print(channel)# Replace with your channel ID
    if channel:
        await channel.purge()

@clear_builds.before_loop
async def before_clear_builds():
    await bot.wait_until_ready()  # Wait for the bot to be ready before starting the loop

@bot.command()
async def urgente(ctx, *, message: str):
    print(message)
    for member in ctx.guild.members:
        if member != bot.user and not member.bot:
            try:
                await member.send(f":warning: Olhem a Aba de Avisos no Discord -{message} :warning:")
                await ctx.send(f'Mensagem enviada para {member.name}')
            except discord.Forbidden:
                await ctx.send(f'Não foi possível enviar a mensagem para {member.name}')

@tasks.loop(hours=24)  # Runs every 24 hours
async def daily_reminder():
    # Replace 'YOUR_CHANNEL_ID' with the ID of the channel where you want to send the reminder
    channel = bot.get_channel(1194463602116141117)

    if channel:
        now = datetime.utcnow()
        if now.hour == 11 and now.minute == 0:
            await channel.send('@everyone Não se esqueçam das metas semanais e dos hábitos! 💪📅')

@daily_reminder.before_loop
async def before_daily_reminder():
    await bot.wait_until_ready()  # Wait for the bot to be ready before starting the loop

@bot.command()
async def matchup(ctx, keyword: str):
    channel = ctx.channel

    if channel:
        matched_messages = []
        async for message in channel.history(limit=None):  # Limit=None busca todas as mensagens
            if message.author != bot.user and message.id != ctx.message.id and keyword.lower() in message.content.lower():
                matched_messages.append(message.content)

        if matched_messages:
            formatted_messages = "\n".join(matched_messages)
            msg = await ctx.send(f"Mensagens encontradas para a palavra-chave '{keyword}':\n{formatted_messages}")

            await asyncio.sleep(60)
            try:
                await msg.delete()
            except discord.Forbidden:
                pass
            # Exclui a mensagem de comando após ser enviada
            await ctx.message.delete()
        else:
            msg=await ctx.send(f"Nenhuma mensagem encontrada para a palavra-chave '{keyword}'")
            # Exclui a mensagem de comando após ser enviada mesmo se não houver correspondências
            await ctx.message.delete()
            await asyncio.sleep(2)
            await msg.delete()
    else:
        await ctx.send("Canal não encontrado ou indisponível.")

@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx):
    try:
        await ctx.channel.purge()
        msg = await ctx.send(f"O canal foi limpo por {ctx.author.mention}.")
        await msg.delete()
    except discord.Forbidden:
        await ctx.send("Não tenho permissão para apagar mensagens.")
    except discord.HTTPException:
        await ctx.send("Falha ao apagar as mensagens.")

bot.run(token)




