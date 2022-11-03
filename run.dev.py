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
            name="text", 
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
    ).add_component(
        BaseComponent(
            name="html",
            type=ComponentType.HTML,
            **{
                "string-html": "<h1>Hello World from html!</h1>",
                "string-css": "h1 {color: yellow; background: blue;}",
                "ratio": 50,
                "position": (30, 200)
            }
        )
    ).add_component(
        BaseComponent(
            name="panel",
            type=ComponentType.PANEL,
            **{
                "position": (500, 35),
                "background-color": (0, 255, 0),
                "panel-size": (100, 100),
            }
        )
    ).add_component(
        BaseComponent(
            name="text",
            type=ComponentType.TEXT,
            **{
                "text": "Hello",
                "relative-position": (10, 10),
                "attached-to": embed._children["html"]
            }
        )
    )
    
    
    await ctx.respond(attachment=embed.save(name="test", fp="."))



#bot.run()

class T:
    pass

s = T()
print(s[0])