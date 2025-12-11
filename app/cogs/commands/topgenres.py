import discord
from discord.ext import commands
from discord import app_commands

from statlib.database.handlers import TracksHandler
from statlib import logger, EMBED_COLOR, get_artist_image, get_artist_genres


class TopGenres(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="topgenres",
        description="Show your most listened-to music genres."
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def topgenres(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        
        try:
            artist_totals = TracksHandler.get_artist_totals()

            if not artist_totals:
                await interaction.followup.send("No listening data available.")
                return

            genre_map = {}

            for artist, total_seconds in artist_totals:
                genres = await get_artist_genres(artist)

                for genre in genres:
                    genre_map[genre] = genre_map.get(genre, 0) + total_seconds

            if not genre_map:
                await interaction.followup.send("No genres could be resolved from Spotify.")
                return

            sorted_genres = sorted(
                genre_map.items(),
                key=lambda x: x[1],
                reverse=True
            )

            top_genres = sorted_genres[:10]

            embed = discord.Embed(
                title="Top Genres",
                description="Most listened-to genres",
                color=EMBED_COLOR
            )

            lines = [
                f"`{i+1}.` {genre} - `{round(seconds / 60)} min`"
                for i, (genre, seconds) in enumerate(top_genres)
            ]
            embed.add_field(
                name="Genre Rankings",
                value="\n".join(lines),
                inline=False
            )

            top_artist = artist_totals[0][0]
            thumb = await get_artist_image(top_artist)
            if thumb:
                embed.set_thumbnail(url=thumb)

            await interaction.edit_original_response(embed=embed)

        except Exception as error:
            logger.error(error)
            await interaction.edit_original_response(
                "Something went wrong. Please try again later."
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(TopGenres(bot))