import unittest
from htmlnode import HtmlNode


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
        self.assertTrue(node.props_to_html() == "class=\"some-class\" id=\"some-id\"")


if __name__ == '__main__':
    unittest.main()


