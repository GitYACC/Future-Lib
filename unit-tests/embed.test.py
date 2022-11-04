import unittest

from future import embed
from future import component

from PIL import Image
import numpy as np

class EmbedSettingTests(unittest.TestCase):
    def test_NTuple_functionality(self):
        test_tup = embed.NTuple(10, 10)
        with self.assertRaises(TypeError):
            self.assertEqual(test_tup[0], test_tup.first)
            self.assertEqual(test_tup[1], test_tup.second)

        with self.assertRaises(TypeError):
            test_tup[0] = 11
            self.assertEqual(test_tup.first, 11)

    def test_EmbedConfig(self):
        self.assertTrue(isinstance(embed.EmbedConfig, dict))

    def test_EmbedSize(self):
        self.assertEqual(embed.EmbedSize.SMALL, 250)
        self.assertEqual(embed.EmbedSize.NORMAL, 500)
        self.assertEqual(embed.EmbedSize.LARGE, 750)

class BaseEmbedTests(unittest.TestCase):
    def setUp(self):
        self.embed = embed.BaseEmbed()
        self.img = Image.open("github-pic.png")
        self.cmp_with_ratio = component.BaseComponent(
            "name", component.ComponentType.TEXT, **{"ratio": 50, "position": (30, 30)}
        )
        self.cmp_with_attached_to = component.BaseComponent(
            "name2", component.ComponentType.TEXT, **{"relative-pos": (10, 10)}
        )

        self.cmp_with_text = component.BaseComponent(
            "cmp1",
            component.ComponentType.TEXT,
            **{
                "text": "Hello World",
                "text-color": (255, 205, 155)
            }
        )
        pos = self.embed.center_with(self.cmp_with_text)
        self.cmp_with_text.pos = pos

    def test_Embed_flags(self):
        self.assertEqual(self.embed.dim.first, 1000)
        self.assertEqual(self.embed.dim, self.embed._dim)
        self.assertEqual(self.embed.font, self.embed._font)
        self.assertEqual(self.embed.hasBanner, self.embed._banner)
        self.assertEqual(self.embed.hasLining, self.embed._lining)
        self.assertEqual(self.embed.backgroundColor, self.embed._back_fill)
        self.assertEqual(self.embed.foregroundColor, self.embed._front_fill)
        self.assertEqual(self.embed.children, self.embed._children)

    def test_set_font(self):
        with self.assertRaises(TypeError):
            self.embed.set_font("wrong file")

    def test__get_pos(self):
        self.embed.add_component(self.cmp_with_ratio)
        self.cmp_with_attached_to.attached_to = self.embed.children["name"]
        self.assertEqual(self.embed._get_pos(self.cmp_with_attached_to), (40, 40))

    def test_ImageProcessing_ratio(self):      
        img_cmp = self.img.resize(
            (
                self.img.width * self.cmp_with_ratio / 100, 
                self.img.height * self.cmp_with_ratio / 100
            )
        )
        new_img = self.embed.ImageProcessing.ratio(self.cmp_with_ratio, self.img)
        self.assertEqual(new_img, img_cmp)

    def test_ImageProcessing_border_radius(self):
        bradius_img = self.embed.ImageProcessing.border_radius(self.embed, self.cmp_with_ratio, self.img)
        self.assertEqual(bradius_img, self.img)

    def test_add_component_TEXT(self):
        pass
        # finish