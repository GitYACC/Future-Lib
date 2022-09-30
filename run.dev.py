import lightbulb
import hikari
from future import *


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
    id = 724002247360380979


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
    embed = BaseEmbed(
        size=EmbedSize.LARGE, 
        font_size=48, 
        banner=(255, 255, 0)
    )

    embed.add_component(
        BaseComponent(
            name="row0col0", 
            type=ComponentType.TEXT, 
            **{
                "position": (30, 30),
                "text": "Hello World",
                "text-color": (255, 255, 0),
                #"italicize": True
            }
        )
    ).add_component(
        BaseComponent(
            name="image",
            type=ComponentType.IMAGE,
            **{
                "position": (30, 100),
                "image": "./github-pic.png",
                "ratio": 50,
                "border-radius": 1
            }
        )
    )
    
    await ctx.respond(attachment=embed.save(name="test", fp="."))



bot.run()