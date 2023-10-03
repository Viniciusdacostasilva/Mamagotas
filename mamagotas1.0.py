import discord
from discord.ext import commands
import voices  # Importe o módulo voices.py se você o tiver
from discord import FFmpegPCMAudio
import asyncio

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
# Antes de importar FFmpegPCMAudio, especifique o caminho para o executável do FFmpeg

bot = commands.Bot(command_prefix='!', intents=intents)

# Lista de palavras-alvo que o bot irá contar
palavras_alvo = ["mamada", "mamar", "mamou",
                 "mamei", "mamo", "mamadeira", "mamalias", "mama", "mamaste", "mamaram"]

# Dicionário para armazenar contagens por palavra para cada usuário
contagens_por_usuario = {}
ranks_por_usuario = {}
usuarios_ordenados = {}
# Dicionário para armazenar contagens globais de mamadas
contagem_global = {palavra: 0 for palavra in palavras_alvo}

# Lista para armazenar IDs de mensagens já respondidas
mensagens_respondidas = []

# -------------------------------------------------------------------------------------------------------------------


@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    # Canal onde você deseja enviar a mensagem de boas-vindas
    channel_id = 1157815827811270726  # Substitua pelo ID do canal desejado

    # Mensagem de boas-vindas ao ser iniciado
    welcome_message = "Como posso te ajudar a mamar hoje?"

    # Envia a mensagem de boas-vindas para o canal
    channel = bot.get_channel(channel_id)
    await channel.send(welcome_message)

# -------------------------------------------------------------------------------------------------------------------


@bot.event
async def on_message(message):
    # Verifica se a mensagem não foi enviada pelo próprio bot
    if message.author == bot.user:
        return

    # Converte a mensagem para letras minúsculas para evitar erros de capitalização
    mensagem = message.content.lower()

    # Verificar e atribuir ranks ao usuário
    novo_rank = await verificar_e_atribuir_rank(message.author.id)

    # Enviar mensagem de parabéns se o rank mudou
    if novo_rank:
        await message.channel.send(f"Parabéns, {message.author.mention}! Você agora é uma **{novo_rank}**.")

    # Verifica se alguma das palavras-alvo está presente na mensagem
    for palavra in palavras_alvo:
        if palavra in mensagem:
            # Atualiza a contagem global
            contagem_global[palavra] += 1

            # Atualiza a contagem para o usuário específico
            if message.author.id not in contagens_por_usuario:
                contagens_por_usuario[message.author.id] = {palavra: 1}
            else:
                if palavra not in contagens_por_usuario[message.author.id]:
                    contagens_por_usuario[message.author.id][palavra] = 1
                else:
                    contagens_por_usuario[message.author.id][palavra] += 1

            # Responde à mensagem mencionando a contagem
            await message.channel.send(f"🍼 {message.author.mention} efetuou {contagens_por_usuario[message.author.id][palavra]} mamada(s) de {palavra}.")

    # Verifica se a mensagem contém uma palavra-chave no arquivo voices.py
    for palavra, resposta in voices.voices.items():
        if palavra in mensagem:
            # Envia a resposta correspondente para o canal
            await message.channel.send(resposta)

    # Verifica se a palavra "macaco" está presente na mensagem e se a mensagem já foi respondida
    if "macaco" in mensagem and message.id not in mensagens_respondidas:
        # Responde com informações sobre o local com mais macacos do planeta e uma imagem
        resposta = "O local com mais macacos do planeta é a Floresta Amazônica, que abriga diversas espécies de macacos, incluindo o macaco-aranha, o macaco-prego e muitos outros."
        imagem_url = "https://pbs.twimg.com/ext_tw_video_thumb/1272362036996046848/pu/img/0tFr0drERAvJMEJd.jpg"
        await message.channel.send(resposta)
        await message.channel.send(imagem_url)

    # Verifica se a palavra "chupetao" está presente na mensagem e se a mensagem já foi respondida
    if "chupetao" in mensagem and message.id not in mensagens_respondidas:
        # Responde com informações sobre o local com mais macacos do planeta e uma imagem
        imagem_url = "https://cdn.discordapp.com/attachments/1026944137129369603/1157829510197153913/image.png?ex=651a0842&is=6518b6c2&hm=557007425c1fe0567747cc929f60961581361b351d967aec75ae2200cf9d4c37&"
        await message.channel.send(imagem_url)

        # Verifica se a palavra "chupetao" está presente na mensagem e se a mensagem já foi respondida
    if ("ao mossar" in mensagem or "almoçar" in mensagem) and message.id not in mensagens_respondidas:
        # Se "ao mossar" ou "almoçar" estiverem na mensagem e a mensagem não foi respondida
        imagem_url = "https://cdn.discordapp.com/attachments/1026944137129369603/1158077718945087630/54813dad2906ec01b02064220b1ecfe451c3117dd9d836c92c0a5c9912488697_1.png?ex=651aef6c&is=65199dec&hm=bb0a1c6fa55496f8d083eb5ab7e9df6ceddb5bfb986980c0a64fdb9dc99e084d&"
        await message.channel.send(imagem_url)
    # Adiciona o ID da mensagem às mensagens já respondidas
    mensagens_respondidas.append(message.id)

    await bot.process_commands(message)
