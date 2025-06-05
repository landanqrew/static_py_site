import unittest
from htmlnode import HtmlNode, LeafNode


class HtmlNodeTest(unittest.TestCase):
    def test_is_valid_node(self):
        node = HtmlNode("p", "some text...", None, None)
        if node.tag or node.value or node.children or node.props:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_is_valid_a_tag(self):
        node = HtmlNode("a", None, None, {"href": "https://google.com"})
        self.assertTrue(node.tag == "a" and node.props)

    def test_is_valid_div_tag(self):
        node = HtmlNode("div", None, None, {"class": "some-class", "id": "some-id"})
        self.assertTrue(node.tag == "div" and node.props)

    def test_is_valid_header(self):
        node = HtmlNode("h", "some_header", None, None)
        self.assertTrue(node.tag == "h" and node.value)

    def test_props_to_html(self):
        node = HtmlNode("div", None, None, {"class": "some-class", "id": "some-id"})
        '''props_str = node.props_to_html()
        print(f"props_str: {props_str}")'''
        self.assertTrue(node.props_to_html() == " class=\"some-class\" id=\"some-id\"")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        # Tests LeafNode.to_html() when no tag is provided.
        node = LeafNode(None, "This is raw text.")
        self.assertEqual(node.to_html(), "This is raw text.")

    def test_leaf_to_html_with_tag_and_props(self):
        # Tests LeafNode.to_html() with a tag and properties.
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\" target=\"_blank\">Click me!</a>")

    def test_leaf_constructor_value_error_on_none_value(self):
        # Tests that LeafNode constructor raises ValueError if value is None.
        with self.assertRaisesRegex(ValueError, "cannot instantiate leaf node without value"):
            LeafNode(value=None, tag="p")


if __name__ == '__main__':
    unittest.main()


