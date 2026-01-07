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
        await bot.change_presence(activity=discord.Game(name="Servidor Offline 🔴"))

# ... puedes añadir aquí el comando !status que ya teníamos ...

bot.run(TOKEN)