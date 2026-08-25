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

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    split_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            split_list.append(old_node)
            continue
        text = old_node.text
        if text == "":
            raise ValueError("Node has no text")
        images = extract_markdown_images(text)
        if len(images) == 0:
            split_list.append(old_node)
            continue
        for image in images:
            split_text = text.split(f"![{image[0]}]({image[1]})", 1)
            if split_text[0] != "":
                split_list.append(TextNode(split_text[0], TextType.TEXT))
            split_list.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = split_text[1]
        if text != "":
            split_list.append(TextNode(text, TextType.TEXT))
    return split_list

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    split_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            split_list.append(old_node)
            continue
        text = old_node.text
        if text == "":
            raise ValueError("Node has no text")
        links = extract_markdown_links(text)
        if len(links) == 0:
            split_list.append(old_node)
            continue
        for link in links:
            split_text = text.split(f"[{link[0]}]({link[1]})", 1)
            if split_text[0] != "":
                split_list.append(TextNode(split_text[0], TextType.TEXT))
            split_list.append(TextNode(link[0], TextType.LINK, link[1]))
            text = split_text[1]
        if text != "":
            split_list.append(TextNode(text, TextType.TEXT))
    return split_list

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes