import discord
from discord.ext import commands
import asyncio
import speech_recognition as sr

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Configuração do reconhecimento de fala
r = sr.Recognizer()

# Palavras-chave para reconhecimento
keywords = ["mamei", "mamou", "mamar", "mamada"]
word_counts = {word: 0 for word in keywords}

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

@bot.command()
async def voice(ctx):
    if ctx.author.voice:
        # Conecta-se ao canal de voz do autor
        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()

        try:
            # Aguarda até que o usuário fale algo (10 segundos de gravação)
            await asyncio.sleep(10)

            # Grava o áudio do canal de voz em um arquivo temporário
            voice_client.stop()
            voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
            voice_client.source.volume = 1.0
            voice_client.source.readinto = lambda b: None  # Evita reprodução do áudio
            voice_client.source.seek(0)

            audio_data = voice_client.source
            with open("audio.wav", "wb") as f:
                while True:
                    chunk = audio_data.read(4096)
                    if not chunk:
                        break
                    f.write(chunk)

            # Reconhece o texto a partir do áudio
            with sr.AudioFile("audio.wav") as source:
                audio = r.record(source)
                print("Estou ouvindo... Fale algo!")
                recognized_text = r.recognize_google(audio, language="pt-BR")
                print("Texto reconhecido:", recognized_text)

                # Verifica as palavras-chave no texto reconhecido e atualiza as contagens
                for word in keywords:
                    if word in recognized_text.lower():
                        word_counts[word] += 1

                # Responde à mensagem com o texto reconhecido e as contagens
                await ctx.send(f"Texto reconhecido: {recognized_text}")
                await ctx.send(f"Contagens: {', '.join(f'{word}: {count}' for word, count in word_counts.items())}")
        except sr.UnknownValueError:
            await ctx.send("Não foi possível reconhecer o áudio")
        except Exception as e:
            await ctx.send(f"Ocorreu um erro: {str(e)}")

        # Desconecta-se do canal de voz
        await voice_client.disconnect()
    else:
        await ctx.send("Você precisa estar em um canal de voz para usar este comando.")

# Iniciar o bot com o token
bot.run('MTE1NzAwMjU5ODg4MTE2NTM2Mg.GggG5h.hT6v1jYhg3dLdPvn8QjzPzm4df-DbVKXmIgdgU')
