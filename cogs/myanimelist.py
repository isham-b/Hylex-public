import discord
import requests
from asyncio import TimeoutError
from bs4 import BeautifulSoup
from discord.ext import commands
from jikanpy import Jikan
from datetime import date
from cogconstants import query_id_anime, query_id_manga

class AnimeManga(commands.Cog):

    def __init__(self, client):
        self.client = client


    # Commands
    @commands.command()
    @commands.guild_only()
    async def anime(self, ctx,  *, title, anime_id=None):
        """ Displays info about given anime. Add 'episode=' to search for an episode.\nUsage: -anime <title> (episode=#)
        """
        url = 'https://graphql.anilist.co'
        searchforep = False
        if anime_id and not title:
            variables = {'id': int(anime_id)}
            query = query_id_anime

        else:
            splitted = title.split()

            # Check for season input
            for number in range(1, 10):
                if 's' + str(number) in splitted:
                    title = title.replace('s' + str(number), 'season ' + str(number))

            if 'episode=' in title:
                title, ep_num = title.split(' episode=')
                searchforep = True

            variables = {'search': title}
            query = '''
                query ($search: String) {
                Media(search: $search, type: ANIME) {
                    title {
                        english
                        romaji
                    }
                    siteUrl
                    idMal
                    status
                    episodes
                    coverImage {
                        large
                    }
                    description
                    startDate {
                        year
                        month
                        day
                    }
                    endDate {
                        year
                        month
                        day
                    }
                    averageScore
                    format
                    genres
                    externalLinks {
                        site
                        url
                    }
                    }
                }
                '''
        response = requests.post(url, json={'query': query, 'variables': variables})

        try:
            decoded = response.content.decode('utf-8')
            replaced = decoded.replace('null', 'None')
            full_dict = eval(replaced)
            media = full_dict['data']['Media']
        except:
            return await ctx.send(f'**Error**: No results found for "{title}", try using `-animesearch <title>` for a list of results.')

        if 'errors' in full_dict:
            return await ctx.send(f'**Error**: No results found for "{title}", try using `-animesearch <title>` for a list of results.')

        if searchforep:
            mal_id = media['idMal']
            return await self._animeEp(ctx, ep_num, mal_id)




        linkvalues, authour = '| ', ctx.message.author
        desc, tempep = 'No description available.', None
        if media['description']:
            tempdesc = BeautifulSoup(media['description'], features="html.parser")
            desc = tempdesc.get_text()[:200] + '...'
        platforms = ['Netflix', 'Hulu', 'AnimeLab', 'Crunchyroll', 'Funimation', 'Viz', 'VRV', 'Tubi TV']
        animeTitle = media['title']['english']
        if not animeTitle:
            animeTitle = media['title']['romaji']
        if media['format'] == 'TV':
            tempep = media['episodes']

        embed = discord.Embed(
            title = animeTitle,
            url = media['siteUrl'].replace('\\', ''),
            description = desc,
            colour = discord.Colour.blurple(),
            type = 'rich')
            
        for link in media['externalLinks']:
            if link == media['externalLinks'][0]:
                linkvalues = '|'
            if link['site'] in platforms:
                site = link['site']
                streamUrl = link['url'].replace('\\', '')
                linkvalues += f' [{site}]({streamUrl}) | '

        if None in media['startDate'].values():
            started, ended = '?', '?'
        elif None in media['endDate'].values():
            started = date(media['startDate']['year'], media['startDate']['month'], media['startDate']['day']).strftime("%B %d, %Y")
            ended ='?'
        else:
            started = date(media['startDate']['year'], media['startDate']['month'], media['startDate']['day']).strftime("%B %d, %Y")
            ended = date(media['endDate']['year'], media['endDate']['month'], media['endDate']['day']).strftime("%B %d, %Y")
        
        embed.set_author(name='Anime Lookup', url="https://github.com/isham-b/Hylex", icon_url=authour.avatar_url)
        embed.set_thumbnail(url=media['coverImage']['large'].replace('\\', ''))
        embed.add_field(name='Premiered', value=f'{started} to {ended}', inline=True)
        if media['averageScore']:
            embed.add_field(name='Score', value=media['averageScore'], inline=True)
        if tempep:
            embed.add_field(name='Episodes', value=tempep, inline=True)
        if media['genres']:
            embed.add_field(name='Genres', value=', '.join(media['genres']), inline=False)
        if not linkvalues == '|':
            embed.add_field(name='Watch', value=linkvalues)
        embed.set_footer(text='Not the right anime? Use -animesearch <anime> for a list of results.')

        await ctx.send(embed=embed)

    


    @commands.command()
    @commands.guild_only()
    async def manga(self, ctx, *, title, manga_id=None):
        """ Displays info about given manga.\nUsage: -manga <title>
        """

        url = 'https://graphql.anilist.co'
        if manga_id and not title:
            variables = {'id': int(manga_id)}
            query = query_id_manga
        else:
            variables = {'search': title}
            query = '''
                query ($search: String) {
                Media(search: $search, type: MANGA) {
                    title {
                        english
                        romaji
                    }
                    siteUrl
                    status
                    coverImage {
                        large
                    }
                    description
                    startDate {
                        year
                        month
                        day
                    }
                    endDate {
                        year
                        month
                        day
                    }
                    averageScore
                    genres
                    externalLinks {
                        site
                        url
                    }
                    }
                }
                '''
        response = requests.post(url, json={'query': query, 'variables': variables})
        
        try:
            decoded = response.content.decode('utf-8')
            replaced = decoded.replace('null', 'None')
            full_dict = eval(replaced)
        except:
            return await ctx.send(f'**Error**: No results found for "{title}."')

        if 'error' in full_dict:
            return await ctx.send(f'**Error**: No results found for "{title}."')

        linkvalues, authour = '| ', ctx.message.author
        media = full_dict['data']['Media']
        desc = 'No description available.'
        if media['description']:
            tempdesc = BeautifulSoup(media['description'], features="html.parser")
            desc = tempdesc.get_text()[:200] + '...'
        mangaTitle = media['title']['english']
        if not mangaTitle:
            mangaTitle = media['title']['romaji']
        

        embed = discord.Embed(
            title = mangaTitle,
            url = media['siteUrl'].replace('\\', ''),
            description = desc,
            colour = discord.Colour.purple(),
            type = 'rich')

        for link in media['externalLinks']:
            site = link['site']
            streamUrl = link['url'].replace('\\', '')
            linkvalues += f'[{site}]({streamUrl}) | '

        if None in media['startDate'].values():
            started, ended = '?', '?'
        elif None in media['endDate'].values():
            started = date(media['startDate']['year'], media['startDate']['month'], media['startDate']['day']).strftime("%B %d, %Y")
            ended ='?'
        else:
            started = date(media['startDate']['year'], media['startDate']['month'], media['startDate']['day']).strftime("%B %d, %Y")
            ended = date(media['endDate']['year'], media['endDate']['month'], media['endDate']['day']).strftime("%B %d, %Y")


        embed.set_author(name='Manga Search', url="https://github.com/isham-b/Hylex", icon_url=authour.avatar_url)
        embed.set_thumbnail(url=media['coverImage']['large'].replace('\\', ''))
        embed.add_field(name='Released', value=f'{started} to {ended}', inline=True)
        if media['averageScore']:
            embed.add_field(name='Score', value=media['averageScore'], inline=True)
        if media['genres']:
            embed.add_field(name='Genres', value=', '.join(media['genres']), inline=False)
        if linkvalues != '|':
            embed.add_field(name='Links', value=linkvalues)
        embed.set_footer(text='Not the right manga? Use -mangasearch <manga> for a list of results.')

        await ctx.send(embed=embed)
        

    @commands.command()
    @commands.guild_only()
    async def animesearch(self, ctx, *, title):
        '''
        Searches for an anime title.\n Usage: -animesearch <title>
        '''
        url = 'https://graphql.anilist.co'
        variables = {'search': title}
        query = '''
        query ($search: String) {
            Page(perPage: 10) {
                media(search: $search, type: ANIME) {
                    id
                    title {
                        english
                        romaji
                    }
                    format
                    startDate {
                        year
                        month
                        day
                    }
                }
            }
            }
        '''
        response = requests.post(url, json={'query': query, 'variables': variables})
        authour = ctx.message.author
        finalstr = ''

        try:
            decoded = response.content.decode('utf-8')
            replaced = decoded.replace('null', 'None')
            full_dict = eval(replaced)
        except:
            return await ctx.send(f'**Error**: No results found for "{title}". Make sure to spell everything correctly (Ex: use "season 2" instead of "s2").')

        page = full_dict['data']['Page']['media']
        if len(page) == 0:
            return await ctx.send(f'**Error**: No results found for "{title}". Make sure to spell everything correctly (Ex: use "season 2" instead of "s2").')

        i = 1
        for entry in page:
            # We have logged 5 entries
            if i == 6:
                break
            yr = str(entry['startDate']['year'])
            mediatype = entry['format']
            temptitle = entry['title']['english']
            if not temptitle:
                temptitle = entry['title']['romaji']
            if yr and mediatype and temptitle:
                finalstr += f'{i}. ' + temptitle + f' ({yr} {mediatype})\n'
                i += 1
            
        await ctx.send("**Please select an anime by typing a number from 1-5, or type 'cancel' to stop the search:**\n" + finalstr)

        try:
            msg = await self.client.wait_for('message', timeout=45.0, check=lambda message: (message.content.split()[0].isnumeric() or message.content.lower() == 'cancel') and message.author == authour)
            if msg.content.lower == 'cancel':
                return
            number = int(msg.content.split()[0]) - 1
            try:
                name = page[number]['title']['english']
                tempid = page[number]['id']
            except KeyError:
                return await ctx.send('**Error**: Cannot find anime with that number.')
            if not name:
                name = page[number]['title']['romaji']
            if name:
                print('f')
                return await self.anime(ctx, title=None, anime_id=tempid)
        except TimeoutError:
            print(f'Animesearch timed out for {authour}')




    @commands.command()
    @commands.guild_only()
    async def mangasearch(self, ctx, *, title):
        '''
        Searches for a manga title.\n Usage: -mangasearch <title>
        '''
        url = 'https://graphql.anilist.co'
        variables = {'search': title}
        query = '''
        query ($search: String) {
            Page(perPage: 10) {
                media(search: $search, type: MANGA) {
                    id
                    title {
                        english
                        romaji
                    }
                    format
                    startDate {
                        year
                        month
                        day
                    }
                }
            }
            }
        '''
        response = requests.post(url, json={'query': query, 'variables': variables})
        authour = ctx.message.author
        finalstr = ''

        try:
            decoded = response.content.decode('utf-8')
            replaced = decoded.replace('null', 'None')
            full_dict = eval(replaced)
        except:
            return await ctx.send(f'**Error**: No results found for "{title}". Make sure to use the correct English/Romaji title.')

        if 'error' in full_dict:
            return await ctx.send(f'**Error**: No results found for "{title}". Make sure to use the correct English/Romaji title.')
       
        page = full_dict['data']['Page']['media']
        i = 1
        for entry in page:
            # We have logged 5 entries
            if i == 6:
                break
            yr = str(entry['startDate']['year'])
            mediatype = entry['format']
            temptitle = entry['title']['english']
            if not temptitle:
                temptitle = entry['title']['romaji']
            if yr and mediatype and temptitle:
                finalstr += f'{i}. ' + temptitle + f' ({yr} {mediatype})\n'
                i += 1

        await ctx.send("**Please select a manga by typing a number from 1-5, or type 'cancel' to stop the search:**\n" + finalstr)

            
        try:
            msg = await self.client.wait_for('message', timeout=45.0, check=lambda message: (message.content.split()[0].isnumeric() or message.content.lower() == 'cancel') and message.author == authour)
            if msg.content.lower == 'cancel':
                return
            number = int(msg.content.split()[0]) - 1
            try:
                name = page[number]['title']['english']
                tempid = page[number]['id']
            except KeyError:
                return await ctx.send('**Error**: Cannot find manga with that number.')
            if not name:
                name = page[number]['title']['romaji']
            if name:
                return await self.manga(ctx, title=None, manga_id=tempid)
        except TimeoutError:
            print(f'Mangasearch timed out for {authour}')
    
















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




    async def _animeEp(self, ctx, ep_num, mal_id):
        jikan = Jikan()
        if not ep_num.isnumeric():
            return await ctx.send("**Error**: `episode=` must be a number!  ")
        try:
            result = jikan.anime(mal_id)
        except:
            return await ctx.send('Episode search is unavailable for now :( Please try again later.')
        anime_title = result['title']
        authour = ctx.message.author
        
        

        if int(self._num_episodes(mal_id)) < int(ep_num):
            return await ctx.send(f'**Error**: Unable to find Episode {ep_num} for {anime_title}.')

        page = int(ep_num) // 100
        if not (int(ep_num) % 100 == 0):
            page += 1
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

        await ctx.send(f'**Error**: Unable to find Episode {ep_num} for {anime_title}.')


















    # Errors
    @anime.error
    async def anime_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Invalid syntax: Use `-anime <name> episode=<#>`, or -animesearch <name> to search for an anime. ")

    @manga.error
    async def manga_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Invalid syntax: Use `-manga <name>`, or -mangasearch <name> to search for a manga.")

    @animesearch.error
    async def animesearch_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Invalid syntax: Use `-animesearch <name>`")

    @mangasearch.error
    async def mangasearch_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Invalid syntax: Use `-mangasearch <name>`")
    




def setup(client):
    client.add_cog(AnimeManga(client))    