import discord
from discord.ext import commands,tasks
from discord.components import *
from discord import *
from datetime import datetime, timedelta
#import docx
#from docx import Document
import requests
import key

# Replace with the URL of the raw GitHub file
url = "https://raw.githubusercontent.com/spikestone/botyopen/main/adsm.txt"

# Send a GET request
response = requests.get(url)
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='>', intents=intents)





#hier ticket code





class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('>'), intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')



class Ticket(discord.ui.View):
    def __init__(self, allowed_roles):
        super().__init__()
        self.value = None
        self.allowed_roles = allowed_roles 

    async def create_ticket_channel(self, user):
        overwrites = {
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            user.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        }
        for role in self.allowed_roles:
            overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        channel = await user.guild.create_text_channel(name=f'ticket-{user.name}', overwrites=overwrites)
        
        return channel
    
    
    


    @discord.ui.button(label='Ticket', style=discord.ButtonStyle.green)
    async def Ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        ticket_channel = await self.create_ticket_channel(user)
        await interaction.response.send_message(f'Ticketing im Kanal {ticket_channel.mention}', ephemeral=True)
        self.value = True
        await delet(channel_name= ticket_channel)
        
    
async def delet(channel_name):
        view = Delet(channel_name)
        await channel_name.send('Willst du dein Ticket Schließen?', view=view)
        await view.wait()
        print(channel_name)

class Delet(discord.ui.View):
    def __init__(self, channel_name):
        super().__init__()
        

    
    async def close_ticket_channel(self, channel_name):
        await channel_name.delete()

    @discord.ui.button(label='Close Ticket', style=discord.ButtonStyle.red)
    async def CloseTicket(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        await self.close_ticket_channel(interaction.channel)
        await interaction.response.send_message(f'Ticket-Kanal geschlossen.', ephemeral=True)

       


   

#nicht anfassen es ist wichtig
bot = Bot()

#hier command code

@tasks.loop(hours=24)
async def dailysend():
    # Replace with your channel ID
    YOUR_CHANNEL_ID = 1216672524201361468

    # Replace with the path to your Word document
    #document_path = "adsm.docx"
    try:
        #document = Document(document_path)
        #content = "\n".join(paragraph.text for paragraph in document.paragraphs)
        channel = bot.get_channel(YOUR_CHANNEL_ID)
        print(channel)
        if channel:
            await channel.send(response.text)
        else:
            print(f"Channel with ID {YOUR_CHANNEL_ID} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

@bot.command()
async def ticket(ctx: commands.Context):
    allowed_roles = [role for role in ctx.author.roles if role.permissions.manage_channels]
    
    view = Ticket(allowed_roles)
    
    await ctx.send('Willst du ein Ticket Öffnen?', view=view)
    await view.wait()
    if view.value is None:
        print('Timed out...')
    elif view.value:
        print('Ticketed...')
    else:
        print('Cancelled...')

@bot.command()
async def website(ctx):
    website = ["https://jan-sternberg.web.app/","https://ventus-gaming.web.app/"]
    anzahl = len(website)
    websitenzahlloop = 0
    for x in range(anzahl):
        await ctx.send(website[websitenzahlloop])
        websitenzahlloop += 1


@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {0}ms'.format(round(bot.latency,1)))


@bot.command()
async def hello(ctx):
    await ctx.send("hello")


# hier Auto rollenverteilung
@bot.event
async def on_member_join(member):
    print(f"{member} has joined the server")
    #rollen id hier hinzufuegen
    Neue_Rolle= 1213603953116188722
    await member.add_roles(discord.utils.get(member.guild.roles, id=Neue_Rolle))

@bot.event
async def on_ready():
    print(f'Eingeloggt als {bot.user.name}')
    dailysend.start()


bot.run(key.bottoken)
