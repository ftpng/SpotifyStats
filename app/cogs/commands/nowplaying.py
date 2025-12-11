from discord.ext import commands
from discord import app_commands, Interaction, Embed

from statlib import logger, EMBED_COLOR
from statlib.api import get_now_playing


class NowPlaying(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client: commands.Bot = client


    @app_commands.command(
        name="nowplaying", 
        description="Show currently listening to on Spotify."
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def nowplaying(self, interaction: Interaction):
        await interaction.response.defer()
        
        try:
            data = await get_now_playing()

            if data is None:
                return await interaction.edit_original_response(
                    content="You are not currently listening to anything on Spotify."
                )

            embed = Embed(
                title = "You are currently listening to",
                description=(
                    f"`{data['track']} - {data['artist']}`\n\n"
                    f"[Open in Spotify]({data['url']})"
                ),
                color=EMBED_COLOR
            )
            embed.set_thumbnail(url=data["thumbnail"])

            await interaction.edit_original_response(
                embed=embed
            )        

        except Exception as error:
            logger.error(error)

            return await interaction.edit_original_response(
                content="Something went wrong. Please try again later."
            )


async def setup(client: commands.Bot) -> None:
    await client.add_cog(NowPlaying(client))    