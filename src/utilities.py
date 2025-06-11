from htmlnode import HtmlNode, ParentNode, LeafNode
from textnode import TextNode, TextType, BlockType
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
        # print(f"function_name:")
        # print(func.__name__)
        return func(old_nodes)
    return wrapper

def text_to_textnodes(text: str) -> list[TextNode]:
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
        new_nodes = v(new_nodes)
        # func = v
        # new_nodes = split_nodes_decorator(v)(new_nodes)
        # print(f"type: {type}")
        # print("new_nodes:", new_nodes)

    return new_nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    uncleaned_blocks: list[str] = markdown.split("\n\n")
    blocks = []
    for block in uncleaned_blocks:
        cleaned_block = clean_block(block)
        if cleaned_block:
            blocks.append(cleaned_block)

    return blocks

    
def clean_block(block: str) -> str:
    # print("block:", block)
    stripped_block = block.strip()
    while stripped_block and stripped_block[0] in ["\n", " "]:
        stripped_block = stripped_block[1:]

    while stripped_block and stripped_block[-1] in ["\n", " "]:
        stripped_block = stripped_block[:-1]

    return stripped_block

def block_to_block_type(block: str):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
        
        

    


        

    


if __name__ == "__main__":
    text: str = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""

    print(markdown_to_blocks(text))