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
    
    return [(alt, url) for alt, url in re.findall(r"!\[(.*?)\]\((.*?)\)", text)]

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    if not text:
        return []
    return [(alt, url) for alt, url in re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)]

def split_nodes_by_pattern(old_nodes: list[TextNode], pattern: str, node_type: TextType):
    new_nodes = []
    for node in old_nodes:
        matches: list[dict] = [{"start": m.start(), "end": m.end(), "groups": m.groups()} for m in re.finditer(pattern, node.text)]
        if len(matches) == 0:
            new_nodes.append(node)
        else:
            cur_loc = 0
            for i, match in enumerate(matches):
                (alt, url) = match["groups"]
                if match["start"] > cur_loc:
                    new_nodes.append(TextNode(node.text[cur_loc:match["start"]],node.text_type, node.url))
                    new_nodes.append(TextNode(alt, node_type, url))
                else:
                    new_nodes.append(TextNode(alt, node_type, url))
                
                cur_loc = match["end"]

            if cur_loc != len(node.text):
                new_nodes.append(TextNode(node.text[cur_loc:],node.text_type, node.url))

    return new_nodes


                    
def split_nodes_image(old_nodes: list[TextNode]):
    return split_nodes_by_pattern(old_nodes, r"!\[(.*?)\]\((.*?)\)", TextType.IMAGE)


def split_nodes_link(old_nodes):
    return split_nodes_by_pattern(old_nodes, r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", TextType.LINK)

def text_to_textnodes(text: str):
    pass

    


if __name__ == "__main__":
    text: str = "[alt1](url1.png) some text ![alt2](url2.jpg) ![alt3](url3.gif)"
    output = split_nodes_link([TextNode(text, TextType.TEXT)])
    print(output)
    text_single = "[url1](url1.png)"
    text_node = TextNode(text_single, TextType.TEXT, None)
    result = split_nodes_link([text_node])
    print(result)