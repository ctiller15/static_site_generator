from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        delimit_count = node.text.count(delimiter)

        if delimit_count % 2 == 1:
            raise Exception("invalid markdown syntax")
        
        split_nodes = node.text.split(delimiter)
        for i in range(len(split_nodes)):
            if split_nodes[i].strip() != "":
                if i % 2 == 1:
                    # Only the odd items will be the correct nodes.
                    new_node = TextNode(split_nodes[i], text_type)
                    new_nodes.append(new_node)
                else:
                    new_node = TextNode(split_nodes[i], node.text_type)
                    new_nodes.append(new_node)

    return new_nodes

def extract_markdown_images(text):
    image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(image_regex, text)
    return matches

def extract_markdown_links(text):
    link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(link_regex, text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]):
    nodes_list = []

    for node in old_nodes:
        result = extract_markdown_images(node.text)
        result_delimiters = [f"![{x[0]}]({x[1]})" for x in result]
        text_to_split = node.text
        if len(result_delimiters) == 0:
            nodes_list.append(node)
        else:
            for delim in result_delimiters:
                sections = text_to_split.split(delim, 1)
                if sections[0] != "":
                    nodes_list.append(TextNode(sections[0], TextType.TEXT))
                image_data = extract_markdown_images(delim)
                nodes_list.append(TextNode(image_data[0][0], TextType.IMAGE, image_data[0][1]))
                text_to_split = sections[1]

            if len(text_to_split) > 0:
                nodes_list.append(TextNode(text_to_split, TextType.TEXT))

    return nodes_list

def split_nodes_link(old_nodes: list[TextNode]):
    nodes_list = []

    for node in old_nodes:
        result = extract_markdown_links(node.text)
        result_delimiters = [f"[{x[0]}]({x[1]})" for x in result]
        text_to_split = node.text
        if len(result_delimiters) == 0:
            nodes_list.append(node)
        else:
            for delim in result_delimiters:
                sections = text_to_split.split(delim, 1)
                if sections[0] != "":
                    nodes_list.append(TextNode(sections[0], TextType.TEXT))
                link_data = extract_markdown_links(delim)
                nodes_list.append(TextNode(link_data[0][0], TextType.LINK, link_data[0][1]))
                text_to_split = sections[1]

            if len(text_to_split) > 0:
                nodes_list.append(TextNode(text_to_split, TextType.TEXT))

    return nodes_list

def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def markdown_to_blocks(markdown):
    split_markdown = list(filter( lambda x: len(x.strip()) > 0 ,map(str.strip, markdown.split("\n\n"))))
    return split_markdown
    
def block_to_block_type(text_block: str):
    if text_block.startswith("#"):
        # it is a heading.
        split_heading = text_block.split(" ")
        heading_hashes = split_heading[0]

        # Assert that everything on the left side is an octothorpe
        if heading_hashes != len(heading_hashes) * "#":
            return "paragraph"
        
        # assume that it is correctly formatted.
        return f"h{min(len(split_heading[0]), 6)}"
    elif text_block.startswith("```"):
        if text_block.endswith("```"):
            return "code"
    elif text_block.startswith(">"):
        # test for quote block.
        lines = text_block.split("\n")
        is_quote = True
        for line in lines:
            if not line.startswith(">"):
                is_quote = False

        if is_quote:
            return "quote"
    elif text_block.startswith("*") or text_block.startswith("-"):
        lines = text_block.split("\n")
        is_ul = True
        for line in lines:
            if not line.startswith("- ") and not line.startswith("* "):
                is_ul = False

        if is_ul:
            return "unordered_list"
    elif text_block.startswith("1"):
        lines = text_block.split("\n")
        is_ol = True
        for i, line in enumerate(lines, start=1):
            if not line.startswith(f"{i}. "):
                is_ol = False
        
        if is_ol:
            return "ordered_list"
        
    # All conditions have fallen through. It is a normal paragraph.
    return "paragraph"
    
def markdown_to_html_node(markdown: str):
    child_nodes = []
    split_markdown = markdown_to_blocks(markdown)
    for block in split_markdown:
        block_type = block_to_block_type(block)
        # Can be broken out into another function
        match block_type:
            case "h1" | "h2" | "h3" | "h4" | "h5" | "h6":
                text = block.split(" ", 1)[1]
                new_node = LeafNode(block_type, text)
                child_nodes.append(new_node)
            case "paragraph":
                # need to further split p tags depending on if they contain anything.
                paragraph_text_nodes = text_to_textnodes(block)
                parent_node = ParentNode("p", paragraph_text_nodes, None)
                child_nodes.append(parent_node)
            case "unordered_list":
                lines = block.split("\n")
                list_item_nodes = list(map(lambda x: LeafNode("li", x.split(" ", 1)[1]), lines))

                parent_node = ParentNode("ul", list_item_nodes)
                child_nodes.append(parent_node)
            case "ordered_list":
                lines = block.split("\n")
                list_item_nodes = list(map(lambda x: LeafNode("li", x.split(" ", 1)[1]), lines))
                parent_node = ParentNode("ol", list_item_nodes)
                child_nodes.append(parent_node)
            case "code":
                text = block.lstrip("```").rstrip("```")
                child_node = LeafNode("code", text, None)
                parent_node = ParentNode("pre", [child_node], None)
                child_nodes.append(parent_node)
            case "quote":
                lines = block.split("\n")
                quote_tag_removed_text = "\n".join(list(map(lambda x: x[1:], lines)))
                child_node = LeafNode("blockquote", quote_tag_removed_text, None)
                child_nodes.append(child_node)

    return ParentNode(tag="div", children=child_nodes)