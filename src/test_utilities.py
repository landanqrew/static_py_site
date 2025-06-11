import unittest
import json
from utilities import *
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


    def test_split_image_nodes(self):
        self.maxDiff = None
        text_multiple = "![alt1](url1.png) some text ![alt2](url2.jpg) ![alt3](url3.gif)"
        text_node = TextNode(text_multiple, TextType.TEXT, None)
        compare_list: list[TextNode] = [
            TextNode("alt1", TextType.IMAGE, "url1.png"),
            TextNode(" some text ", TextType.TEXT),
            TextNode("alt2", TextType.IMAGE, "url2.jpg"),
            TextNode(" ", TextType.TEXT),
            TextNode("alt3", TextType.IMAGE, "url3.gif")
        ]
        result: list[TextNode] = split_nodes_image([text_node])
        # print(result)
        self.assertListEqual(result, compare_list)

        # test links
        text_multiple = "[url1](url1.png) some text [url2](url2.jpg) [alt3](url3.gif)"
        text_node = TextNode(text_multiple, TextType.TEXT, None)
        self.assertListEqual(split_nodes_image([text_node]), [text_node])

        text_single = "![image](url1.png)"
        text_node = TextNode(text_single, TextType.TEXT, None)
        result_node = TextNode("image", TextType.IMAGE, "url1.png")
        func_res = split_nodes_image([text_node])
        # print(func_res)
        self.assertListEqual(func_res, [result_node])

    def test_split_link_nodes(self):
        self.maxDiff = None
        text_multiple = "[url1](url1.png) some text [url2](url2.jpg) [alt3](url3.gif)"
        text_node = TextNode(text_multiple, TextType.TEXT, None)
        compare_list: list[TextNode] = [
            TextNode("url1", TextType.LINK, "url1.png"),
            TextNode(" some text ", TextType.TEXT),
            TextNode("url2", TextType.LINK, "url2.jpg"),
            TextNode(" ", TextType.TEXT),
            TextNode("alt3", TextType.LINK, "url3.gif")
        ]
        result: list[TextNode] = split_nodes_link([text_node])
        #print(result)
        self.assertListEqual(result, compare_list)

        # test images
        text_multiple = "![alt1](url1.png) some text ![alt2](url2.jpg) ![alt3](url3.gif)"
        text_node = TextNode(text_multiple, TextType.TEXT, None)
        self.assertListEqual(split_nodes_link([text_node]), [text_node])

        # single link
        text_single = "[url1](url1.png)"
        text_node = TextNode(text_single, TextType.TEXT, None)
        result_node = TextNode("url1", TextType.LINK, "url1.png")
        func_res = split_nodes_link([text_node])
        # print(func_res)
        self.assertListEqual(func_res, [result_node])


        
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


    def test_text_to_textnode(self):
        text: str = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        compare_list: list[TextNode] = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertListEqual(text_to_textnodes(text), compare_list)


    def test_markdown_to_blocks(self):
        md: str = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

        





        

        