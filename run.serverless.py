from future import *

em = embed.BaseEmbed()

cmp = BaseComponent(
        "cmp1",
        component.ComponentType.TEXT,
        **{
            "text": "Hello World",
            "text-color": (255, 205, 155)
        }
)

pos = em.center_with(cmp)
cmp.pos = pos

em.add_component(
    cmp
)

em.save("test")