import discord
from discord.ext import commands
import youtube_dl
import asyncio

# Configuração do bot
intents = discord.Intents.default()
intents.typing = False  # Isso desativa o intent de "digitação" (opcional)

bot = commands.Bot(command_prefix='!', intents=intents)

# Configurações do player de música
players = {}

# Função para criar o player de música
def create_player(ctx):
    player = players.get(ctx.guild.id)
    if not player:
        player = MusicPlayer(ctx)
        players[ctx.guild.id] = player
    return player

# Classe para gerenciar a reprodução de música
class MusicPlayer:
    def __init__(self, ctx):
        self.ctx = ctx
        self.voice_channel = ctx.author.voice.channel
        self.voice_client = None
        self.queue = []
        self.is_playing = False

    async def join_voice_channel(self):
        if self.voice_client is not None and self.voice_client.is_connected():
            return

        self.voice_client = await self.voice_channel.connect()

    async def disconnect_voice_channel(self):
        if self.voice_client is not None and self.voice_client.is_connected():
            await self.voice_client.disconnect()
            self.voice_client = None

    async def play_next(self):
        if not self.queue:
            self.is_playing = False
            return

        url = self.queue.pop(0)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']

        self.voice_client.play(discord.FFmpegPCMAudio(url2, executable="ffmpeg", options="-vn"))
        self.is_playing = True

    def add_to_queue(self, url):
        self.queue.append(url)

    def pause(self):
        if self.voice_client.is_playing():
            self.voice_client.pause()

    def resume(self):
        if self.voice_client.is_paused():
            self.voice_client.resume()

    def stop(self):
        if self.voice_client.is_playing() or self.voice_client.is_paused():
            self.voice_client.stop()
            self.is_playing = False

# Comando para tocar música
@bot.command()
async def play(ctx, url):
    player = create_player(ctx)
    await player.join_voice_channel()
    player.add_to_queue(url)
    if not player.is_playing:
        await player.play_next()

# Comando para pausar a música
@bot.command()
async def pause(ctx):
    player = create_player(ctx)
    player.pause()

# Comando para retomar a música
@bot.command()
async def resume(ctx):
    player = create_player(ctx)
    player.resume()

# Comando para parar a música
@bot.command()
async def stop(ctx):
    player = create_player(ctx)
    player.stop()

# Comando para mostrar a fila de reprodução
@bot.command()
async def queue(ctx):
    player = create_player(ctx)
    if not player.queue:
        await ctx.send("A fila de reprodução está vazia.")
        return

    queue_message = "Fila de reprodução:\n"
    for index, url in enumerate(player.queue, start=1):
        queue_message += f"{index}. {url}\n"

    await ctx.send(queue_message)

# Evento de inicialização do bot
@bot.event
async def on_ready():
    print(f'Bot está online como {bot.user.name}')

# Iniciar o bot com o token
bot.run('MTE1NzcwNjYxNjcwODI4MDM4MA.GkL-aY.Fu-yVaVZhrQeY9d_ygSADwAEA9xLSb4g4HekhU')
