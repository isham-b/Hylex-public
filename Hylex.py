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




@client.command()
@commands.is_owner()
async def servers(ctx):
    server_list = list(client.guilds)
    await ctx.send(f'Connected to {str(len(server_list))} servers:')
    finalstr = ''
    for server in server_list:
        total_members = str(len(server.members))
        server_name = server.name
        finalstr += f'{server_name} ({total_members})\n'
    await ctx.send(finalstr)

    


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')



client.run('PLACE BOT TOKEN HERE')