# -------------------------------------------------------------------------------------------------------------------

# Comando !ajuda


@bot.command()
async def ajuda(ctx):
    # Cria uma mensagem de ajuda
    help_message = """
    **Comandos disponíveis:**
    `!mamadas` - Conta o número de mamadas efetuadas por você.
    `!mamadaslog` - Diz o número de vezes que cada derivação do verbo mamar foi dito por todos usuários.
    `!mamadaglobal` - Conta o número de mamadas efetuadas por todos usúarios.
    `!ajuda` - Exibe a lista de comandos disponíveis.
    `!elo` - Exibe seu elo nas mamadas.
    `!top` - Exibe os top mamadores.
    **Fotos disponíveis:**
    `macaco` - Exibe o local com a maior quantidade de macacos do mundo.
    `chupetao` - Exibe o chupetão.
    `almoçar` ou  `ao mossar`- Exibe se já está podendo almossar.
    **Efeitos sonoros:**
    `!boanoite` - Reproduz um boa noite quente e aconchegante.
    `!vamo` - Reproduz o aúdio "Vamo ver o cú dele".
    `!satanas` - Reproduz um aúdio saído do inferno.
    `!caneta` - Reproduz uma das falas icônicas de Manoel Gomes.
    `!macaco` - Reproduz um aúdio de macaco.
    `!lula` - Reproduz um aúdio de macaco.
    `!heroi` - Reproduz um aúdio do Smzinho.
    `!pix` - Reproduz um aúdio do pix.
    `!gosta` - Reproduz um aúdio do ELE GOSTA.
    `!ui` - Reproduz um aúdio do UIIII.
    `!demais` - Reproduz um aúdio do DEMAIS.
    `!cavalo` - Reproduz um aúdio do CAVALO.
    """

    # Envia a mensagem de ajuda para o canal
    await ctx.send(help_message)

# -------------------------------------------------------------------------------------------------------------------
# Comando !mamadas para verificar a quantidade de mamadas do usuário


@bot.command()
async def mamadas(ctx):
    # Verifica se o usuário possui contagens
    if ctx.author.id in contagens_por_usuario:
        contagem_usuario = contagens_por_usuario[ctx.author.id]
        mensagem_contagem = f"Suas mamadas 🍼({ctx.author.mention}):"
        for palavra, contagem in contagem_usuario.items():
            mensagem_contagem += f"🍼 {palavra}: {contagem} vezes/"
        await ctx.send(mensagem_contagem)
    else:
        await ctx.send(f"{ctx.author.mention}, você não efetuou nenhuma mamada ainda.")
# -------------------------------------------------------------------------------------------------------------------

# Comando !mamadaslog para verificar cada verbo de mamar


@bot.command()
async def mamadaslog(ctx):
    mensagem_contagem_global = "Contagem global de mamadas:\n"
    for palavra, contagem in contagem_global.items():
        mensagem_contagem_global += f"🍼 {palavra}: {contagem} vezes\n"
    await ctx.send(mensagem_contagem_global)
# -------------------------------------------------------------------------------------------------------------------
# Comando !mamada global para verificar a quantidade global de mamadas


@bot.command()
async def mamadaglobal(ctx):
    # Calcule a contagem total global somando as contagens individuais
    total_global = sum(contagem_global.values())

    # Crie a mensagem com a contagem total global
    mensagem_contagem_global = f"Mamadas globais: {total_global} vezes"

    # Envie a mensagem com a contagem total global
    await ctx.send(mensagem_contagem_global)
# -------------------------------------------------------------------------------------------------------------------

# Dicionário para armazenar os ranks dos usuários
ranks_por_usuario = {}

# -------------------------------------------------------------------------------------------------------------------
# Função para verificar e atribuir ranks


