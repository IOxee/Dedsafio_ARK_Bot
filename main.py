import time, asyncio, random, string, json, os, discord, discord.ext
from keep_alive import keep_alive
from discord.ext import commands
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
intents = discord.Intents.default()
intents.guilds = True
discord.Intents.members = True
intents.bans = True
intents.emojis = True
intents.integrations = True
intents.webhooks = True
intents.invites = True
intents.voice_states = True
intents.presences = True
intents.messages = True
intents.reactions = True
intents.typing = True
lang = config["messages"]
bot_in_vc = False
ruleta_activa = False
listado_de_nombres = []
members_who_cant_send = []


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(
            name=config["bot"]["status"],
            status=discord.Status.do_not_disturb
        )
    )
    print("Bot online")

@slash.slash(
    name="ruleta",
    description="Ruletas evento",
    options=[
        create_option(
            name="tipo_ruleta",
            description="Que tipo de ruleta quieres ejecutar?",
            option_type=3,
            required=True,
            choices=[
                manage_commands.create_choice(name="Mutacion de ADN",
                                              value="ADN"),
                #                   manage_commands.create_choice(
                #  name="Dino Indomables",
                #                       value="dinoespitosos"
                # ),
                manage_commands.create_choice(name="Dinos Dormilones",
                                              value="dinosdormidos"),
                manage_commands.create_choice(
                    name="Afeccion por Polen (Flor Rara)", value="florrara"),
                manage_commands.create_choice(
                    name="Esporas Malignas provenientes de Setas",
                    value="setas"),
                manage_commands.create_choice(
                    name="¡Joderrrrrr que me cago! (Diarrea)",
                    value="diarrea"),
                manage_commands.create_choice(
                    name="¡Alto peligro! - Ventosidades (Tufon)",
                    value="tufon"),
                manage_commands.create_choice(
                    name="¡Dejen-me dormir es sabado! (Dormilon)",
                    value="dormilon"),
                manage_commands.create_choice(
                    name="¡Joder me pesa mucho el culo! (Pies de plomo)",
                    value="playerspeed"),
                manage_commands.create_choice(
                    name="Como el mundo me trajo (Desnudez)", value="desnudo"),
                manage_commands.create_choice(
                    name="Feromonas Sexuales Alteradas! (Orgasmo)",
                    value="orgasmo"),
                manage_commands.create_choice(name="REGRESION INFATIL (Bebe)",
                                              value="bebe"),
                manage_commands.create_choice(
                    name="MIERDA DE MOSQUITOS (Mosquitos)", value="mosquito"),
                manage_commands.create_choice(name="Congalacion",
                                              value="congelacion"),
				manage_commands.create_choice(name="Chupar energina vital (Casi Muertos)", value="casimuerto"),
				manage_commands.create_choice(name="Gases Peligrosos", value="gagases"),
				manage_commands.create_choice(name="Altos niveles de radiacion!", value="radio")
				
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
            if str(ctx.author.id) in config["eventos_config"].get(tipo.lower(
            ))["has_permission"] or config["eventos_config"].get(
                    tipo.lower())["has_permission"] == "allowed":
                try:
                    duracion = int(duracion)
                    if duracion < 30:
                        minutos = duracion
                    else:
                        minutos = int(duracion / 60)
                    repeticion = int(repeticion)
                    type = tipo.lower()
                    typeClass = config["eventos_config"].get(type)
                    serverchatdosentWork = config["serverchat"]
                    if repeticion > 1 and typeClass["dontrepeat"] == "False":
                        repeticion = int(repeticion)
                    else:
                        repeticion = duracion

                    if duracion > 1800:
                        await ctx.send(lang.get("dura_maxima"))
                    else:
                        await ctx.send(
                            f"Se mandaran {tipo} durante {minutos} minutos")

                        if typeClass["Concat"] == "True":
                            variableMensaje = typeClass["mensaje"] + str(
                                minutos) + " " + lang.get("minuts")

                            response = await rcon(
                                typeClass["ruletaComando"] + variableMensaje +
                                "] " + str(typeClass["colorRuleta"]),
                                host=config["rcon"]["host"],
                                port=config["rcon"]["port"],
                                passwd=os.getenv("rconpassword"))
                            print(response)

                            if serverchatdosentWork == "True":
                                response = await rcon(
                                    "serverchat " + variableMensaje,
                                    host=config["rcon"]["host"],
                                    port=config["rcon"]["port"],
                                    passwd=os.getenv("rconpassword"))
                        else:
                            response = await rcon(
                                typeClass["ruletaComando"] +
                                typeClass["mensaje"] + "]",
                                host=config["rcon"]["host"],
                                port=config["rcon"]["port"],
                                passwd=os.getenv("rconpassword"))
                            print(response)
                            if serverchatdosentWork == "True":
                                response = await rcon(
                                    "serverchat " + typeClass["mensaje"],
                                    host=config["rcon"]["host"],
                                    port=config["rcon"]["port"],
                                    passwd=os.getenv("rconpassword"))

                        await ctx.send(
                            f"La peticion se ha completado con exito, se ha lanzado una ruleta del tipo: {tipo}"
                        )

                        if typeClass["delay"]:
                            await asyncio.sleep(typeClass["delay"])

                        ruleta_activa = True
                        while duracion > 0 and ruleta_activa:
                            for message in typeClass["comandos"]:
                                #await ctx.send(message)
                                await ctx.send(
                                    f"¡Se ha ejecutado el comando pertinente a la ruleta lanzada! {tipo}"
                                )
                                response = await rcon(
                                    message,
                                    host=config["rcon"]["host"],
                                    port=config["rcon"]["port"],
                                    passwd=os.getenv("rconpassword"))
                                print(response)

                            # Reduce la duración restante por la cantidad de tiempo de repetición
                            duracion -= repeticion
                            if duracion <= 0:
                                ruleta_activa = False
                                await ctx.send(
                                    f"La ultima ruleta ejecutada de tipo: {tipo} ha finalizado con exito"
                                )

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
                        passwd=os.getenv("rconpassword")) as RClient:
                response = RClient.run(f'serverchat {text}')

                await ctx.send(response)
                await ctx.send(
                    f"La peticion se ha completado con exito, el mensaje ha sido {text}"
                )

        except Exception as e:
            print(f"Error en la conexión RCON: {e}")
    else:
        await ctx.send(lang.get("donthavepermisions"))

@slash.slash(name="deteneruleta",
             description="Detener la ultima ruleta ejecutada!")
async def deteneruleta(ctx: SlashContext):
    global ruleta_activa
    ruleta_activa = False
    await ctx.send("La ultima ruleta se ha detenido con exito!")

keep_alive()
client.run(os.getenv("TOKEN"))
