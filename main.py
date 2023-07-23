import time, asyncio, random, string, json, os, discord, discord.ext, pyttsx3
#PyNaCl
from keep_alive import keep_alive
#from discord.utils import get
from discord.ext import commands, tasks
#from discord.ext.commands import has_permissions, CheckFailure, check
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord_slash.utils import manage_commands
from discord_slash.utils.manage_commands import create_option
from rcon.source import Client
from rcon.source import rcon

with open('config.json') as f:
    config = json.load(f)

#Define our bot
client = discord.Client()
client = commands.Bot(command_prefix="DED!")
slash = SlashCommand(client, sync_commands=True)
lang = config["messages"]
bot_in_vc = False
ruleta_activa = False


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name='Viendo DEDSAFIO ARK', status=discord.Status.do_not_disturb)
	)
    print("Bot online")


def has_permisions(sender_id):
    if str(sender_id) in config["allowed_ids"]:
        return True
    else:
        return False


@slash.slash(
    name="ruleta",
    description="Ruletas evento",
    options=[
        create_option(name="tipo_ruleta",
                      description="Que tipo de ruleta quieres ejecutar?",
                      option_type=3,
                      required=True,
                      choices=[
						  manage_commands.create_choice(
							  name="Mutacion de ADN",
                              value="ADN"
						  ),
        #                   manage_commands.create_choice(
							 #  name="Dino Indomables",
        #                       value="dinoespitosos"
						  # ),
						  manage_commands.create_choice(
							  name="Dinos Dormilones",
							  value="dinosdormidos"
						  ),
						  manage_commands.create_choice(
							  name="Afeccion por Polen",
							  value="florrara"
						  ),
						  manage_commands.create_choice(
							  name="Esporas Malignas provenientes de Setas",
							  value="setas"
						  ),
						  manage_commands.create_choice(
							  name="¡Joderrrrrr que me cago!",
							  value="diarrea"
						  ),
						  manage_commands.create_choice(
							  name="¡Alto peligro! - Ventosidades",
							  value="tufon"
						  ),
						  manage_commands.create_choice(
							  name="¡Dejen-me dormir es sabado!",
							  value="dormilon"
						  ),
						  manage_commands.create_choice(
							  name="¡Joder me pesa mucho el culo!",
							  value="playerspeed"
						  ),
						  manage_commands.create_choice(
							  name="Como el mundo me trajo",
							  value="desnudo"
						  ),
						  manage_commands.create_choice(
							  name="Feromonas Sexuales Alteradas!",
							  value="orgasmo"
						  )
                      ]),
        create_option(name="duracion_ruleta",
                      description="Por favor seleciona una opcion de tiempo!",
                      option_type=3,
                      required=True,
                      choices=[
                          manage_commands.create_choice(name="30 min",
                                                        value="1800"),
                          manage_commands.create_choice(name="25 min",
                                                        value="1500"),
                          manage_commands.create_choice(name="20 min",
                                                        value="1200"),
                          manage_commands.create_choice(name="15 min",
                                                        value="900"),
                          manage_commands.create_choice(name="10 min",
                                                        value="600"),
                          manage_commands.create_choice(name="5 min",
                                                        value="300"),
                          manage_commands.create_choice(name="4 min",
                                                        value="240"),
                          manage_commands.create_choice(name="3 min",
                                                        value="180"),
                          manage_commands.create_choice(name="2 min",
                                                        value="120"),
                          manage_commands.create_choice(name="1 min",
                                                        value="60"),
                          manage_commands.create_choice(name="30 seg",
                                                        value="30"),
                          manage_commands.create_choice(name="Sin Duración",
                                                        value="1")
                      ]),
        create_option(
            name="tempo_repeticion",
            description=
            "Por favor seleciona una de las siguientes opciones de repeticion",
            option_type=3,
            required=True,
            choices=[
                manage_commands.create_choice(name="30 min", value="1800"),
                manage_commands.create_choice(name="25 min", value="1500"),
                manage_commands.create_choice(name="20 min", value="1200"),
                manage_commands.create_choice(name="15 min", value="900"),
                manage_commands.create_choice(name="10 min", value="600"),
                manage_commands.create_choice(name="5 min", value="300"),
                manage_commands.create_choice(name="4 min", value="240"),
                manage_commands.create_choice(name="3 min", value="180"),
                manage_commands.create_choice(name="2 min", value="120"),
                manage_commands.create_choice(name="1 min", value="60"),
                manage_commands.create_choice(name="30 seg", value="30"),
                manage_commands.create_choice(name="Sin repeticion", value="0")
            ])
    ])
