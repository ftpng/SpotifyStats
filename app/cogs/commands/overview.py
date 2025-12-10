import io
import discord
import matplotlib.pyplot as plt
from discord.ext import commands
from discord import app_commands

from statlib import logger, EMBED_COLOR, get_artist_image, get_track_image
from statlib.database.handlers import StatsHandler, TracksHandler
from statlib.api import get_now_playing


class Overview(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="overview",
        description="Show your full Spotify listening overview for this year."
    )
    async def overview(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

        try:
            summary = StatsHandler.get_this_year()
            minutes = round(summary.total_seconds / 60)

            top_tracks = TracksHandler.get_top_tracks_year()
            top_artists = TracksHandler.get_top_artists_year()

            monthly = StatsHandler.get_this_year_monthly_breakdown()
            months = [
                "Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"
            ]

            now_playing = await get_now_playing()

            description = (
                f"Total listening time this year: `{minutes:,} minutes`"
            )

            if now_playing:
                description += (
                    "\nNow Playing: "
                    f"[{now_playing['track']} - {now_playing['artist']}]({now_playing['url']})"
                )

            embed = discord.Embed(
                title="Spotify Overview",
                description=description,
                color=EMBED_COLOR
            )

            if top_artists:
                artist_lines = [
                    f"`{i+1}.` {artist.artist_name} - `{round(artist.total_seconds / 60)} min`"
                    for i, artist in enumerate(top_artists)
                ]
                embed.add_field(
                    name="Top Artists",
                    value="\n".join(artist_lines),
                    inline=False
                )

            if top_tracks:
                track_lines = [
                    f"`{i+1}.` {track.track_name} - `{round(track.total_seconds / 60)} min`"
                    for i, track in enumerate(top_tracks)
                ]
                embed.add_field(
                    name="Top Tracks",
                    value="\n".join(track_lines),
                    inline=False
                )

            thumbnail = None

            if now_playing:
                thumbnail = now_playing.get("thumbnail")

            if not thumbnail and top_artists:
                thumbnail = await get_artist_image(top_artists[0].artist_name)

            if not thumbnail and top_tracks:
                track = top_tracks[0]
                thumbnail = await get_track_image(track.track_name, "")

            if thumbnail:
                embed.set_thumbnail(url=thumbnail)

            plt.style.use("https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle")

            fig, ax = plt.subplots(figsize=(12, 4))
            ax.bar(months, monthly, color="#1DB954", edgecolor="#1DB954")

            ax.set_title("Minutes Listened Per Month")
            ax.set_ylabel("Minutes")
            plt.tight_layout()

            buffer = io.BytesIO()
            plt.savefig(buffer, format="png", bbox_inches="tight", dpi=300)
            buffer.seek(0)
            plt.close()

            file = discord.File(buffer, filename="yearlygraph.png")
            embed.set_image(url="attachment://yearlygraph.png")

            await interaction.edit_original_response(embed=embed, attachments=[file])

        except Exception as error:
            logger.error(error)
            await interaction.edit_original_response(
                content="Something went wrong. Please try again later."
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Overview(bot))