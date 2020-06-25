import discord
import random
import commands_help
from discord.ext import commands



class General(commands.Cog):
    
    def __init__(self, client):
        self.client = client





    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game('Bot Stuff | ~help'))
        print('We have logged in as {0.user}'.format(self.client))

    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member, ctx):
        print(f'{member} has joined the server!')
        await ctx.send(f'Welcome {member.mention} to the server!')

    
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member, ctx):
        print(f'{member} has left the server.')
        await ctx.send(f'{member} has left the server.')

    
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild, ctx):
        print(f'Hylex has joined {guild}!')
        await ctx.send('Hello! Hylex uses Tildes ```~``` as command prefixes, type ~help for command help and syntax.')







    # Commands
    @commands.command()
    async def send_bot_help(self, ctx, aliases=['help']):
        authour = ctx.message.author
        embed = discord.Embed(
            colour = discord.Colour.blue()
        )

        embed.set_author(name='Help')
        embed.add_field(name='General', value=commands_help.general_help, inline=False)
        embed.add_field(name='Moderation', value=commands_help.mod_help, inline=False)
        embed.set_footer(text='If this is not the correct anime, do ~anime')

        await authour.send(embed=embed)
        

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')


    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.","It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.",
                 "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.",
                 "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
        await ctx.send(random.choice(responses))
    
    





    # Errors
    







def setup(client):
    client.add_cog(General(client))