async def _help(ctx: SlashContext, tipo: str, duracion: str, repeticion: str):
    global ruleta_activa
    if str(ctx.author.id) in config["allowed_ids"]:
        if ruleta_activa == False:
            if str(ctx.author.id) in config["eventos_config"].get(tipo.lower())["has_permission"] or config["eventos_config"].get(tipo.lower())["has_permission"] == "allowed":
                try:
                    duracion = int(duracion)
                    if duracion < 30: 
                        minutos = duracion 
                    else:
                        minutos = int(duracion / 60)
                    repeticion = int(repeticion)
                    type = tipo.lower()
                    typeClass = config["eventos_config"].get(type)
                    if repeticion > 1 and typeClass["dontrepeat"] == "False":
                        repeticion = int(repeticion)
                    else:
                        repeticion = duracion

                    if duracion > 1800:
                        await ctx.send(lang.get("dura_maxima"))
                    else:
                        await ctx.send(f"Se mandaran {tipo} durante {minutos} minutos")

                        if typeClass["Concat"] == "True":
                            response = await rcon(typeClass["ruletaComando"] + str(minutos) + lang.get("minuts") + "] " + str(typeClass["colorRuleta"]), host=config["rcon"]["host"], port=config["rcon"]["port"], passwd=os.getenv("rconpassword_dedsafio"))
                            print(response)
                        else:
                            response = await rcon(typeClass["ruletaComando"], host=config["rcon"]["host"], port=config["rcon"]["port"], passwd=os.getenv("rconpassword_dedsafio"))
                            print(response)

                        await ctx.send(f"La peticion se ha completado con exito, se ha lanzado una ruleta del tipo: {tipo}")
					
                        if typeClass["delay"]:
                            await asyncio.sleep(typeClass["delay"])

                        ruleta_activa = True
                        while duracion > 0 and ruleta_activa:
                            for message in typeClass["comandos"]:
                                #await ctx.send(message)
                                await ctx.send(f"¡Se ha ejecutado el comando pertinente a la ruleta lanzada! {tipo}")
                                response = await rcon(
                                    message,
                                    host=config["rcon"]["host"],
                                    port=config["rcon"]["port"],
                                    passwd=os.getenv("rconpassword_dedsafio"))
                                print(response)

                            # Reduce la duración restante por la cantidad de tiempo de repetición
                            duracion -= repeticion
                            if duracion <= 0:
                                ruleta_activa = False
                                await ctx.send(f"La ultima ruleta ejecutada de tipo: {tipo} ha finalizado con exito")

                            # Espera el tiempo de repetición entre cada repetición
                            await asyncio.sleep(repeticion)
                except Exception as e:
                    print(f"Error en la conexión RCON: {e}")
            else:
                await ctx.send(lang.get("donthavepermissions_roulette_type"))
        else:
            await ctx.send(lang.get("ruleta_activa"))
    else:
        await ctx.send(lang.get("donthavepermisions"))


@slash.slash(
    name="clear",
    description="Limpia el discord de los deschos humanos llamados mensajes",
    options=[
        create_option(
            name="cantidad",
            description=
            "Introduce una cantidad de recogedores que quieres comprar!",
            option_type=3,
            required=True),
    ])
async def clear(ctx, amount: str):
    if str(ctx.author.id) in config["allowed_ids"]:
        await ctx.send(
            "Se eliminaran todos los desechos! Gracias por usar basurerias Paco"
        )
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=int(amount))
    else:
        await ctx.send(lang.get("donthavepermisions"))