async def verificar_e_atribuir_rank(usuario_id):
    if usuario_id in contagens_por_usuario:
        contagem_usuario = sum(contagens_por_usuario[usuario_id].values())
        if contagem_usuario >= 10:
            novo_rank = "Boquinha de Viludo 👅"
        elif contagem_usuario >= 5:
            novo_rank = "Boquinha Doce 🍬"
        else:
            novo_rank = "Boquinha Cansada 🥱"

        if ranks_por_usuario.get(usuario_id) != novo_rank:
            ranks_por_usuario[usuario_id] = novo_rank
            return novo_rank
        return None

# Comando para !elo


@bot.command()
async def elo(ctx):
    if ctx.author.id in ranks_por_usuario:
        elo = ranks_por_usuario[ctx.author.id]
        await ctx.send(f"{ctx.author.mention}, seu elo atual é: **{elo}**")

    else:
        await ctx.send(f"{ctx.author.mention}, você não efetuou nenhuma mamada ainda e é uma Boquinha cansada 🥱.")
# -------------------------------------------------------------------------------------------------------------------
# Comando para !top


@bot.command()
async def top(ctx):
    usuarios_ordenados = sorted(contagens_por_usuario.items(
    ), key=lambda x: sum(x[1].values()), reverse=True)
    # Monta uma mensagem com o ranking
    mensagem_ranking = "Top Mamadores 🍼:\n"
    for posicao, (usuario_id, contagem_usuario) in enumerate(usuarios_ordenados, start=1):
        usuario = await bot.fetch_user(int(usuario_id))
        total_mamadas = sum(contagem_usuario.values())
        mensagem_ranking += f"{posicao}. {usuario.name}: {total_mamadas} mamadas\n"

    await ctx.send(mensagem_ranking)

# -------------------------------------------------------------------------------------------------------------------
# Comando !vamo


@bot.command()
async def vamo(ctx):
    # Verifique se o autor da mensagem está em um canal de voz
    if ctx.author.voice is None:
        await ctx.send('Você precisa estar em um canal de voz para usar esse comando.')
        return

    # Obtenha o canal de voz do autor da mensagem
    voice_channel = ctx.author.voice.channel

    # Conecte o bot ao canal de voz
    voice_client = await voice_channel.connect()

    # Especifique o caminho completo para o executável do FFmpeg
    # Substitua pelo caminho correto
    ffmpeg_path = 'C:/Users/Vinícius/Downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe'

    # Reproduza um arquivo de áudio (substitua 'seu_audio.mp3' pelo seu arquivo de áudio)
    audio_source = FFmpegPCMAudio(
        'C:/Users/Vinícius/Desktop/Bot discord/audios/vamo.mp3', executable=ffmpeg_path)

    # Inicie a reprodução do áudio
    voice_client.play(audio_source)

    # Aguarde até que a reprodução termine
    while voice_client.is_playing():
        await asyncio.sleep(1)

    # Espere mais 5 segundos e desconecte o bot do canal de voz
    await asyncio.sleep(5)
    await voice_client.disconnect()

# -------------------------------------------------------------------------------------------------------------------
# Comando !satanas


@bot.command()
async def satanas(ctx):
    # Verifique se o autor da mensagem está em um canal de voz
    if ctx.author.voice is None:
        await ctx.send('Você precisa estar em um canal de voz para usar esse comando.')
        return

    # Obtenha o canal de voz do autor da mensagem
    voice_channel = ctx.author.voice.channel

    # Conecte o bot ao canal de voz
    voice_client = await voice_channel.connect()

    # Especifique o caminho completo para o executável do FFmpeg
    # Substitua pelo caminho correto
    ffmpeg_path = 'C:/Users/Vinícius/Downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe'

    # Reproduza um arquivo de áudio (substitua 'seu_audio.mp3' pelo seu arquivo de áudio)
    audio_source = FFmpegPCMAudio(
        'C:/Users/Vinícius/Desktop/Bot discord/audios/project_satanas.mp3', executable=ffmpeg_path)

    # Inicie a reprodução do áudio
    voice_client.play(audio_source)

    # Aguarde até que a reprodução termine
    while voice_client.is_playing():
        await asyncio.sleep(1)

    # Espere mais 5 segundos e desconecte o bot do canal de voz
    await asyncio.sleep(5)
    await voice_client.disconnect()
# -------------------------------------------------------------------------------------------------------------------
# Comando !boanoite


