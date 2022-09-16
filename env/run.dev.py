import lightbulb
import hikari
from dataclasses import dataclass
from future.discord.embed import BaseEmbed
from base64 import urlsafe_b64decode

@dataclass
class TestServer:
    client_secret: bytes = b"TnpJME1EQXpNalUxTkRJek9EWXdOelk1LkdmbkFoVi51UDVRVGJMVW95TDl6VExHV2djVFF5LUM3YlI1M1FsOGZzWndUMA=="
    id: int = 724002247360380979


bot = lightbulb.BotApp(
    intents=hikari.Intents.ALL,
    token=urlsafe_b64decode(
        TestServer.client_secret
    ),
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



