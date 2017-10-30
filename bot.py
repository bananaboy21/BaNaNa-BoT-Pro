import discord
import os
import io
import textwrap
from contextlib import redirect_stdout
import traceback
from discord.ext import commands 
bot = commands.Bot(command_prefix='*',description="This bot is weird. Deal with it. Owner: dat banana boi #1982, with help of Free TNT 5796\n\nHelp Commands",owner_id=277981712989028353)

def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    return content.strip('` \n')

@bot.event
async def on_ready():
   print('Bot is online!') 


@bot.command()
async def say(ctx, *, message: str):
    """Say Something As The Bot""" 
    await ctx.send(message)

   
@bot.command()
async def ping(ctx):
    """Pong! Returns your websocket latency."""
    em = discord.Embed()
    em.title ='Pong! Websocket Latency:'
    em.description = f"{bot.ws.latency * 1000:.4f} ms"
    await ctx.send(embed=em)
    

@bot.command(pass_context=True, hidden=True, name='eval')
@commands.is_owner()
async def _eval(ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
        }

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        
        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                await ctx.send(f'```py\n{value}{ret}\n```')
 
     
@bot.command()
async def invite(ctx):
    """Invite me! I'm possible by Free TNT #5796 and dat banana boi#1982."""
    await ctx.send("Invite me to your server, for extra dankness. https://discordapp.com/oauth2/authorize?client_id=372129317108580352&scope=bot&permissions=66186303")
    
    
@bot.command()
async def discord(ctx):
    """Join my dank Discord server. For no dank reason."""
    await ctx.send("Join my Discord. For dank and for other stuff. Join: https://discord.gg/xSFetCJ")
    

@bot.command(name='presence')
@commands.is_owner()
async def _set(ctx, Type=None,*,thing=None):
  """Change the bot's discord game/stream!"""
  if Type is None:
    await ctx.send('Usage: `.presence [game/stream] [message]`')
  else:
    if Type.lower() == 'stream':
      await bot.change_presence(game=discord.Game(name=thing,type=1,url='https://www.twitch.tv/a'),status='online')
      await ctx.send(f'Set presence to. `Streaming {thing}`')
    elif Type.lower() == 'game':
      await bot.change_presence(game=discord.Game(name=thing))
      await ctx.send(f'Set presence to `Playing {thing}`')
    elif Type.lower() == 'clear':
      await bot.change_presence(game=None)
      await ctx.send('Cleared Presence')
    else:
      await ctx.send('Usage: `.presence [game/stream] [message]`')
    
    
def duration_to_str(duration):

    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    return f"{f'{days} days, ' if days > 0 else ''}{f'{hours} hours, ' if hours > 0 else ''}{f'{minutes} minutes, ' if minutes > 0 else ''}{seconds} seconds"


class MusicError(commands.UserInputError):
    pass


class Song(discord.PCMVolumeTransformer):
    ytdl_opts = {
        'default_search': 'auto',
        'format': 'bestaudio/best',
        'ignoreerrors': False,
        'source_address': '0.0.0.0', # Make all connections via IPv4
        'nocheckcertificate': True,
        'restrictfilenames': True,
        'logger': logging.getLogger(__name__),
        'logtostderr': False,
        'no_warnings': True,
        'quiet': True,
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s'
    }
    ytdl = youtube_dl.YoutubeDL(ytdl_opts)

    def __init__(self, info, requester, channel):
        self.info = info
        self.requester = requester
        self.channel = channel
        self.filename = info.get('_filename', self.ytdl.prepare_filename(info))
        source = info.get('url', info.get('file', None)                          
        
    @classmethod
    async def create(cls, query, requester, channel, loop=None):
        try:
            is_file = pathlib.Path(query).is_file()
        except:
            is_file = False

        if is_file:
            return cls.from_file(query, requester, channel)
        else:
            return await cls.from_ytdl(query, requester, channel, loop)



    @classmethod
    def from_file(cls, file, requester, channel):
        info = {
            'file': file,
            'title': pathlib.Path(file).stem,
            'creator': 'local file',         
        }
        return cls(info, requester, channel)



    @classmethod
    async def from_ytdl(cls, url, requester, channel, loop=None):
        loop = loop or asyncio.get_event_loop()
        info = await loop.run_in_executor(None, cls.ytdl.extract_info, url)



        if "entries" in info:

            info = info['entries'][0]


        return cls(info, requester, channel)



    def __str__(self):
        title = f"**{self.info['title']}**"
        creator = f"**{self.info.get('creator') or self.info['uploader']}**"
        duration = f" (duration: {duration_to_str(self.info['duration'])})" if 'duration' in self.info else ''
        return f'{title} from {creator}{duration}'


class Playlist(asyncio.Queue):
    def __iter__(self):
        return self._queue.__iter__()

    def clear(self):
        self._queue.clear()

    def get_song(self):
        return self.get_nowait()

    def add_song(self, song):
        self.put_nowait(song)

    def __str__(self):
        info = 'Current playlist:\n'
        info_len = len(info)
        for song in self:
            s = str(song)
            l = len(s) + 1 # Counting the extra \n
            if info_len + l > 1995:
                info += '[...]'
                break
            info += f'{s}\n'
            info_len += l
        return info

                          
class GuildMusicState:
    def __init__(self, loop):
        self.playlist = Playlist(maxsize=50)
        self.voice_client = None
        self.loop = loop
        self.player_volume = 0.5
        self.skips = set()
        self.min_skips = 5

    @property
    def current_song(self):
        return self.voice_client.source

    @property
    def volume(self):
        return self.player_volume

    @volume.setter
    def volume(self, value):
        self.player_volume = value
        if self.voice_client:
            self.voice_client.source.volume = value

    async def stop(self):
        self.playlist.clear()
        if self.voice_client:
            await self.voice_client.disconnect()
            self.voice_client = None

    def is_playing(self):
        return self.voice_client and self.voice_client.is_playing()

    async def play_next_song(self, song=None, error=None):
        if error:
            await self.current_song.channel.send(f'An error has occurred while playing {self.current_song}: {error}')

        if song and song.filename not in [s.filename for s in self.playlist]:
            os.remove(song.filename)

        if self.playlist.empty():
            await self.stop()
        else:
            next_song = self.playlist.get_song()
            next_song.volume = self.player_volume
            self.voice_client.play(next_song, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next_song(next_song, e), self.loop).result())
            await next_song.channel.send(f'Now playing {next_song}')


