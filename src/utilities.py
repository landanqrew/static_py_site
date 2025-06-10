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
        if len(matches) == 0 or node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            cur_loc = 0
            for i, match in enumerate(matches):
                if len(match["groups"]) > 1:
                    (alt, url) = match["groups"]
                    if match["start"] > cur_loc:
                        new_nodes.append(TextNode(node.text[cur_loc:match["start"]],node.text_type, node.url))
                        new_nodes.append(TextNode(alt, node_type, url))
                    else:
                        new_nodes.append(TextNode(alt, node_type, url))
                else:
                    if match["start"] > cur_loc:
                        new_nodes.append(TextNode(node.text[cur_loc:match["start"]],node.text_type, node.url))
                        new_nodes.append(TextNode(match["groups"][0], node_type, None))
                    else:
                        new_nodes.append(TextNode(match["groups"][0], node_type, None))
                
                cur_loc = match["end"]

            if cur_loc != len(node.text):
                new_nodes.append(TextNode(node.text[cur_loc:],node.text_type, node.url))

    return new_nodes


                    
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_by_pattern(old_nodes, r"!\[(.*?)\]\((.*?)\)", TextType.IMAGE)

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_by_pattern(old_nodes, r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", TextType.LINK)

def split_nodes_bold(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_by_pattern(old_nodes, r"\*\*(.*?)\*\*", TextType.BOLD)

def split_nodes_italics(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_by_pattern(old_nodes, r"\_(.*?)\_", TextType.ITALIC)

def split_nodes_code(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_by_pattern(old_nodes, r"\`(.*?)\`", TextType.CODE)

def split_nodes_decorator(func):
    def wrapper(old_nodes: list[TextNode]):
        print(f"function_name:")
        print(func.__name__)
        return func(old_nodes)
    return wrapper

def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = nodes.copy()
    map = {
        TextType.IMAGE: split_nodes_image,
        TextType.LINK: split_nodes_link,
        TextType.BOLD: split_nodes_bold,
        TextType.ITALIC: split_nodes_italics,
        TextType.CODE: split_nodes_code,
    }
    for k, v in map.items():
        type: TextType = k
        func = v
        # new_nodes = split_nodes_decorator(v)(new_nodes)
        new_nodes = func(new_nodes)
        # print(f"type: {type}")
        # print("new_nodes:", new_nodes)

    return new_nodes




    


if __name__ == "__main__":
    text: str = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    # res: list[TextNode] = split_nodes_bold([TextNode(text, TextType.TEXT)])
    """node = TextNode(' with an _italic_ word and a `code block` and an ', TextType.TEXT, None)
    res = split_nodes_italics([node])
    res = split_nodes_code(res)
    print(res)"""
    '''
    [TextNode(' with an ', <TextType.TEXT: 'text'>, None), 
    TextNode('italic', <TextType.ITALIC: 'italic'>, None), 
    TextNode(' word and a ', <TextType.TEXT: 'text'>, None), 
    TextNode('code block', <TextType.CODE: 'code'>, None), 
    TextNode(' and an ', <TextType.TEXT: 'text'>, None)]
    '''
    res: list[TextNode] = text_to_textnodes(text)
    print(res)
    '''
    [
    TextNode('This is ', <TextType.TEXT: 'text'>, None), 
    TextNode('text', <TextType.BOLD: 'bold'>, None), 
    TextNode(' with an ', <TextType.TEXT: 'text'>, None), 
    TextNode('italic', <TextType.ITALIC: 'italic'>, None), 
    TextNode(' word and a ', <TextType.TEXT: 'text'>, None), 
    TextNode('code block', <TextType.CODE: 'code'>, None), 
    TextNode(' and an ', <TextType.TEXT: 'text'>, None), 
    TextNode('obi wan image', <TextType.IMAGE: 'image'>, 'https://i.imgur.com/fJRm4Vk.jpeg'), 
    TextNode(' and a ', <TextType.TEXT: 'text'>, None), 
    TextNode('link', <TextType.LINK: 'link'>, 'https://boot.dev')
    ]
    '''