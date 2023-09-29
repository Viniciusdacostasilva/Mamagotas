import discord
from discord.ext import commands
from chatterbot import ChatBot

# Crie o chatbot
mamagotas = ChatBot('Mamagotas')

# Configuração do bot do Discord
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Bot está pronto como {bot.user.name}')

@bot.command()
async def chat(ctx, *, question):
    response = mamagotas.get_response(question)
    await ctx.send(f'Mamagotas: {response}')

# Inicialize o bot do Discord
bot.run('TOKEN_DO_SEU_BOT')  # Substitua 'TOKEN_DO_SEU_BOT' pelo token do seu bot do Discord
