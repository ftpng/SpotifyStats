import io
import discord
import matplotlib.pyplot as plt
from discord.ext import commands
from discord import app_commands

from statlib.database.handlers import StatsHandler, TracksHandler
from statlib import logger, EMBED_COLOR, get_artist_image, get_track_image


class Daily(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="daily",
        description="Show your listening stats for today."
    )
    async def daily(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

        try:
            summary = StatsHandler.get_today()
            minutes = round(summary.total_seconds / 60)

            top_tracks = TracksHandler.get_top_tracks_today()
            top_artists = TracksHandler.get_top_artists_today()
            hourly = StatsHandler.get_today_hourly_breakdown()

            embed = discord.Embed(
                title="Daily Listening Stats",
                description=f"You have listened for **{minutes:,} minutes** today.",
                color=EMBED_COLOR
            )

            if top_artists:
                artist_lines = [
                    f"`{i+1}.` {artist.artist_name} - `{round(artist.total_seconds / 60)} min`"
                    for i, artist in enumerate(top_artists)
                ]
                embed.add_field(name="Top Artists", value="\n".join(artist_lines), inline=False)

            if top_tracks:
                track_lines = [
                    f"`{i+1}.` {track.track_name} - `{round(track.total_seconds / 60)} min`"
                    for i, track in enumerate(top_tracks)
                ]
                embed.add_field(name="Top Tracks", value="\n".join(track_lines), inline=False)

            thumbnail = None

            if top_artists:
                thumbnail = await get_artist_image(top_artists[0].artist_name)

            if not thumbnail and top_tracks:
                track = top_tracks[0]
                thumbnail = await get_track_image(track.track_name, "")

            if thumbnail:
                embed.set_thumbnail(url=thumbnail)

            hours = list(range(24))

            plt.style.use("https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle")
            fig, ax = plt.subplots(figsize=(12, 4))

            ax.bar(hours, hourly, color="#1DB954", edgecolor="#1DB954")
            ax.set_xlabel("Hour of Day")
            ax.set_ylabel("Minutes")
            ax.set_title("Today's Listening Activity")

            plt.tight_layout()

            buffer = io.BytesIO()
            plt.savefig(buffer, format="png", bbox_inches="tight", dpi=300)
            buffer.seek(0)
            plt.close()

            file = discord.File(buffer, filename="dailygraph.png")
            embed.set_image(url="attachment://dailygraph.png")

            await interaction.edit_original_response(embed=embed, attachments=[file])

        except Exception as error:
            logger.error(error)
            await interaction.edit_original_response(
                content="Something went wrong. Please try again later."
            )
            

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Daily(bot))
