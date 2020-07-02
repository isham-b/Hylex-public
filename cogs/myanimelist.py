import discord
from discord.ext import commands
from jikanpy import Jikan
from datetime import date

class MyAnimeList(commands.Cog):

    def __init__(self, client):
        self.client = client


    # Commands
    @commands.command()
    async def anime(self, ctx, *, title):
        """ Displays info about given anime. Use optional parameter <episode=> to search for an episode.

        Usage: -anime <anime name> (episode=#)
        """

        if 'season' in title:
            title = title.replace('season', '')

        if 'episode=' in title:
            return await self._animeEp(ctx, title)
        
        jikan = Jikan()
        result = jikan.search(search_type='anime', query=title)['results'][0]
        mal_id = result['mal_id']
        full_result = jikan.anime(mal_id)
        authour = ctx.message.author


        embed = discord.Embed(
            title = result['title'],
            url = result['url'],
            description = result['synopsis'],
            colour = discord.Colour.blurple(),
            type = 'rich'
        )

        embed.set_author(name='Anime Search', url="https://github.com/isham-b/Hylex", icon_url=authour.avatar_url)
        embed.set_thumbnail(url=result['image_url'])

        if full_result['type'] == 'Movie' or full_result['type'] == 'Special':
            embed.add_field(name='Duration', value=full_result['duration'])

        if full_result['type'] == 'TV':
            if result['episodes']:
                embed.add_field(name='Episodes', value=result['episodes'], inline=True)
            else:
                embed.add_field(name='Episodes', value=self._num_episodes(mal_id), inline=True)
            

        embed.add_field(name='Premiered', value=full_result['aired']['string'], inline=True)
        embed.add_field(name='Score', value=result['score'], inline=True)
        embed.add_field(name='Genres', value= ', '.join([genre['name'] for genre in full_result['genres']]), inline=False)
        
        await ctx.send(embed=embed)

    






    # Helper Functions
    def _num_episodes(self, mal_id):
        jikan = Jikan()
        last_page_num = jikan.anime(int(mal_id), extension='episodes')['episodes_last_page']
        last_page = jikan.anime(int(mal_id), extension='episodes', page=last_page_num)
        try:
            episodes = last_page['episodes'][-1]['episode_id']
        except (IndexError, KeyError):
            return "Unknown"
        return episodes



    async def _animeEp(self, ctx, title):
        jikan = Jikan()
        name, ep_num = title.split('episode=')
        result = jikan.search(search_type='anime', query=name)['results'][0]
        mal_id = result['mal_id']
        anime_title = result['title']
        authour = ctx.message.author
        

        if int(self._num_episodes(mal_id)) < int(ep_num):
            return await ctx.send(f'Error: \"{anime_title}\" has no episode {ep_num}!')

        page = int(ep_num) // 100
        if not (int(ep_num) % 100 == 0):
            page += 1
        print(page)
        episodes = jikan.anime(mal_id, extension='episodes', page=page)
        
        for dictionary in episodes['episodes']:
            if dictionary['episode_id'] == int(ep_num):
                embed = discord.Embed(
                    title = f'{anime_title} - Episode {ep_num}',
                    url = dictionary['video_url'],
                    description = dictionary['title'],
                    colour = discord.Colour.blue(),
                    type = 'rich'
                                    )
                
                premiere, filler = "Unknown", "Unknown"
                if dictionary['aired'] is not None:
                    d = date.fromisoformat(dictionary['aired'][:10])
                    premiere = d.strftime("%B %d, %Y")
                if dictionary['filler'] is not None:
                    filler = ['Yes' if dictionary['filler'] else 'No'][0]

                embed.set_author(name='Episode Search', url="https://github.com/isham-b/Hylex", icon_url=authour.avatar_url)
                embed.set_thumbnail(url=result['image_url'])
                embed.add_field(name='Premiered', value=premiere, inline=True)
                embed.add_field(name='Filler', value=filler)

                return await ctx.send(embed=embed)

        await ctx.send(f'Unable to find Episode {ep_num} for {anime_title}.')



    # Errors
    @anime.error
    async def animeEp_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Invalid syntax: Use `~animeEp <anime> episode=<#>`")



def setup(client):
    client.add_cog(MyAnimeList(client))        