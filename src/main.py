from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode


def main():
    txt_node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    return txt_node

if __name__ == "__main__":
    print(main())