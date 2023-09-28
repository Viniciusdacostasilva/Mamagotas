import discord
from discord.ext import commands
from voices import voices, responses
import asyncio
import speech_recognition as sr
import random

# Token do seu bot do Discord
TOKEN = 'MTE1NzAwMjU5ODg4MTE2NTM2Mg.GYqse-.lrtVLz6qsFpGge2-WPFL97quc9MJ4wK-pfU5Fo'


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Variável para contar a quantidade de vezes que "mamou" ou "mamei" foi dito
count_mamou_mamei = 0

# Lista de respostas possíveis

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

@bot.command()
async def listen(ctx):
    global count_mamou_mamei  # Usamos 'global' para acessar a variável fora da função

    if ctx.author.voice:
        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()

        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 4000

        try:
            while True:
                with sr.Microphone() as source:
                    print("Estou ouvindo... Fale algo!")
                    audio = recognizer.listen(source)

                try:
                    recognized_text = recognizer.recognize_google(audio, language="pt-BR")
                    print("Texto reconhecido:", recognized_text)

                    for key in voices.keys():
                        if key in recognized_text.lower():
                            await ctx.send(voices[key], tts=True)
                        # Verifique se alguma das palavras-chave está presente no texto reconhecido
                        elif any(keyword in recognized_text.lower() for keyword in ["mama","mamei", "mamou", "mamada", "mamando", "cu"]):
                            response = random.choice(responses)
                            await ctx.send(f"{response}", tts=True)

                            # Verifique se "mamou" ou "mamei" está presente no texto reconhecido e atualize a contagem
                            if "mamou" in recognized_text.lower() or "mamei" in recognized_text.lower():
                                count_mamou_mamei += 1
                                await ctx.send(f"Quantidade de vezes que 'mamou' ou 'mamei' foi dito: {count_mamou_mamei}")

                    

                except sr.UnknownValueError:
                    print("Não foi possível reconhecer o áudio")

        except KeyboardInterrupt:
            print("Parando de ouvir...")
        finally:
            await voice_client.disconnect()
    else:
        await ctx.send("Você precisa estar em um canal de voz para usar este comando.")

bot.run(TOKEN)





