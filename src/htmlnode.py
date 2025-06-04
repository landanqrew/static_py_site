from enum import Enum

class HtmlNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    # override in children
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        return " ".join([f'{key}="{value}"' for key, value in self.props.items()])
    
    def __repr__(self) -> str:
        if not self.tag:
            return self.value
        
        if self.children:
            return f"<{self.tag} {self.props_to_html()}>" + "\n  " + "\n  ".join([str(child.__repr__()) for child in self.children]) + "\n" +  f"</{self.tag}>"
        else:
            return f"<{self.tag} {self.props_to_html()}> {self.value} </{self.tag}>"

    


