from textnode import TextNode


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        delimit_count = node.text.count(delimiter)
        
        if delimit_count == 0 or delimit_count % 2 == 1:
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
