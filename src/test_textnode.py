import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_valid_default_url(self):
        node = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node.url, None)

    def test_is_secure_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        self.assertTrue("https", node.url[:5])
    
    def test_is_insecure_url(self):
        node = TextNode("This is a text node", TextType.LINK, "http://www.google.com")
        self.assertTrue("http:", node.url[:5])

    def test_is_valid_code(self):
        node = TextNode("```print('This is a text node')```", TextType.CODE)
        self.assertGreater(len(node.text), 6)
        self.assertTrue("```", node.text[:3])
        self.assertTrue("```", node.text[-3:])





if __name__ == "__main__":
    unittest.main()