import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode, HTMLNode
from utils import block_to_block_type, extract_markdown_images, extract_markdown_links, extract_title, markdown_to_blocks, markdown_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_splits_old_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_splits_multiple(self):
        node = TextNode("This is text with a **bold** word and a second **bold phrase!**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word and a second ", TextType.TEXT),
            TextNode("bold phrase!", TextType.BOLD)
        ]

        self.assertEqual(new_nodes, expected)
    
    def test_multiple_nodes(self):
        node1 = TextNode("This is a **bold** word", TextType.TEXT)
        node2 = TextNode("This is an *italic* word and a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        expected = [
            TextNode("This is a ", TextType.TEXT, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" word", TextType.TEXT, None),
            TextNode("This is an *italic* word and a ", TextType.TEXT, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" word", TextType.TEXT, None)
        ]

        self.assertEqual(new_nodes, expected)

    def test_splits_start(self):
        node = TextNode("*This is italic text*, and this is text I would like to *emphasize*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

        expected = [
            TextNode("This is italic text", TextType.ITALIC),
            TextNode(", and this is text I would like to ", TextType.TEXT),
            TextNode("emphasize", TextType.ITALIC)
        ]

        self.assertEqual(new_nodes, expected)

    def test_empty_case(self):
        new_nodes = split_nodes_delimiter([], "`", TextType.CODE)

        self.assertEqual(new_nodes, [])

    def test_one_empty(self):
        node1 = TextNode("This is a word", TextType.TEXT)
        node2 = TextNode("This is an *italic* word", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node1, node2], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is a word", TextType.TEXT, None),
            TextNode("This is an ", TextType.TEXT, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" word", TextType.TEXT, None)])

    def test_error_if_matching_delimiter_not_found(self):
        node = TextNode("I don't know how to handle *this sort of text.", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

class TestMarkDownImageExtractor(unittest.TestCase):
    def test_image_extraction(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)

        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(result, expected)

    def test_link_extraction(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)

        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(result, expected)

class TestSplitNodesLink(unittest.TestCase):
    def test_node_link_split(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]

        self.assertEqual(new_nodes, expected)

    def test_no_links(self):
        node = TextNode("This has no links", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        expected = [node]

        self.assertEqual(new_nodes, expected)

    def test_text_after(self):
        node = TextNode("Here's a [link](url) and some text after", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        
        expected = [
            TextNode("Here's a ", TextType.TEXT, None),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" and some text after", TextType.TEXT, None)
        ]
        self.assertEqual(new_nodes, expected)

class TestSplitNodesImage(unittest.TestCase):
    def test_node_split_image(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]

        self.assertEqual(new_nodes, expected)

    def test_no_images(self):
        node = TextNode("This is text without an image", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        expected = [
            node
        ]

        self.assertEqual(new_nodes, expected)

    def test_text_after(self):
        node = TextNode("Here's a ![image](url) and some text after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        
        expected = [
            TextNode("Here's a ", TextType.TEXT, None),
            TextNode("image", TextType.IMAGE, "url"),
            TextNode(" and some text after", TextType.TEXT, None)
        ]
        self.assertEqual(new_nodes, expected)

class TestFullTextToTextNodes(unittest.TestCase):
    def test_full_text(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        result = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(result, expected)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_main(self):
        text = """# This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is the first list item in a list block
            * This is a list item
            * This is another list item"""
        
        result = markdown_to_blocks(text)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
            * This is a list item
            * This is another list item"""
        ]

        self.assertEqual(result, expected)

    def test_markdown_to_blocks_filters_whitespace(self):
        text = """# This is a heading

        


            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is the first list item in a list block
            * This is a list item
            * This is another list item"""
        
        result = markdown_to_blocks(text)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
            * This is a list item
            * This is another list item"""
        ]

        self.assertEqual(result, expected) 

    def test_markdown_to_blocks_empty(self):
        text = """"""
        
        result = markdown_to_blocks(text)
        expected = []

        self.assertEqual(result, expected)

    def test_markdown_to_blocks_no_changes(self):
        text = "# Just a heading"

        result = markdown_to_blocks(text)
        expected = ["# Just a heading"]

        self.assertEqual(result, expected)

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        blocks = [
            ("# h1", "h1"), 
            ("## h2", "h2"),
            ("### h3", "h3"),
            ("#### h4", "h4"),
            ("##### h4", "h5"), 
            ("###### h6", "h6"),
        ]

        for block in blocks:
            with self.subTest(params=block):
                self.assertEqual(block_to_block_type(block[0]), block[1])

    def test_heading_fails_without_space(self):
        block = "###h3"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_code_block(self):
        block = "```code goes here```"

        self.assertEqual(block_to_block_type(block), "code")
    
    def test_code_block_failure(self):
        block = "`code_goes_here`"

        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_quote_block(self):
        block = """> This is a quote.
> This is the second line of a quote.
> This is the third line of a quote block."""

        self.assertEqual(block_to_block_type(block), "quote")

    def test_quote_block_no_spaces(self):
        block = """> This is a quote.
>This is the second line of a quote.
>This is the third line of a quote block."""

        self.assertEqual(block_to_block_type(block), "quote")

    def test_incorrect_quote_block(self):
        block = """> This is a quote.
> This is the second line of a quote.
* insert secret wrong line!
> This is the third line of a quote block."""

        self.assertEqual(block_to_block_type(block), "paragraph")     

    def test_unordered_list_block(self):
        block = """* list item 1
- list item with minus sign
- another minus sign
* another star!!!
- aaaaaand another minus sign"""
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_unordered_list_block_no_spaces(self):
        block = """* list item 1
-list item with minus sign
-another minus sign
* another star!!!
- aaaaaand another minus sign"""
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_unordered_list_block_no_spaces(self):
        block = """* list item 1
- list item with minus sign
> another minus sign
* another star!!!
- aaaaaand another minus sign"""
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_ordered_list_block(self):
        block = """1. item 1
2. item 2
3. item 3
4. item 4
5. item 5"""
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_ordered_list_block_does_not_start_correctly(self):
        block = """9. item 1
2. item 2
3. item 3
4. item 4
5. item 5"""
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_ordered_list_block_no_spaces(self):
        block = """1. item 1
2.item 2
3. item 3
4. item 4
5. item 5"""
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_paragraph_block(self):
        block = "fh3287h1238"
        self.assertEqual(block_to_block_type(block), "paragraph")

class TestMarkdownToHtmlNode(unittest.TestCase):
    # TODO: Test nested values under ol/li
    def test_converts_to_html_happy_path(self):
        markdown_doc = """
# Header

paragraph text

- list item 1
- list item 2

[link to boot.dev](https://www.boot.dev)

![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)

*italics text*

**bold text**
"""

        result = markdown_to_html_node(markdown_doc)
        expected = ParentNode(tag="div", children=[
            LeafNode(tag="h1", value="Header", props=None), 
            ParentNode(tag="p", children=[LeafNode(tag=None, value="paragraph text", props=None)]), 
            ParentNode(tag="ul", children=[
                ParentNode(tag="li", children=[LeafNode(tag=None, value="list item 1", props=None)]), 
                ParentNode(tag="li", children=[LeafNode(tag=None, value="list item 2", props=None)]),
            ]),
            ParentNode(tag="p", children=[LeafNode(tag="a", value="link to boot.dev", props={"href": "https://www.boot.dev"})], props=None), 
            ParentNode(tag="p", children=[LeafNode(tag="img", value="", props=({"href": "https://i.imgur.com/fJRm4Vk.jpeg", "alt": "obi wan image"}))], props=None), 
            ParentNode(tag="p", children=[LeafNode(tag="i", value="italics text")], props=None), 
            ParentNode(tag="p", children=[LeafNode(tag="b", value="bold text")], props=None)
        ])

        self.assertEqual(expected, result)

    def test_handles_more_elements(self):
        markdown_doc = """
        # Header

## Header Two

### Header Three

#### Header Four

##### Header Five

###### Header Six

paragraph text

1. list item 1
2. list item 2
3. list item 3
4. list item 4
5. list item 5

```print("Hello World!")```

> This is some quote text.
> It keeps going.
> Until I stop with the less than symbols.

This is a paragraph with a mix of *italics* and **bold** text!
"""

        result = markdown_to_html_node(markdown_doc)
        expected = ParentNode(tag="div", children=[
            LeafNode(tag="h1", value="Header", props=None), 
            LeafNode(tag="h2", value="Header Two", props=None), 
            LeafNode(tag="h3", value="Header Three", props=None), 
            LeafNode(tag="h4", value="Header Four", props=None), 
            LeafNode(tag="h5", value="Header Five", props=None), 
            LeafNode(tag="h6", value="Header Six", props=None),
            ParentNode(tag="p", children=[
                LeafNode(tag=None, value="paragraph text", props=None)
            ], props=None),
            ParentNode(tag="ol", children=[
                ParentNode(tag="li", children=[
                    LeafNode(tag=None, value="list item 1")
                ]),
                ParentNode(tag="li", children=[
                    LeafNode(tag=None, value="list item 2")
                ]),
                ParentNode(tag="li", children=[
                    LeafNode(tag=None, value="list item 3")
                ]),
                ParentNode(tag="li", children=[
                    LeafNode(tag=None, value="list item 4")
                ]),
                ParentNode(tag="li", children=[
                    LeafNode(tag=None, value="list item 5")
                ]),
            ], props=None),
            ParentNode(tag="pre", children=[
                LeafNode(tag="code", value="print(\"Hello World!\")", props=None)
            ]),
            LeafNode(tag="blockquote", value="This is some quote text.\nIt keeps going.\nUntil I stop with the less than symbols.", props=None),
            ParentNode(tag="p", children=[
                LeafNode(tag=None, value="This is a paragraph with a mix of ", props=None),
                LeafNode(tag="i", value="italics", props=None),
                LeafNode(tag=None, value=" and ", props=None),
                LeafNode(tag="b", value="bold", props=None),
                LeafNode(tag=None, value=" text!", props=None)
            ], props=None)
        ], props=None)

        self.assertEqual(result, expected)

class TestExtractTitle(unittest.TestCase):
    def test_extracts_a_h1_tag(self):
        result = extract_title("# Hello")
        
        self.assertEqual(result, "Hello")

    def test_errors_if_no_header(self):
        with self.assertRaises(Exception) as context:
            result = extract_title("hello")

        self.assertEqual(str(context.exception), "markdown does not contain a h1 block")

        