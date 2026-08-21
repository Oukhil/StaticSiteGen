import re

from textnode import TextNode, TextType

def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
    ) -> list[TextNode]:

    valid_delimiters = {
        '**':TextType.BOLD,
        '_':TextType.ITALIC,
        '`':TextType.CODE,
        }
    if delimiter not in valid_delimiters:
        raise Exception("Given delimiter is not of a valid type")
    
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
        else:
            if (node.text.count(delimiter) % 2) != 0:
                raise Exception("No closing delimiter")
            cut_node = node.text.split(delimiter)
            for i in range(len(cut_node)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(cut_node[i], node.text_type))
                else:
                    new_nodes.append(TextNode(cut_node[i], valid_delimiters[delimiter]))

    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches