import discord
from discord.ext import commands
from discord import app_commands

from statlib.database.handlers import TracksHandler
from statlib import logger, EMBED_COLOR, get_track_image


class TopSongs(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="topsongs",
        description="Show your top 10 most listened-to songs."
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def topsongs(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        
        try:
            top_tracks = TracksHandler.get_top_tracks(limit=10)

            embed = discord.Embed(
                title="Top Songs",
                description="Most listened-to songs of all time",
                color=EMBED_COLOR
            )

            if top_tracks:
                track_lines = [
                    f"`{i+1}.` {track.track_name} - `{round(track.total_seconds / 60)} min`"
                    for i, track in enumerate(top_tracks)
                ]
                embed.add_field(
                    name="Leaderboard",
                    value="\n".join(track_lines),
                    inline=False
                )

                thumbnail = await get_track_image(top_tracks[0].track_name, "")
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
    await bot.add_cog(TopSongs(bot))