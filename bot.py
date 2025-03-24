import discord
import requests
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv

# Cargar el token desde el archivo .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))  # Asegúrate de tener el ID correcto del canal

# Crear el bot
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

# Función para obtener actualizaciones desde la API de GitHub de CPython
def get_cpython_updates():
    url = "https://api.github.com/repos/python/cpython/commits"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Función para enviar las noticias al canal de Discord
async def send_updates_to_discord():
    updates = get_cpython_updates()
    
    if updates:
        for update in updates[:5]:  # Mostrar las 5 últimas actualizaciones
            message = f"**{update['commit']['message']}**\n" \
                      f"Por {update['commit']['author']['name']}\n" \
                      f"Enlace: {update['html_url']}"
            
            # Enviar el mensaje al canal de Discord
            channel = client.get_channel(CHANNEL_ID)
            if channel:
                await channel.send(message)
            else:
                print(f"Canal con ID {CHANNEL_ID} no encontrado.")
    else:
        print("No se encontraron actualizaciones en la API.")

# Tarea para verificar las actualizaciones cada 10 minutos
@tasks.loop(minutes=10)
async def check_updates():
    await send_updates_to_discord()

# Evento cuando el bot está listo
@client.event
async def on_ready():
    print(f"Bot conectado como {client.user}")
    check_updates.start()  # Iniciar la tarea de verificar actualizaciones

# Iniciar el bot
client.run(TOKEN)
