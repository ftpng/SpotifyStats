import discord
from discord.ext import commands
from discord import app_commands

from statlib.database.handlers import TracksHandler
from statlib import logger, EMBED_COLOR, get_artist_image


class TopArtists(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="topartists",
        description="Show your top 10 most listened-to artists."
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def topartists(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        
        try:
            top_artists = TracksHandler.get_top_artists(limit=10)

            embed = discord.Embed(
                title="Top Artists",
                description="Most listened-to artists of all time",
                color=EMBED_COLOR
            )

            if top_artists:
                artist_lines = [
                    f"`{i+1}.` {artist.artist_name} - `{round(artist.total_seconds / 60)} min`"
                    for i, artist in enumerate(top_artists)
                ]
                embed.add_field(
                    name="Leaderboard",
                    value="\n".join(artist_lines),
                    inline=False
                )

                thumbnail = await get_artist_image(top_artists[0].artist_name)
                if thumbnail:
                    embed.set_thumbnail(url=thumbnail)

            else:
                embed.description = "No listening data available."

            await interaction.edit_original_response(embed=embed)

        except Exception as error:
            logger.error(error)
            await interaction.edit_original_response(
                content="Something went wrong. Please try again later."
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TopArtists(bot))