import lightbulb
import hikari
from dataclasses import dataclass
from future.discord import \
    BaseEmbed,             \
    BaseComponent,         \
    ComponentType


@dataclass
class TestServer:
    client_secret = [
        "NzI0MDA", 
        "zMjU1NDIz", 
        "ODYwNzY5.GzeO", 
        "4_.vYnSuerN", 
        "nSjbld3T", 
        "1QWjxHKND", 
        "VVsvbib", 
        "lTAacM"
    ]
    id: int = 724002247360380979


bot = lightbulb.BotApp(
    #intents=hikari.Intents.ALL,
    token="".join(TestServer.client_secret),
    default_enabled_guilds=TestServer.id,
    banner=None
)

@bot.command
@lightbulb.command("embed", "test embed")
@lightbulb.implements(lightbulb.SlashCommand)
async def test_command(ctx: lightbulb.Context):
    component_flags = {
        "position": (10, 10),
        "text": "Hello World"
    }
    embed = BaseEmbed()
    embed.add_component(
        BaseComponent(
            name="row0col0", 
            type=ComponentType.TEXT, 
            **component_flags
        )
    )
    
    await ctx.respond(attachment=embed.save(name="test", fp="../env"))



bot.run()