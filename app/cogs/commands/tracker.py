import asyncio
import time
from discord.ext import tasks, commands

from statlib.api import get_now_playing
from statlib.database.handlers import ListeningHandler


class Tracker(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.last_progress = None
        self.last_track = None
        self.last_artist = None
        self.last_timestamp = None
        self.track_loop.start()

    @tasks.loop(seconds=5)
    async def track_loop(self):
        data = await get_now_playing()
        now = time.time()

        if not data:
            self.last_progress = None
            self.last_track = None
            self.last_artist = None
            self.last_timestamp = now
            return

        track = data["track"]
        artist = data["artist"]
        progress = data["progress_ms"]
        is_playing = data["is_playing"]

        if not is_playing:
            self.last_progress = progress
            self.last_timestamp = now
            return

        if (
            self.last_track == track
            and self.last_artist == artist
            and self.last_progress is not None
        ):
            real_delta = (progress - self.last_progress) / 1000

            if 0 < real_delta <= 15:
                ListeningHandler.insert_entry(track, artist, real_delta)

        self.last_track = track
        self.last_artist = artist
        self.last_progress = progress
        self.last_timestamp = now

    @track_loop.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(Tracker(bot))