# pip install discord.py requests

import discord
from discord.ext import commands, tasks
import requests

# Configuración del token de Discord y la API Key de FortniteAPI.io
TOKEN = ""
FORTNITE_API_KEY = ""

# Configurar los intents
intents = discord.Intents.default()
intents.message_content = True

# Configuración inicial del bot con intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Variable para almacenar el canal configurado por el usuario
user_channel = None


# Función para obtener la tienda de Fortnite desde el endpoint de FortniteAPI.io
def get_fortnite_shop():
    url = "https://fortniteapi.io/v2/shop?lang=en"
    headers = {"Authorization": FORTNITE_API_KEY}
    response = requests.get(url, headers=headers)

    # Verificar si la respuesta es exitosa
    if response.status_code == 200:
        data = response.json()
        items = []

        # Recorrer cada entrada en la tienda de Fortnite
        for entry in data.get('data', {}).get('entries', []):
            # Obtener el nombre del artículo
            item_name = entry.get('displayName', 'Artículo sin nombre')

            # Obtener el precio del artículo
            price = entry.get('finalPrice', 'Precio no disponible')

            # Intentar obtener la imagen del artículo
            image = None
            if entry.get('images'):
                image = entry['images'].get('icon') or entry['images'].get(
                    'full_background')
            elif entry.get('displayAssets'):
                image = entry['displayAssets'][0].get(
                    'url') if entry['displayAssets'] else None

            # Formatear la información del artículo
            item_info = f"**{item_name}** - {price} V-Bucks\n{image}\n" if image else f"**{item_name}** - {price} V-Bucks\nSin imagen disponible\n"
            items.append(item_info)

        # Dividir el mensaje en fragmentos de 2000 caracteres si es necesario
        return [items[i:i + 2000] for i in range(0, len(items), 2000)]
    else:
        print("Error al obtener la tienda de Fortnite.")
        return ["No se pudo obtener la tienda de Fortnite."]


# Comando para que los administradores configuren el canal de anuncios
@bot.command(name="set_channel")
@commands.has_permissions(administrator=True)
async def set_channel(ctx):
    global user_channel
    user_channel = ctx.channel.id
    await ctx.send(f"Canal configurado correctamente: {ctx.channel.name}")


@bot.command(name="shopday")
async def shopday(ctx):
    print("Comando !shopday llamado")
    await ctx.send("Probando envío de mensaje...")  # Mensaje de prueba
    shop_info_parts = get_fortnite_shop()
    print(shop_info_parts)

    if shop_info_parts:
        for part in shop_info_parts:
            await ctx.send(part)
    else:
        await ctx.send("No se encontró información de la tienda.")


# Tarea que envía el anuncio de la tienda cada 24 horas
@tasks.loop(hours=24)
async def daily_shop_announcement():
    if user_channel:
        channel = bot.get_channel(user_channel)
        if channel:
            shop_info = get_fortnite_shop()
            for part in shop_info:
                await channel.send(part)


# Inicia la tarea de anuncio diario cuando el bot se conecta
@bot.event
async def on_ready():
    daily_shop_announcement.start()
    print(f'{bot.user} se ha conectado a Discord.')


# Comando de ayuda para mostrar los comandos disponibles
@bot.command(name="bothelp")
async def bothelp(ctx):
    help_message = (
        "**Comandos disponibles:**\n"
        "`!set_channel` - Establece el canal para las notificaciones diarias de la tienda.\n"
        "`!shopday` - Muestra la tienda de Fortnite del día en el canal actual.\n"
        "`!ping` - Comando de prueba para verificar que el bot está activo.\n")
    await ctx.send(help_message)


# Comando de prueba para verificar que el bot responde
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command(name="opinion")
async def opinion(ctx):
    await ctx.send("Yo opino que el pedrito gomez es wekito")


# Manejo de errores para depuración
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Error: {error}")


# Ejecuta el bot
bot.run(TOKEN)
