from htmlnode import HtmlNode, ParentNode, LeafNode
from textnode import TextNode, TextType
import re

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid text type")


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    
    new_nodes = []
    for node in old_nodes:
        delimiters = re.findall(f"r'{delimiter}'", node.text)
        if len(delimiters) != 0 and len(delimiters) % 2 != 0:
            raise Exception("Invalid delimiter count. Please ensure the number of delimiters is even")
        split_parts = node.text.split(delimiter)
        if len(split_parts) > 1:
            for i, part in enumerate(split_parts):
                if len(part) > 0:
                    new_nodes.append(TextNode(part, text_type if (i + 1) % 2 == 0 else node.text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    if not text:
        return []
    
    '''matches: list[re.Match[str]] = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    if not matches:
        return []'''
    return [(alt, url) for alt, url in re.findall(r"!\[(.*?)\]\((.*?)\)", text)]

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    if not text:
        return []
    return [(alt, url) for alt, url in re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)]


if __name__ == "__main__":
    res = extract_markdown_images("![alt1](url1.png) some text ![alt2](url2.jpg) ![alt3](url3.gif)")
    expected = [("alt1", "url1.png"), ("alt2", "url2.jpg"), ("alt3", "url3.gif")]
    print(f"res: {res}")
    print(f"expected: {expected}")
    print(res == expected)