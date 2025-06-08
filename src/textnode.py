from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({repr(self.text)}, {repr(self.text_type)}, {repr(self.url)})"
    
    def to_html_string(self, pretty=False):
        match self.text_type:
            case TextType.TEXT:
                return self.text
            case TextType.BOLD:
                return f"<b>{self.text}</b>"
            case TextType.ITALIC:
                return f"<i>{self.text}</i>"
            case TextType.CODE:
                return f"<code>{self.text}</code>"
            case TextType.LINK:
                return f"<a href=\"{self.url}\">{self.text}</a>"
            case TextType.IMAGE:
                return f"<img src=\"{self.url}\" alt=\"{self.text}\">"
            case _:
                raise Exception("Invalid text type")

            