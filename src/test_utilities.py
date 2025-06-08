import unittest
import json
from utilities import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from htmlnode import HtmlNode, ParentNode, LeafNode
from textnode import TextNode, TextType

class TestUtilities(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        text_node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

        text_node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

        text_node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

        text_node = TextNode("This is a link text node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

        text_node = TextNode("This is a link text node", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.google.com", "alt": "This is a link text node"})

    def test_split_nodes_delimiter(self):
        text_nodes = [
            TextNode("This is a plain text node", TextType.TEXT),
            TextNode("This is a *bold* text node", TextType.TEXT),
            TextNode("This is a _italic_ text node", TextType.TEXT),
            TextNode("This is text node has a `code block`", TextType.TEXT),
        ]
        
        ### BOLD ###
        # print(f"bold tests: {text_nodes[1:2]}")
        new_nodes = split_nodes_delimiter(text_nodes[1:2], "*", TextType.BOLD)
        # print("resulting nodes: ", new_nodes)
        type_map: dict = {}
        # print("type map:")
        for node in new_nodes:
            # print(f"{node.text}: {node.text_type}")
            type_map[node.text] = node.text_type
        self.assertEqual("This is a " in type_map, True)
        self.assertEqual(type_map["This is a "], TextType.TEXT)
        self.assertEqual("bold" in type_map, True)
        self.assertEqual(type_map["bold"], TextType.BOLD)
        self.assertEqual(" text node" in type_map, True)
        self.assertEqual(type_map[" text node"], TextType.TEXT)

        ### ITALICS ###
        new_nodes = split_nodes_delimiter(text_nodes[2:3], "_", TextType.ITALIC)
        type_map = {}
        for node in new_nodes:
            type_map[node.text] = node.text_type
        self.assertEqual("This is a " in type_map, True)
        self.assertEqual(type_map["This is a "], TextType.TEXT)
        self.assertEqual("italic" in type_map, True)
        self.assertEqual(type_map["italic"], TextType.ITALIC)
        self.assertEqual(" text node" in type_map, True)
        self.assertEqual(type_map[" text node"], TextType.TEXT)

        ### CODE ###
        # print(f"code test: {text_nodes[3:4]}")
        new_nodes = split_nodes_delimiter(text_nodes[3:4], "`", TextType.CODE)
        # print("resulting nodes: ", new_nodes)
        type_map = {}
        for node in new_nodes:
            type_map[node.text] = node.text_type
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual("This is text node has a " in type_map, True)
        self.assertEqual(type_map["This is text node has a "], TextType.TEXT)
        self.assertEqual("code block" in type_map, True)
        self.assertEqual(type_map["code block"], TextType.CODE)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        # Test with empty string
        self.assertListEqual(extract_markdown_images(""), [])

        # Test with text but no images
        self.assertListEqual(extract_markdown_images("This is plain text."), [])

        # Test with multiple images
        text_multiple = "![alt1](url1.png) some text ![alt2](url2.jpg) ![alt3](url3.gif)"
        expected_multiple = [("alt1", "url1.png"), ("alt2", "url2.jpg"), ("alt3", "url3.gif")]
        res_multiple = extract_markdown_images(text_multiple)
        self.assertEqual(res_multiple[0], expected_multiple[0])
        self.assertEqual(res_multiple[1], expected_multiple[1])
        self.assertEqual(res_multiple[2], expected_multiple[2])

        # Test image at the beginning
        text_beginning = "![start](start.png) and some text"
        expected_beginning = [("start", "start.png")]
        self.assertListEqual(extract_markdown_images(text_beginning), expected_beginning)

        # Test image at the end
        text_end = "Some text and ![end](end.png)"
        expected_end = [("end", "end.png")]
        self.assertListEqual(extract_markdown_images(text_end), expected_end)

        # Test with empty alt text
        self.assertListEqual(extract_markdown_images("![](empty_alt.png)"), [("", "empty_alt.png")])

        # Test with empty URL
        self.assertListEqual(extract_markdown_images("![alt_empty_url]()"), [("alt_empty_url", "")])

        # Test with alt text containing special characters (including brackets)
        text_special_alt = "![alt [with] !@#$*()](special_alt.svg)"
        expected_special_alt = [("alt [with] !@#$*()", "special_alt.svg")]
        self.assertListEqual(extract_markdown_images(text_special_alt), expected_special_alt)

        '''# Test with URL containing special characters (including parentheses)
        text_special_url = "![special_url_alt](https://example.com/path?query=value(1)&another=param#fragment)"
        expected_special_url = [("special_url_alt", "https://example.com/path?query=value(1)&another=param#fragment")]
        self.assertListEqual(extract_markdown_images(text_special_url), expected_special_url)'''

        # Test with no space between closing bracket and opening parenthesis
        self.assertListEqual(extract_markdown_images("![no_space](no_space.bmp)"), [("no_space", "no_space.bmp")])
        
        # Test malformed markdown (should not match)
        self.assertListEqual(extract_markdown_images("![alt(malformed.png"), []) # Missing ]
        self.assertListEqual(extract_markdown_images("![alt](malformed.png"), []) # Missing closing )
        self.assertListEqual(extract_markdown_images("!alt](malformed.png)"), [])  # Missing [
        self.assertListEqual(extract_markdown_images("[alt](not_an_image.png)"), []) # Missing !, this is a link





        # Test mixed valid and invalid
        '''text_mixed = "Valid: ![img1](url1.png). Invalid: ![img2(url2.png. Valid again: ![img3](url3.png)"
        expected_mixed = [("img1", "url1.png"), ("img3", "url3.png")]
        self.assertListEqual(extract_markdown_images(text_mixed), expected_mixed)'''


    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([], matches)

        # Invalid space between braces
        matches = extract_markdown_links("This is text with an [link] (https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([], matches)


        





        

        