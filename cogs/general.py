import discord
import random
from discord.ext import commands
from discord.utils import find


class General(commands.Cog):

    def __init__(self, client):
        self.client = client





    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game('Bot Stuff | -help'))
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
    async def on_guild_join(self, guild: discord.Guild):
        print(f'Hylex has joined {guild}!')
        general = find(lambda x: x.name == 'general',  guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            await general.send('Hello! Hylex uses Dashes "`-`" as command prefixes, type -help for command help and syntax.')




    # Commands

        

    @commands.command()
    async def ping(self, ctx):
        '''
        Gets the latency of bot.
        Usage: `-ping`
        '''
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')


    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        '''
        Asks the mysterious 8ball for advice.
        Usage: `-8ball <question>`
        '''
        responses = ["It is certain.","It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.",
                 "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.",
                 "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
        await ctx.send(random.choice(responses))
    
    
    @commands.command(pass_context=True)
    @commands.has_permissions(add_reactions=True, embed_links=True)
    async def help(self,ctx,*cog):
        """Gets all cogs and commands of mine."""
        try:
            
            if not cog:
                """Cog listing"""
                halp=discord.Embed(title='Command Help',
                                description='Use `-help <category>` (Case Sensitive) to find out more about them!\nMessage **LlamaLegacy#2576** for additional help!')
                cogs_desc = ''
                for x in self.client.cogs:
                    if x != 'CommandErrorHandler':
                        cogs_desc += ('{}\n'.format(x))
                halp.add_field(name='Categories',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
                await ctx.message.add_reaction(emoji='✉')
                await ctx.message.author.send('',embed=halp)
            else:
                """Helps me remind you if you pass too many args."""
                if len(cog) > 1:
                    halp = discord.Embed(title='Error!',description='Too many categories given!',color=discord.Color.red())
                    await ctx.message.author.send('',embed=halp)
                else:
                    """Command listing within a cog."""
                    found = False
                    for x in self.client.cogs:
                        for y in cog:
                            if x.lower() == y.lower():
                                halp=discord.Embed(title=x+' Command Listing',description=self.client.cogs[x].__doc__)
                                for c in self.client.get_cog(y).get_commands():
                                    if not c.hidden:
                                        tempname = [c.aliases[0] if c.aliases else c.name][0]
                                        halp.add_field(name=tempname,value=c.help,inline=False)
                                found = True
                    if not found:
                        """Reminds you if that cog doesn't exist."""
                        halp = discord.Embed(title='Error!',description='No category "'+cog[0]+'" found. Make sure you spelled it right (including captials)!',color=discord.Color.red())
                    else:
                        await ctx.message.add_reaction(emoji='✉')
                    await ctx.message.author.send('',embed=halp)
        except:
            await ctx.send("Unable to send embeds.")
        



    # Errors
    






def setup(client):
    client.remove_command('help')
    client.add_cog(General(client))
    