class Music:
    def __init__(self, bot):
        self.bot = bot
        self.music_states = {}

    def __unload(self):
        for state in self.music_states.values():
            self.bot.loop.create_task(state.stop())

    def __local_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command cannot be used in a private message.')
        return True

    async def __before_invoke(self, ctx):
        ctx.music_state = self.get_music_state(ctx.guild.id)

    async def __error(self, ctx, error):
        if not isinstance(error, commands.UserInputError):
            raise error

        try:
            await ctx.send(error)
        except discord.Forbidden:
            pass # /shrug

    def get_music_state(self, guild_id):
        return self.music_states.setdefault(guild_id, GuildMusicState(self.bot.loop))

    @commands.command()
    async def status(self, ctx):
        """Displays the currently played song."""
        if ctx.music_state.is_playing():
            song = ctx.music_state.current_song
            await ctx.send(f'Playing {song}. Volume at {song.volume * 100}% in {ctx.voice_client.channel.mention}')
        else:
            await ctx.send('Not playing.')

    @commands.command()
    async def playlist(self, ctx):
        """Shows info about the current playlist."""
        await ctx.send(f'{ctx.music_state.playlist}')

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        """Summons the bot to a voice channel.

        If no channel is given, summons it to your current voice channel.
        """
        if channel is None and not ctx.author.voice:
            raise MusicError('You are not in a voice channel nor specified a voice channel for me to join.')

        destination = channel or ctx.author.voice.channel

        if ctx.voice_client:
            await ctx.voice_client.move_to(destination)
        else:
            ctx.music_state.voice_client = await destination.connect()

    @commands.command()
    async def play(self, ctx, *, song: str):
        """Plays a song or adds it to the playlist.

        Automatically searches with youtube_dl
        List of supported sites :
        https://github.com/rg3/youtube-dl/blob/1b6712ab2378b2e8eb59f372fb51193f8d3bdc97/docs/supportedsites.md
        """
        await ctx.message.add_reaction('\N{HOURGLASS}')

        # Add the song to the playlist
        source = await Song.create(song, ctx.author, ctx.channel, loop=ctx.bot.loop)
        try:
            ctx.music_state.playlist.add_song(source)
        except asyncio.QueueFull:
            raise MusicError('Playlist is full, try again later.')

        # Connect to the voice channel if needed
        if ctx.voice_client is None or not ctx.voice_client.is_connected():
            await ctx.invoke(self.join)

        # Start playing or notify it's been added to the playlist
        if not ctx.music_state.is_playing():
            await ctx.music_state.play_next_song()
        else:
            await ctx.send(f'Queued {source} in position **#{ctx.music_state.playlist.qsize()}**')

        await ctx.message.remove_reaction('\N{HOURGLASS}', ctx.me)
        await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')

    @play.error
    async def play_error(self, ctx, error):
        await ctx.message.remove_reaction('\N{HOURGLASS}', ctx.me)
        await ctx.message.add_reaction('\N{CROSS MARK}')



    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def pause(self, ctx):
        """Pauses the player."""
        if ctx.voice_client:
            ctx.voice_client.pause()

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def resume(self, ctx):
        """Resumes the player."""
        if ctx.voice_client:
            ctx.voice_client.resume()

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def stop(self, ctx):
        """Stops the player, clears the playlist and leaves the voice channel."""
        await ctx.music_state.stop()

    @commands.command()
    async def volume(self, ctx, volume: int = None):
        """Sets the volume of the player, scales from 0 to 100."""
        if volume < 0 or volume > 100:
            raise MusicError('The volume level has to be between 0 and 100.')
        ctx.music_state.volume = volume / 100

    @commands.command()
    async def clear(self, ctx):
        """Clears the playlist."""
        ctx.music_state.playlist.clear()

    @commands.command()
    async def skip(self, ctx):
        """Votes to skip the current song.
        To configure the minimum number of votes needed, use `minskips`
        """
        if not ctx.music_state.is_playing():
            raise MusicError('Not playing anything to skip.')



        if ctx.author.id in ctx.music_state.skips:

            raise MusicError(f'{ctx.author.mention} You already voted to skip that song')

        # Count the vote
        ctx.music_state.skips.add(ctx.author.id)
        await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')

        # Check if the song has to be skipped
        if len(ctx.music_state.skips) > ctx.music_state.min_skips or ctx.author == ctx.music_state.current_song.requester:
            ctx.music_state.skips.clear()
            ctx.voice_client.stop()

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def minskips(self, ctx, number: int):
        """Sets the minimum number of votes to skip a song.

        Requires the `Manage Guild` permission.
        """
        ctx.music_state.min_skips = number
    
    
if not os.environ.get('TOKEN'):
    print("no token found REEEE!")
bot.run(os.environ.get('TOKEN').strip('"'))


