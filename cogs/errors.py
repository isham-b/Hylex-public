import traceback
import sys
import discord
from discord.ext import commands
#from general import General

class CommandErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

'''
    @General._8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'question':
                await ctx.send("You didn't give me a question to answer!")
                
'''
def setup(client):
    client.add_cog(CommandErrorHandler(client))