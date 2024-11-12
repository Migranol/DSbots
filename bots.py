import discord
import requests
from discord.ext import commands, tasks

TOKEN = 'MTMwNTc3MzQyODk4NDUxNjY0OA.GTTU_q.IPwTw4ro4FkibFKygBErknf4w7n_oNC2uzBGms'
CHANNEL_ID = 123456789012345678  # Reemplaza con el ID del canal para los anuncios

# Configura el bot con prefijo "/"
bot = commands.Bot(command_prefix="/", intents=discord.Intents.default())

# Función para obtener datos de la tienda de Fortnite
def get_store_data():
    url = "https://fortnite-api.com/v2/shop/br"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Tarea periódica para enviar actualizaciones diarias de la tienda
@tasks.loop(hours=24)
async def daily_store_update():
    store_data = get_store_data()
    if store_data:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f"¡La tienda de Fortnite se ha actualizado! Aquí tienes la info: {store_data}")

# Comando /shopday para consultar la tienda actual
@bot.command(name="shopday")
async def shopday(ctx):
    store_data = get_store_data()
    if store_data:
        # Extrae y organiza los datos según la estructura de la API
        items = [item["name"] for item in store_data["data"]["daily"]["entries"]]
        items_list = "\n".join(items)
        await ctx.send(f"Items actuales en la tienda de Fortnite:\n{items_list}")
    else:
        await ctx.send("No se pudo obtener la información de la tienda en este momento.")

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    daily_store_update.start()

bot.run(TOKEN)
