import os
from unicodedata import name

import wikiModule
import help
import discord

from discord.ext import commands

if not os.environ.get("PRODUCTION"):
    from dotenv import load_dotenv

    load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='0!',intents=intents)

helpstring='Type 0!tips and then one of the following to generate advice. Note: This command is targeted at beginners.'
for x,y in help.suggestions.items():
    helpstring+=f'\n{x}: {y["name"]}'

@bot.event
async def on_ready():
    
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='wiki', help='Type 0!wiki and the name of a character(e.g 0!wiki Roy) to generate a link to their Serenes Forest Page.\nFor entries with spaces(such as Robin (Male), place a \'_\' character where the space should be.')
async def wiki(ctx,char):
    print("Wiki Command called: "+char.replace(char[0,1],(char[0,1].capitalize())))
    if (char+' (Cipher)') in wikiModule.characters:
        await ctx.send(f'https://wiki.serenesforest.net/index.php/{char}_(Cipher)')
    else:
       await ctx.send('That character page doesn\'t exist. Did you misspell something?')

@bot.command(name='tips', help=helpstring)
async def tips(ctx,card):
    print("Tips Command Called")
    if(card in help.suggestions):
        entry=help.suggestions[card]
        output=f'```Name: {entry["name"]}\nHere are some tips:'
        for x in entry["tips"]:
            output+=f'\n\n{x}'
        if("cards" in entry):
            output+='\n\nSee also:'
            for x in entry['cards']:
                output+=f"\n{x}"
            output+="```"
        else:
            output+='\n This card can fit its way into a vast amount of decks.```'
        await ctx.send(output)
    else:
        await ctx.send('This card hasn\'t been listed in this bot yet, but a member of Ciphercord will likely be able to help you')



@bot.event
async def on_member_join(member):
    print("Member joined")
    ch=bot.get_channel(107543785776373760)
    await ch.send(
        f'''Hi {member.mention}. Welcome to Ciphercord! 
For some help with playing cipher or deck building advice you can ask in:
general/ #cipher-discussion/#cipher-questions 
or direct attention to people with the @ I\'m being helpful role
We mainly use LackeyCCG on this server and all resources can be found in #cipher-resources '''
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    #if message.content == '@poor dreidel,,,':
       # await message.channel.send(message.content)
    await bot.process_commands(message)
bot.run(TOKEN)