@bot.command()
async def boanoite(ctx):
    # Verifique se o autor da mensagem está em um canal de voz
    if ctx.author.voice is None:
        await ctx.send('Você precisa estar em um canal de voz para usar esse comando.')
        return

    # Obtenha o canal de voz do autor da mensagem
    voice_channel = ctx.author.voice.channel

    # Conecte o bot ao canal de voz
    voice_client = await voice_channel.connect()

    # Especifique o caminho completo para o executável do FFmpeg
    # Substitua pelo caminho correto
    ffmpeg_path = 'C:/Users/Vinícius/Downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe'

    # Reproduza um arquivo de áudio (substitua 'seu_audio.mp3' pelo seu arquivo de áudio)
    audio_source = FFmpegPCMAudio(
        'C:/Users/Vinícius/Desktop/Bot discord/audios/jota.mp3', executable=ffmpeg_path)

    # Inicie a reprodução do áudio
    voice_client.play(audio_source)

    # Aguarde até que a reprodução termine
    while voice_client.is_playing():
        await asyncio.sleep(1)

    # Espere mais 5 segundos e desconecte o bot do canal de voz
    await asyncio.sleep(5)
    await voice_client.disconnect()
# -------------------------------------------------------------------------------------------------------------------
# Comando !caneta


@bot.command()
async def caneta(ctx):
    # Verifique se o autor da mensagem está em um canal de voz
    if ctx.author.voice is None:
        await ctx.send('Você precisa estar em um canal de voz para usar esse comando.')
        return

    # Obtenha o canal de voz do autor da mensagem
    voice_channel = ctx.author.voice.channel

    # Conecte o bot ao canal de voz
    voice_client = await voice_channel.connect()

    # Especifique o caminho completo para o executável do FFmpeg
    # Substitua pelo caminho correto
    ffmpeg_path = 'C:/Users/Vinícius/Downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe'

    # Reproduza um arquivo de áudio (substitua 'seu_audio.mp3' pelo seu arquivo de áudio)
    audio_source = FFmpegPCMAudio(
        'C:/Users/Vinícius/Desktop/Bot discord/audios/caneta.mp3', executable=ffmpeg_path)

    # Inicie a reprodução do áudio
    voice_client.play(audio_source)

    # Aguarde até que a reprodução termine
    while voice_client.is_playing():
        await asyncio.sleep(1)

    # Espere mais 5 segundos e desconecte o bot do canal de voz
    await asyncio.sleep(5)
    await voice_client.disconnect()

# -------------------------------------------------------------------------------------------------------------------
# Comando !macaco


@bot.command()
async def macaco(ctx):
    # Verifique se o autor da mensagem está em um canal de voz
    if ctx.author.voice is None:
        await ctx.send('Você precisa estar em um canal de voz para usar esse comando.')
        return

    # Obtenha o canal de voz do autor da mensagem
    voice_channel = ctx.author.voice.channel

    # Conecte o bot ao canal de voz
    voice_client = await voice_channel.connect()

    # Especifique o caminho completo para o executável do FFmpeg
    # Substitua pelo caminho correto
    ffmpeg_path = 'C:/Users/Vinícius/Downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe'

    # Reproduza um arquivo de áudio (substitua 'seu_audio.mp3' pelo seu arquivo de áudio)
    audio_source = FFmpegPCMAudio(
        'C:/Users/Vinícius/Desktop/Bot discord/audios/macaco.mp3', executable=ffmpeg_path)

    # Inicie a reprodução do áudio
    voice_client.play(audio_source)

    # Aguarde até que a reprodução termine
    while voice_client.is_playing():
        await asyncio.sleep(1)

    # Espere mais 5 segundos e desconecte o bot do canal de voz
    await asyncio.sleep(5)
    await voice_client.disconnect()

@bot.command()
async def lula(ctx):
    # Verifique se o autor da mensagem está em um canal de voz
    if ctx.author.voice is None:
        await ctx.send('Você precisa estar em um canal de voz para usar esse comando.')
        return

    # Obtenha o canal de voz do autor da mensagem
    voice_channel = ctx.author.voice.channel

    # Conecte o bot ao canal de voz
    voice_client = await voice_channel.connect()

    # Especifique o caminho completo para o executável do FFmpeg
    # Substitua pelo caminho correto
    ffmpeg_path = 'C:/Users/Vinícius/Downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe'

    # Reproduza um arquivo de áudio (substitua 'seu_audio.mp3' pelo seu arquivo de áudio)
    audio_source = FFmpegPCMAudio(
        'C:/Users/Vinícius/Desktop/Bot discord/audios/lula-tira.mp3', executable=ffmpeg_path)

    # Inicie a reprodução do áudio
    voice_client.play(audio_source)

    # Aguarde até que a reprodução termine
    while voice_client.is_playing():
        await asyncio.sleep(1)

    # Espere mais 5 segundos e desconecte o bot do canal de voz
    await asyncio.sleep(5)
    await voice_client.disconnect()

