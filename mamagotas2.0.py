import discord
from discord.ext import commands
import asyncio
import speech_recognition as sr
import random

# Token do seu bot do Discord
TOKEN = 'MTE1NzAwMjU5ODg4MTE2NTM2Mg.GA2tCf.p8ILQpC9F_jaNAkn7YMkhKI26s5IxT7v4ntnks'


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Variável para contar a quantidade de vezes que "mamou" ou "mamei" foi dito
count_mamou_mamei = 0

# Lista de respostas possíveis
responses = ["Abra a boca então", "O charuto agora é outro", "Hmmmmmm", "Com 2 rabiscada, a caneta azul, já sai tinta"]

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

                    # Verifique se a frase exata "vamos ver" está presente no texto reconhecido
                    if "vamos ver" in recognized_text.lower():
                        await ctx.send("vamo ver ", tts=True)
            
                    # Verifique se a frase exata "botaram" está presente no texto reconhecido
                    elif "botaram" in recognized_text.lower():
                        await ctx.send("botaram ", tts=True)

                    # Verifique se a palavra "tá falando" está presente no texto reconhecido
                    elif "tá falando" in recognized_text.lower():
                        await ctx.send("ta falando comigo?", tts=True)

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





