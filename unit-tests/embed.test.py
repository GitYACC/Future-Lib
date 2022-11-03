import unittest

from future import embed
from future import component

from PIL import Image

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

    def test_Embed_flags(self):
        self.assertEqual(self.embed.dim.first, 1000)
        self.assertEqual(self.embed.dim, self.embed._dim)
        self.assertEqual(self.embed.font, self.embed._font)
        self.assertEqual(self.embed.banner, self.embed._banner)
        self.assertEqual(self.embed.hasLining, self.embed._lining)
        self.assertEqual(self.embed.backgroundColor, self.embed._back_fill)
        self.assertEqual(self.embed.foregroundColor, self.embed._front_fill)
        self.assertEqual(self.embed.children, self.embed._children)

    def test_set_font(self):
        with self.assertRaises(TypeError):
            self.embed.set_font("wrong file")

    def test_ImageProcessing_ratio(self):
        img = Image.open("github-pic.png")
        cmp = component.BaseComponent("name", component.ComponentType.TEXT, **{"ratio": 50})
        # finish later