import lightbulb
import hikari
from dataclasses import dataclass
from future.discord.embed import BaseEmbed

@dataclass
class TestServer:
    client_secret: str = "NzI0MDAzMjU1NDIzODYwNzY5.Xu52kw.5WPfqBkpqTPfk_qs6fai0xtdv4A"
    id: int = 724002247360380979


bot = lightbulb.BotApp(
    intents=hikari.Intents.ALL,
    token=TestServer.client_secret,
    default_enabled_guilds=TestServer.id,
    banner=None
)

@bot.command
@lightbulb.command("embed", "test embed")
@lightbulb.implements(lightbulb.SlashCommand)
async def test_command(ctx: lightbulb.Context):
    embed = BaseEmbed(

    )

    await ctx.respond(
        embed=embed,
        components=[]
    )



