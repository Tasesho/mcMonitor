import discord
import os
from discord.ext import commands, tasks
from mcstatus import JavaServer
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER_IP = os.getenv('MC_SERVER_IP')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot iniciado como {bot.user}')
    update_status.start()

@tasks.loop(seconds=60)
async def update_status():
    try:
        server = JavaServer.lookup(SERVER_IP)
        status = server.status()
        await bot.change_presence(activity=discord.Game(name=f"MC: {status.players.online} online"))
    except:
        await bot.change_presence(activity=discord.Game(name="Servidor Offline "))


@bot.command()
async def status(ctx):
    try:
        # Buscamos el servidor de Minecraft
        server = JavaServer.lookup(SERVER_IP)
        status = server.status()

        # Creamos un mensaje elegante (Embed)
        embed = discord.Embed(title=" Estado del Servidor", color=discord.Color.green())
        embed.add_field(name="Estado", value=" Online", inline=True)
        embed.add_field(name="Jugadores", value=f"{status.players.online}/{status.players.max}", inline=True)
        embed.add_field(name="Ping", value=f"{round(status.latency, 2)} ms", inline=True)
        
        if status.players.sample:
            names = ", ".join([p.name for p in status.players.sample])
            embed.add_field(name="Conectados", value=names, inline=False)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f" El servidor está offline o no se pudo conectar.\nError: {e}")


bot.run(TOKEN)