@slash.slash(
    name="serverchat",
    description=
    "Pues hace lo que su nombre indica mandar un mensaje por el chat del servidor",
    options=[
        create_option(
            name="texto",
            description=
            "Repuesta que esto le afecta el limite de caracteres de discord y los permitidos por el propio juego!",
            option_type=3,
            required=True),
    ])
async def serverchat(ctx: SlashContext, text: str):
    if str(ctx.author.id) in config["allowed_ids"]:
        try:
            with Client(config["rcon"]["host"],
                        config["rcon"]["port"],
                        passwd=os.getenv("rconpassword_dedsafio")) as RClient:
                response = RClient.run(f'serverchat {text}')

                await ctx.send(response)
                await ctx.send(
                    f"La peticion se ha completado con exito, el mensaje ha sido {text}"
                )

        except Exception as e:
            print(f"Error en la conexión RCON: {e}")
    else:
        await ctx.send(lang.get("donthavepermisions"))


@slash.slash(
    name="broadcast",
    description=
    "Pues hace lo que su nombre indica mandar un broadcast en el server",
    options=[
        create_option(
            name="texto",
            description=
            "Repuesta que esto le afecta el limite de caracteres de discord y los permitidos por el propio juego!",
            option_type=3,
            required=True)
    ])
async def broadcast(ctx, text: str):
    if str(ctx.author.id) in config["allowed_ids"]:
        await ctx.send(text)


# send broadcast!
    else:
        await ctx.send(lang.get("donthavepermisions"))


@slash.slash(name="joinvoice",
             description="this is a test for voice channel join",
             options=[
                 create_option(name="channel",
                               description="please sleect channel",
                               option_type=7,
                               required=True)
             ])
async def joinvoice(ctx, channel):
    if str(ctx.author.id) in config["allowed_ids"]:
        await channel.connect()
    else:
        await ctx.send(lang.get("donthavepermisions"))


@slash.slash(
    name="deteneruleta",
    description="Detener la ultima ruleta ejecutada!"
)
async def deteneruleta(ctx: SlashContext):
    global ruleta_activa
    ruleta_activa = False
    await ctx.send("La ultima ruleta se ha detenido con exito!")


def text_to_speech(message):
    engine = pyttsx3.init()
    engine.save_to_file(message, 'tts.mp3')
    engine.runAndWait()


@slash.slash(name="tts",
             description="Reproduce un mensaje en un canal de voz.",
             options=[{
                 "name": "canal_de_voz",
                 "description":
                 "Canal de voz en el que se reproducirá el mensaje.",
                 "type": 7,
                 "required": True
             }, {
                 "name": "mensaje",
                 "description": "Mensaje a reproducir por voz.",
                 "type": 3,
                 "required": True
             }])
async def tts(ctx, canal_de_voz: discord.VoiceChannel, mensaje: str):
    global bot_in_vc
    #if ctx.author.voice and ctx.author.voice.channel:
    #voice_channel = ctx.author.voice.channel
    if not bot_in_vc:
        try:
            vc = await canal_de_voz.connect()
            bot_in_vc = True
            await ctx.send(f"Me he unido al canal de voz {canal_de_voz.name}.")
        except discord.ClientException:
            await ctx.send(
                "Ya estoy en un canal de voz. Utiliza el comando 'leave' para salir antes de unirme a otro."
            )
    else:
        await ctx.send(
            "Ya estoy en un canal de voz. Utiliza el comando 'leave' para salir antes de unirme a otro."
        )
    #else:
    #await ctx.send(
    #"¡Debes estar en un canal de voz para usar este comando!")


@slash.slash(name="leave", description="El bot sale del canal de voz actual.")
async def leave(ctx):
    global bot_in_vc
    if bot_in_vc:
        voice_client = ctx.guild.voice_client
        await voice_client.disconnect()
        bot_in_vc = False
        await ctx.send("Me he desconectado del canal de voz.")
    else:
        await ctx.send("No estoy en un canal de voz.")


# LAS TABULACION PETAN EL CODIGO SOLO SE PUEDE USAR ESPACIOS COMO ESTO "    " 4 ESPACIOS SIMULAN UNA TABULACION



keep_alive()
#Run our bot
client.run(os.getenv("TOKEN"))
