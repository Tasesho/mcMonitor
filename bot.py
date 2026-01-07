import discord
from discord.ext import commands
from mcstatus import JavaServer

# Configuración
TOKEN = 'MTQ1ODUzNjg0ODk2NzMzNjA4OQ.G2M-_V.5_WQHtNIfl-jGRMc8wxPxx8fsf29HkzgJeFbkU'
SERVER_IP = 'society-detroit.gl.joinmc.link' # Ejemplo: 'localhost' o '192.168.1.1'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command()
async def status(ctx):
    try:
        # Buscamos el servidor de Minecraft
        server = JavaServer.lookup(SERVER_IP)
        status = server.status()

        # Creamos un mensaje elegante (Embed)
        embed = discord.Embed(title="📊 Estado del Servidor", color=discord.Color.green())
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











#