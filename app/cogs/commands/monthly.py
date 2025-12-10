import io
import calendar
import discord
import matplotlib.pyplot as plt
from discord.ext import commands
from discord import app_commands

from statlib.database.handlers import StatsHandler, TracksHandler
from statlib import logger, EMBED_COLOR, get_artist_image, get_track_image


class Monthly(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="monthly",
        description="Show your listening stats for the current month."
    )
    async def monthly(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

        try:
            summary = StatsHandler.get_this_month()
            minutes = round(summary.total_seconds / 60)

            top_tracks = TracksHandler.get_top_tracks_month()
            top_artists = TracksHandler.get_top_artists_month()
            daily = StatsHandler.get_this_month_daily_breakdown()

            embed = discord.Embed(
                title="Monthly Listening Stats",
                description=f"You have listened for **{minutes:,} minutes** this month.",
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

            year = summary.timestamp.year if hasattr(summary, "timestamp") else None
            month = summary.timestamp.month if hasattr(summary, "timestamp") else None

            if not year or not month:
                from datetime import datetime
                now = datetime.now()
                year = now.year
                month = now.month

            days_in_month = calendar.monthrange(year, month)[1]
            days = list(range(1, days_in_month + 1))

            plt.style.use("https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle")
            fig, ax = plt.subplots(figsize=(14, 4))

            ax.bar(days, daily, color="#1DB954", edgecolor="#1DB954")
            ax.set_xlabel("Day of Month")
            ax.set_ylabel("Minutes")
            ax.set_title("This Month's Listening Activity")

            plt.tight_layout()

            buffer = io.BytesIO()
            plt.savefig(buffer, format="png", bbox_inches="tight", dpi=300)
            buffer.seek(0)
            plt.close()

            file = discord.File(buffer, filename="monthgraph.png")
            embed.set_image(url="attachment://monthgraph.png")

            await interaction.edit_original_response(embed=embed, attachments=[file])

        except Exception as error:
            logger.error(error)
            await interaction.edit_original_response(
                content="Something went wrong. Please try again later."
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Monthly(bot))
