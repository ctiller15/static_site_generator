import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

class TestTextNodeToHTML(unittest.TestCase):
    def test_text_node(self):
        node = TextNode("test_text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        result = html_node.to_html()
        self.assertEqual(result, "test_text")

    def test_text_bold_node(self):
        node = TextNode("test_text_bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        result = html_node.to_html()
        self.assertEqual(result, "<b>test_text_bold</b>")

    def test_text_italic_node(self):
        node = TextNode("test_text_italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        result = html_node.to_html()
        self.assertEqual(result, "<i>test_text_italic</i>")
    
    def test_text_code_node(self):
        node = TextNode("test_text_code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        result = html_node.to_html()
        self.assertEqual(result, "<code>test_text_code</code>")
        
    def test_text_link_node_no_url(self):
        node = TextNode("test_text_link_no_url", TextType.LINKS)
        html_node = text_node_to_html_node(node)
        result = html_node.to_html()
        self.assertEqual(result, "<a href=\"\">test_text_link_no_url</a>")

    def test_text_link_node_with_url(self):
        node = TextNode("test_text_link_no_url", TextType.LINKS, url="https://www.google.com")
        html_node = text_node_to_html_node(node)
        result = html_node.to_html()
        self.assertEqual(result, "<a href=\"https://www.google.com\">test_text_link_no_url</a>")
    
    def test_text_image_node_no_url(self):
        node = TextNode("test_text_image_no_url", TextType.IMAGES)
        html_node = text_node_to_html_node(node)
        result = html_node.to_html()
        self.assertEqual(result, "<img href=\"\" alt=\"test_text_image_no_url\"/>")
    
    def test_text_image_node_with_url(self):
        node = TextNode("test_text_image_no_url", TextType.IMAGES, url="https://www.google.com")
        html_node = text_node_to_html_node(node)
        result = html_node.to_html()
        self.assertEqual(result, "<img href=\"https://www.google.com\" alt=\"test_text_image_no_url\"/>")

if __name__ == "__main__":
    unittest.main()