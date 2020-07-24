import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from cogconstants import LOLPARSER_SERVERS, LOLPARSER_RANKICONS

class LoL(commands.Cog):

    def __init__(self, client):
        self.client = client

    
    # Commands
    @commands.command()
    @commands.guild_only()
    async def lolrank(self, ctx, *, name):
        """
        Search for a summoner's ranked stats, including rank, W/L, and more.\nUsage: -lolrank <name> <region>
        """
        region = name.split()[-1].lower()
        username = ' '.join(name.split()[:-1])
        opggurl = "https://" + region + f".op.gg/summoner/userName={username.replace(' ', '+')}"

        if region not in LOLPARSER_SERVERS:
            return await ctx.send('**Error**: You must include a valid region name! (NA, EUW, EUNE...)')
        
        page = requests.get(opggurl)

        if page.status_code != 200:
            return await ctx.send('**Error**: Unable to connect to servers, please try again later.')

        soup = BeautifulSoup(page.content, 'html.parser')
        metas = soup.find_all('meta')
        temp = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
        splitted = temp[0].split(' / ')
        rank, lp = ' '.join(splitted[1].split()[:2]), ' '.join(splitted[1].split()[2:])
        # Summoner is Unranked/Provisional
        if len(rank) == 0:
            rank = 'Unranked'
            wins, losses = '-', '-'
            desc = None
        else:
            wins, losses = splitted[2].split()[0].replace('W', ''), splitted[2].split()[1].replace('L', '')
            desc = splitted[-1].replace(',', ',\n')
        authour = ctx.message.author

        # Summoner is in rank with no tiers
        if 'Challenger' in splitted[1] or 'Grandmaster' in splitted[1] or 'Master' in splitted[1]:
            rank, lp = ' '.join(splitted[1].split()[:1]), ' '.join(splitted[1].split()[1:])
            

        # Summoner not registered on OPGG
        if username.lower() != splitted[0].lower():
            return await ctx.send(f'**Error**: Could not find player "{username}" in region {region}.')


        embed = discord.Embed(
            title = f'{splitted[0]} - {rank} / ' + [lp if lp != '' else '0 LP'][0], 
            url = opggurl, 
            description = desc,
            colour = discord.Color.green(),
            type = 'rich'
        )

        embed.set_author(name='League Rank Search', url="https://github.com/isham-b/Hylex", icon_url=authour.avatar_url)
        embed.set_thumbnail(url=[LOLPARSER_RANKICONS[rank] if len(rank) > 0 else LOLPARSER_RANKICONS['Unranked']][0])
        embed.add_field(name='Wins', value=wins, inline=True)
        embed.add_field(name='Losses', value=losses, inline=True)
        if losses.isnumeric() and int(losses) != 0:
            embed.add_field(name='Win Ratio', value=round(int(wins) / (int(losses) + int(wins)), 2))
        elif losses.isnumeric() and int(losses) == 0:
            embed.add_field(name='Win Ratio', value='1.00')

        await ctx.send(embed=embed)


    # Errors
    @lolrank.error
    async def lolrank_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Invalid syntax: Use `-lolrank <name> <region>`.")




def setup(client):
    client.add_cog(LoL(client))    