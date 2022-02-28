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

helpstring='Type 0!tips and then one of the following to generate advice for splash cards. Note: This command is targeted at beginners.'
helpstring2='Type 0!mc and then one of the following to generate advice for MCs. All of these entries have been submitted by members of the community.'
for x,y in help.suggestions.items():
    helpstring+=f'\n{x}: {y["name"]}'
for x,y in help.MCs.items():
    helpstring2+=f'\n{x}: {y["deck"]}'


@bot.event
async def on_ready():
    
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='wiki', help='Type 0!wiki and the name of a character(e.g 0!wiki Roy) to generate a link to their Serenes Forest Page.\nFor entries with spaces(such as Robin (Male), place a \'_\' character where the space should be.')
async def wiki(ctx,char):
    print("Wiki Command called: "+char)
    name_arr = char.split("_")
    search_term = "" 

    for word in name_arr:
        if(word[0]=='('):
            word=word.replace(word[1:2],word[1:2].capitalize())
        else:
            word = word.capitalize()
        search_term += word
        search_term += "_" 
    print(search_term)
    if (search_term[0:len(search_term)-1]+' (Cipher)') in wikiModule.characters:
        await ctx.send(f'https://wiki.serenesforest.net/index.php/{search_term}(Cipher)')
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

@bot.command(name='mc', help=helpstring2)
async def tips(ctx,card):
    print("MC Command Called")
    if(card in help.MCs):
        entry=help.MCs[card]
        output=f'```Deck: {entry["deck"]}\n'
        output+=f'Intended Final Promo: {entry["promo"]}\n'
        output+=f'Author: {entry["author"]}\n\n'
        output+=f'{entry["explanation"]}```'
        await ctx.send(output)
        await ctx.send(f'```Staples:\n{entry["staples"]}```')
    else:
        await ctx.send('This deck hasn\'t been listed in this bot yet, but a member of Ciphercord will likely be able to help you.')



@bot.event
async def on_member_join(member):
    print("Member joined")
    ch=bot.get_channel(107543785776373760)
    await ch.send(
        f'''Hi {member.mention}. Welcome to Ciphercord! 
For some help with playing cipher or deck building advice you can ask in:
general/ <#194169331091767296>/<#454116320380715019> 
or direct attention to people with the @ I\'m being helpful role.
We mainly use LackeyCCG on this server and all resources can be found in <#333965218482880513>.
If you're here to collect, you can find help in <#343299107554590722>.
Come say hello in <#946426335809646622>. We'd love to hear from you!
日本語で話せる <#945742334153326692> もあります '''
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    #if message.content == '@poor dreidel,,,':
       # await message.channel.send(message.content)
    await bot.process_commands(message)
bot.run(TOKEN)

