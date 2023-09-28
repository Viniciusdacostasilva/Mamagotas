import discord
from discord.ext import commands

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!mamadas', intents=intents)

# Lista de palavras-alvo que o bot irá contar
palavras_alvo = ["mamada", "mamar", "mamou", "mamei", "mamo", "mamadeira", "mamalias"]

# Dicionário para armazenar contagens por palavra
contagens = {palavra: 0 for palavra in palavras_alvo}

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

@bot.event
async def on_message(message):
    # Verifica se a mensagem não foi enviada pelo próprio bot
    if message.author == bot.user:
        return

    # Converte a mensagem para letras minúsculas para evitar erros de capitalização
    mensagem = message.content.lower()

    # Verifica se alguma das palavras-alvo está presente na mensagem
    for palavra in palavras_alvo:
        if palavra in mensagem:
            # Atualiza a contagem para a palavra encontrada
            contagens[palavra] += 1

            # Responde à mensagem mencionando a contagem
            await message.channel.send(f"O charuto agora é outro, '{palavra}' foi mencionada {contagens[palavra]} vezes.")

    await bot.process_commands(message)

# Iniciar o bot com o token
bot.run('MTE1Njk4MzE2MDUzMDI5Mjc4OQ.GnzYiQ.4Iup4dNX4L0cRrfPjNnCMMUE8bOJYjwaMEtvmU')