@bot.command()
async def heroi(ctx):
    # Verifique se o autor da mensagem está em um canal de voz
    if ctx.author.voice is None:
        await ctx.send('Você precisa estar em um canal de voz para usar esse comando.')
        return

    # Obtenha o canal de voz do autor da mensagem
    voice_channel = ctx.author.voice.channel

    # Conecte o bot ao canal de voz
    voice_client = await voice_channel.connect()

    # Especifique o caminho completo para o executável do FFmpeg
    # Substitua pelo caminho correto
    ffmpeg_path = 'C:/Users/Vinícius/Downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe'

    # Reproduza um arquivo de áudio (substitua 'seu_audio.mp3' pelo seu arquivo de áudio)
    audio_source = FFmpegPCMAudio(
        'C:/Users/Vinícius/Desktop/Bot discord/audios/heroi.mp3', executable=ffmpeg_path)

    # Inicie a reprodução do áudio
    voice_client.play(audio_source)

    # Aguarde até que a reprodução termine
    while voice_client.is_playing():
        await asyncio.sleep(1)

    # Espere mais 5 segundos e desconecte o bot do canal de voz
    await asyncio.sleep(5)
    await voice_client.disconnect()

@bot.command()
async def pix(ctx):
    # Verifique se o autor da mensagem está em um canal de voz
    if ctx.author.voice is None:
        await ctx.send('Você precisa estar em um canal de voz para usar esse comando.')
        return

    # Obtenha o canal de voz do autor da mensagem
    voice_channel = ctx.author.voice.channel

    # Conecte o bot ao canal de voz
    voice_client = await voice_channel.connect()

    # Especifique o caminho completo para o executável do FFmpeg
    # Substitua pelo caminho correto
    ffmpeg_path = 'C:/Users/Vinícius/Downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe'

    # Reproduza um arquivo de áudio (substitua 'seu_audio.mp3' pelo seu arquivo de áudio)
    audio_source = FFmpegPCMAudio(
        'C:/Users/Vinícius/Desktop/Bot discord/audios/pix.mp3', executable=ffmpeg_path)

    # Inicie a reprodução do áudio
    voice_client.play(audio_source)

    # Aguarde até que a reprodução termine
    while voice_client.is_playing():
        await asyncio.sleep(1)

    # Espere mais 5 segundos e desconecte o bot do canal de voz
    await asyncio.sleep(5)
    await voice_client.disconnect()

@bot.command()
async def gosta(ctx):
    # Verifique se o autor da mensagem está em um canal de voz
    if ctx.author.voice is None:
        await ctx.send('Você precisa estar em um canal de voz para usar esse comando.')
        return

    # Obtenha o canal de voz do autor da mensagem
    voice_channel = ctx.author.voice.channel

    # Conecte o bot ao canal de voz
    voice_client = await voice_channel.connect()

    # Especifique o caminho completo para o executável do FFmpeg
    # Substitua pelo caminho correto
    ffmpeg_path = 'C:/Users/Vinícius/Downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe'

    # Reproduza um arquivo de áudio (substitua 'seu_audio.mp3' pelo seu arquivo de áudio)
    audio_source = FFmpegPCMAudio(
        'C:/Users/Vinícius/Desktop/Bot discord/audios/gosta.mp3', executable=ffmpeg_path)

    # Inicie a reprodução do áudio
    voice_client.play(audio_source)

    # Aguarde até que a reprodução termine
    while voice_client.is_playing():
        await asyncio.sleep(1)

    # Espere mais 5 segundos e desconecte o bot do canal de voz
    await asyncio.sleep(5)
    await voice_client.disconnect()

