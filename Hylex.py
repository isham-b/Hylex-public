import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix='-')




@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')  


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')



client.run('NzE5NzE3MjQ3NzQ4MTQ1MTYz.XxkkuQ.PmY6c3tFaJl6FTPgui-v0DZXi6Y')
