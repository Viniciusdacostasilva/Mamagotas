import discord
from discord.ext import commands
import voices  # Importe o módulo voices.py se você o tiver

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Lista de palavras-alvo que o bot irá contar
palavras_alvo = ["mamada", "mamar", "mamou", "mamei", "mamo", "mamadeira", "mamalias", "mama"]

# Dicionário para armazenar contagens por palavra para cada usuário
contagens_por_usuario = {}
ranks_por_usuario = {}
# Dicionário para armazenar contagens globais de mamadas
contagem_global = {palavra: 0 for palavra in palavras_alvo}

# Lista para armazenar IDs de mensagens já respondidas
mensagens_respondidas = []

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    # Canal onde você deseja enviar a mensagem de boas-vindas
    channel_id = 1026944137129369603 # Substitua pelo ID do canal desejado
    
    # Mensagem de boas-vindas ao ser iniciado
    welcome_message = "Como posso te ajudar a mamar hoje?"
    
    # Envia a mensagem de boas-vindas para o canal
    channel = bot.get_channel(channel_id)
    await channel.send(welcome_message)

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
        
        # Adiciona o ID da mensagem às mensagens já respondidas
        mensagens_respondidas.append(message.id)

    await bot.process_commands(message)

# Comando !ajuda
@bot.command()
async def ajuda(ctx):
    # Cria uma mensagem de ajuda
    help_message = """
    **Comandos disponíveis:**
    `!mamadas` - Conta o número de mamadas efetuadas por você.
    `!mamadaglobal` - Conta o número de mamadas efetuadas por todos usúarios.
    `!ajuda` - Exibe a lista de comandos disponíveis.
    `macaco` - Exibe o local com a maior quantidade de macacos do mundo.
    `!elo` - Exibe seu elo nas mamadas.
    """

    # Envia a mensagem de ajuda para o canal
    await ctx.send(help_message)

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

# Comando !mamada global para verificar a quantidade global de mamadas
@bot.command()
async def mamadaglobal(ctx):
    mensagem_contagem_global = "Contagem global de mamadas:\n"
    for palavra, contagem in contagem_global.items():
        mensagem_contagem_global += f"🍼 {palavra}: {contagem} vezes\n"
    await ctx.send(mensagem_contagem_global)

# Dicionário para armazenar os ranks dos usuários
ranks_por_usuario = {}

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
    
#Comando para !elo   
@bot.command()
async def elo(ctx):
    if ctx.author.id in ranks_por_usuario:
        elo = ranks_por_usuario[ctx.author.id]
        await ctx.send(f"{ctx.author.mention}, seu elo atual é: **{elo}**")
        
    else:
        await ctx.send(f"{ctx.author.mention}, você não efetuou nenhuma mamada ainda e é uma Boquinha cansada.")


# Iniciar o bot com o token
bot.run('MTE1Njk4MzE2MDUzMDI5Mjc4OQ.GnnHWV.DpbDeJim2K8KGyG-ZpD1QQURDe0vQB6-p9GBh4')