@bot.command()
async def ui(ctx):
    # Verifique se o autor da mensagem está em um canal de voz
    if ctx.author.voice is None:
        await ctx.send('Você precisa estar em um canal de voz para usar esse comando.')
        return

    # Obtenha o canal de voz do autor da mensagem
    voice_channel = ctx.author.voice.channel

    # Conecte o bot ao canal de voz
    voice_client = await voice_channel.connect()

    # Especifique o caminho completo para o executável do FFmpeg
    # Substitua pelo caminho correto
    ffmpeg_path = 'C:/Users/Vinícius/Downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe'

    # Reproduza um arquivo de áudio (substitua 'seu_audio.mp3' pelo seu arquivo de áudio)
    audio_source = FFmpegPCMAudio(
        'C:/Users/Vinícius/Desktop/Bot discord/audios/ui.mp3', executable=ffmpeg_path)

    # Inicie a reprodução do áudio
    voice_client.play(audio_source)

    # Aguarde até que a reprodução termine
    while voice_client.is_playing():
        await asyncio.sleep(1)

    # Espere mais 5 segundos e desconecte o bot do canal de voz
    await asyncio.sleep(5)
    await voice_client.disconnect()

@bot.command()
async def demais(ctx):
    # Verifique se o autor da mensagem está em um canal de voz
    if ctx.author.voice is None:
        await ctx.send('Você precisa estar em um canal de voz para usar esse comando.')
        return

    # Obtenha o canal de voz do autor da mensagem
    voice_channel = ctx.author.voice.channel

    # Conecte o bot ao canal de voz
    voice_client = await voice_channel.connect()

    # Especifique o caminho completo para o executável do FFmpeg
    # Substitua pelo caminho correto
    ffmpeg_path = 'C:/Users/Vinícius/Downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe'

    # Reproduza um arquivo de áudio (substitua 'seu_audio.mp3' pelo seu arquivo de áudio)
    audio_source = FFmpegPCMAudio(
        'C:/Users/Vinícius/Desktop/Bot discord/audios/demais.mp3', executable=ffmpeg_path)

    # Inicie a reprodução do áudio
    voice_client.play(audio_source)

    # Aguarde até que a reprodução termine
    while voice_client.is_playing():
        await asyncio.sleep(1)

    # Espere mais 5 segundos e desconecte o bot do canal de voz
    await asyncio.sleep(5)
    await voice_client.disconnect()

@bot.command()
async def dança(ctx):
    # Verifique se o autor da mensagem está em um canal de voz
    if ctx.author.voice is None:
        await ctx.send('Você precisa estar em um canal de voz para usar esse comando.')
        return

    # Obtenha o canal de voz do autor da mensagem
    voice_channel = ctx.author.voice.channel

    # Conecte o bot ao canal de voz
    voice_client = await voice_channel.connect()

    # Especifique o caminho completo para o executável do FFmpeg
    # Substitua pelo caminho correto
    ffmpeg_path = 'C:/Users/Vinícius/Downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe'

    # Reproduza um arquivo de áudio (substitua 'seu_audio.mp3' pelo seu arquivo de áudio)
    audio_source = FFmpegPCMAudio(
        'C:/Users/Vinícius/Desktop/Bot discord/audios/dança.mp3', executable=ffmpeg_path)

    # Inicie a reprodução do áudio
    voice_client.play(audio_source)

    # Aguarde até que a reprodução termine
    while voice_client.is_playing():
        await asyncio.sleep(1)

    # Espere mais 5 segundos e desconecte o bot do canal de voz
    await asyncio.sleep(5)
    await voice_client.disconnect()


@bot.command()
async def cavalo(ctx):
    # Verifique se o autor da mensagem está em um canal de voz
    if ctx.author.voice is None:
        await ctx.send('Você precisa estar em um canal de voz para usar esse comando.')
        return

    # Obtenha o canal de voz do autor da mensagem
    voice_channel = ctx.author.voice.channel

    # Conecte o bot ao canal de voz
    voice_client = await voice_channel.connect()

    # Especifique o caminho completo para o executável do FFmpeg
    # Substitua pelo caminho correto
    ffmpeg_path = 'C:/Users/Vinícius/Downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe'

    # Reproduza um arquivo de áudio (substitua 'seu_audio.mp3' pelo seu arquivo de áudio)
    audio_source = FFmpegPCMAudio(
        'C:/Users/Vinícius/Desktop/Bot discord/audios/cavalo.mp3', executable=ffmpeg_path)

    # Inicie a reprodução do áudio
    voice_client.play(audio_source)

    # Aguarde até que a reprodução termine
    while voice_client.is_playing():
        await asyncio.sleep(1)

    # Espere mais 5 segundos e desconecte o bot do canal de voz
    await asyncio.sleep(5)
    await voice_client.disconnect()
    


# Iniciar o bot com o token
bot.run('MTE1Njk4MzE2MDUzMDI5Mjc4OQ.GKTEQU.4Qa_SGRMu8-I3scYpjTajjspQKxIStklIJmS8A')