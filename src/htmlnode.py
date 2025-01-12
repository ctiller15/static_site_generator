class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        return_str = ""
        if self.props:
            for key in self.props:
                return_str += f" {key}=\"{self.props[key] if self.props[key] else ''}\""

        return return_str
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")
        
        if not self.tag:
            return f"{self.value}"
        
        if self.tag == "img":
            # image tags are self-closing.
            html_text = f"<{self.tag}{self.props_to_html()}/>"
        else:
            html_text = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html_text
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
    
    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.props == other.props

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag is required")
        
        if not self.children:
            raise ValueError("children is required")

        children_html = list(map(lambda x: x.to_html(), self.children))

        result = f"<{self.tag}{self.props_to_html()}>{''.join(children_html)}</{self.tag}>"
        return result
    
    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
    
    def __eq__(self, other):
        return self.tag == other.tag and self.props == other.props and self.children == other.children