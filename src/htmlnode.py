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
        if not self.props:
            return ""
        return " " + " ".join([f'{key}="{value}"' for key, value in self.props.items()])
    
    def __repr__(self) -> str:
        if not self.tag:
            return self.value
        
        if self.children:
            return f"<{self.tag}{self.props_to_html()}>" + "\n  " + "\n  ".join([str(child.__repr__()) for child in self.children]) + "\n" +  f"</{self.tag}>"
        else:
            return f"<{self.tag}{self.props_to_html()}> {self.value} </{self.tag}>"
        

class LeafNode(HtmlNode):
    def __init__(self, tag: str | None, value: str, props: dict = None):
        super().__init__(tag, value, None, props)
        if self.value is None:
            raise ValueError("cannot instantiate leaf node without value")
        
    def to_html(self):
        if not self.tag:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        

    
class ParentNode(HtmlNode):
    def __init__(self, tag: str | None, children: list, props: dict = None):
        super().__init__(tag=tag, children=children, props=props)
        if not self.children:
            raise ValueError("cannot instantiate parent node without children")
        if not self.tag:
            raise ValueError("cannot instantiate parent node without tag")
        
    def to_html(self, pretty=False):
        if not self.tag:
            return self.value
        else:
            if pretty:
                return f"<{self.tag}{self.props_to_html()}>" + "\n  " + "\n  ".join([str(child.to_html()) for child in self.children]) + "\n" +  f"</{self.tag}>"
            else:
                return f"<{self.tag}{self.props_to_html()}>" + "".join([str(child.to_html()) for child in self.children]) +  f"</{self.tag}>" 



if __name__ == "__main__":
    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )

    print(node.to_html())
    

    


