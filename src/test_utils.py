import unittest

from textnode import TextNode, TextType
from utils import split_nodes_delimiter

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

    def test_error_if_matching_delimiter_not_found(self):
        node = TextNode("I don't know how to handle *this sort of text.", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)