# pip install discord.py python-dotenv

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os

# Cargar el token del archivo .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configuración inicial del bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

# Variable para almacenar el canal configurado por el usuario
user_channel = None

# Comando para que los administradores configuren el canal de anuncios
@bot.command(name="set_channel")
@commands.has_permissions(administrator=True)
async def set_channel(ctx):
    global user_channel
    user_channel = ctx.channel.id
    await ctx.send(f"Canal configurado correctamente: {ctx.channel.name}")

# Comando para consultar la tienda de Fortnite en cualquier momento
@bot.command(name="shopday")
async def shopday(ctx):
    shop_info = get_fortnite_shop()  # función ficticia para obtener la tienda
    await ctx.send(f"**Tienda de Fortnite hoy:**\n{shop_info}")

# Tarea que envía el anuncio de la tienda cada 24 horas
@tasks.loop(hours=24)
async def daily_shop_announcement():
    if user_channel:
        channel = bot.get_channel(user_channel)
        if channel:
            shop_info = get_fortnite_shop()  # función ficticia para obtener la tienda
            await channel.send(f"**Anuncio diario de la tienda de Fortnite:**\n{shop_info}")

# Función ficticia para obtener la tienda de Fortnite (deberías completar esta función)
def get_fortnite_shop():
    return "Información de la tienda del día..."

# Inicia la tarea de anuncio diario cuando el bot se conecta
@bot.event
async def on_ready():
    daily_shop_announcement.start()
    print(f'{bot.user} se ha conectado a Discord.')

bot.run(TOKEN)
