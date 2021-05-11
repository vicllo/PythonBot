# coding: utf8

import discord
from discord.ext import commands
import constants
import sys
import os
from dotenv import load_dotenv
from keep_alive import keep_alive
from datetime import datetime

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
console = sys.stdout




#detecter l'allumage du bot
@bot.event
async def on_ready():
    print("Successfully connected !")
    servernb = str(len(bot.guilds))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("serving "+servernb+" servers"))



@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    serveur = member.guild.id
    print(channel,serveur)
    if serveur == 682539277330284585:
        if channel is not None:
            await channel.send('Bienvenue sur le serveur général {0.mention}, merci d\'écrire ici ton prénom, nom ainsi que ta classe afin que tu sois assigné(e) à ta classe.'.format(member))
    elif serveur == 707200285436805141:
        if channel is not None:
            await channel.send('Bienvenue sur le serveur des 2nde {0.mention}, merci d\'écrire ici ton prénom, nom ainsi que ta classe afin que tu sois assigné(e) à ta classe.'.format(member))
    else:
        if channel is not None:
            await channel.send('Welcome in the server {0.mention}.'.format(member))

#commande test
@bot.command()
async def ping(ctx):
    """
    A small command to see if the bot is alive
    """
    await ctx.send("pong")

@bot.command()
async def python(ctx):
    """
    A command to execute python scripts.
    First, call the command, and wait for a bot waiting message.
    Second, write your code. You can choose to write it with or without the python code markdown\n(\`\`\`python\n code \n \`\`\`)\n
    """
    sys.stdout = console
    channel = ctx.channel
    authorid = ctx.author.id
    def check(m):
        return m.channel == channel and m.author.id == authorid
    messagebot = await ctx.send(constants.send_wait_msg)
    prgm = await bot.wait_for('message', check=check)
    await messagebot.delete(delay=2)
    await ctx.message.delete(delay=2)
    if prgm.content.startswith("```"):
        prgm.content = prgm.content.replace("```python","")
        prgm.content = prgm.content.replace("```","")
    with open("input.py","w") as input_file:
        input_file.write(prgm.content)

    os.system("wandbox-python3 run input.py > retour.txt")

    with open("retour.txt", "r") as output_file:
        retour_txt = output_file.read()
    if not retour_txt.startswith("signal: Killed"):
        retour_txt = retour_txt[17:]
    else:
        retour_txt = "Your program is to slow"
    try:
        message = await ctx.send("```python\n"+retour_txt+"```")
    except discord.errors.HTTPException:
        with open("retour.txt", "r") as output_file:
            message = await ctx.send("```Your program output is more than 2000 caracters.Please consider shorting it.```", file=discord.File(output_file,filename=datetime.now().strftime("%d %b %Y. %H:%M:%S.txt")))
    await message.add_reaction(constants.emotrash)


@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    messageReaction = await channel.fetch_message(payload.message_id)
    if messageReaction.author.id == constants.botid and payload.user_id != constants.botid:
        if payload.emoji.name == constants.emotrash:
            await messageReaction.delete()


#LOGS 
@bot.event
async def on_message(ctx):

    servernb = str(len(bot.guilds))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("serving "+servernb+" servers"))

    
    serv = bot.get_guild(709826568016625745)
    canal = serv.get_channel(709826568016625748)
    if ctx.channel.id != 709826568016625748:
        await canal.send(str("**"+ctx.author.name)+"** ("+str(ctx.guild)+" - "+str(ctx.channel)+") : "+str(ctx.content)+"\n")

    await bot.process_commands(ctx)


print("Let's go")
load_dotenv()
token = os.getenv('TOKEN')

keep_alive()
bot.run(token)

