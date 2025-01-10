import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com", 
            "target": "_blank",
        }

        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_html_node_repr(self):
        node = HTMLNode(tag="a", value="a link!", props={"href": "https://www.google.com"})
        self.assertEqual(repr(node), "HTMLNode(tag=a, value=a link!, children=None, props={'href': 'https://www.google.com'})")

    def test_to_html_throws_exception(self):
        with self.assertRaises(NotImplementedError):
            node = HTMLNode()
            node.to_html()

class TestLeafNode(unittest.TestCase):
    def test_leaf_node_requires_value_and_tag(self):
        with self.assertRaises(TypeError):
            node = LeafNode()

    def test_to_html_without_value(self):
        with self.assertRaises(ValueError) as context:
            node = LeafNode("a", "anchor")
            node.value = None

            node.to_html()

        self.assertEqual(str(context.exception), "all leaf nodes must have a value")

    def test_value_returns_as_raw_text_without_tag(self):
        node = LeafNode("a", "anchor")
        node.tag = None

        result = node.to_html()

        self.assertEqual(result, "anchor")

    def test_normal_html_tag_returns(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        result = node.to_html()
        self.assertEqual(result, "<a href=\"https://www.google.com\">Click me!</a>")

    def test_leaf_node_repr(self):
        node = LeafNode(tag="a", value="a link!", props={"href": "https://www.google.com"})
        self.assertEqual(repr(node), "LeafNode(tag=a, value=a link!, props={'href': 'https://www.google.com'})")

class TestParentNode(unittest.TestCase):
    def test_parent_node_requires_tag_children(self):
        with self.assertRaises(TypeError):
            node = ParentNode()

    def test_parent_node_proper_args(self):
        leaf_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node = ParentNode(tag="div", children=[leaf_node])

    def test_parent_node_fails_when_no_tag(self):
        leaf_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node = ParentNode(tag="div", children=[leaf_node])
        node.tag = None

        with self.assertRaises(ValueError):
            result = node.to_html()

    def test_parent_node_fails_when_no_children(self):
        leaf_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node = ParentNode(tag="div", children=[leaf_node])
        node.children = None

        with self.assertRaises(ValueError):
            result = node.to_html()

    def test_successful_to_html(self):
        leaf_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node = ParentNode(tag="div", children=[leaf_node]) 

        result = node.to_html()
        self.assertEqual(result, "<div><a href=\"https://www.google.com\">Click me!</a></div>")

    def test_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        result = node.to_html()
        self.assertEqual(result, "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parent_node_nesting(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "div",
                    [
                        ParentNode(
                            "div",
                            [LeafNode("p", "Hello nested world!"),]
                        )
                    ],
                    {
                        "width": "50px",
                        "height": "50px",
                        "display": "block"
                    }
                )
            ]
        )

        result = node.to_html()
        self.assertEqual(result, "<div><div width=\"50px\" height=\"50px\" display=\"block\"><div><p>Hello nested world!</p></div></div></div>")


if __name__ == "__main__":
    unittest.main()