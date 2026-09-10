from enum import Enum

from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from node_func import text_to_textnodes


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split('\n\n')
    full_blocks = []
    for i in range(len(blocks)):
        if len(blocks[i]) == 0:
            continue
        else:
            full_blocks.append(blocks[i].strip())
    return full_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    if block.startswith(('# ', '## ', '### ', '#### ', '##### ', '###### ')):
        return BlockType.HEADING
    if block.startswith('```\n') and block[-3:] == '```':
        return BlockType.CODE
    blocksplit = block.split('\n')
    check = True
    for split in blocksplit:
        check = split.startswith('>') and check
    if check:
        return BlockType.QUOTE
    check = True
    for split in blocksplit:
        check = split.startswith('- ') and check
    if check:
        return BlockType.UNORDERED_LIST
    number = 1
    check = True
    for split in blocksplit:
        check = split.startswith(f'{number}. ') and check
        number += 1
    if check:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    node_list = []
    for block in blocks:
        node_list.append(block_to_html_node(block))
    return ParentNode("div", node_list)

def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        return block_to_heading_node(block)
    elif block_type == BlockType.CODE:
        return block_to_code_node(block)
    elif block_type == BlockType.QUOTE:
        return block_to_quote_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return block_to_unordered_list(block)
    elif block_type == BlockType.ORDERED_LIST:
        return block_to_ordered_list(block)
    elif block_type == BlockType.PARAGRAPH:
        return block_to_paragraph(block)
    raise ValueError("Block has a block type of unknown origin")
    

def text_to_children(text: str) -> list[HTMLNode]:
    text_node_list = text_to_textnodes(text)
    html_node_list = []
    for text_node in text_node_list:
        html_node_list.append(text_node_to_html_node(text_node))
    return html_node_list

def block_to_heading_node(block: str) -> ParentNode:
    heading_split = block.split(' ', 1)
    h_count = len(heading_split[0])
    text = block[h_count + 1: ]
    childen = text_to_children(text)
    return ParentNode(f"h{h_count}", childen)

def block_to_code_node(block: str) -> ParentNode:
    text = block[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    child_node = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [child_node])
    return ParentNode("pre", [code_node])

def block_to_quote_node(block: str) -> ParentNode:
    line_list = block.split('\n')
    stripped_line_list = []
    for line in line_list:
        stripped_line_list.append(line[1:].strip())
    stripped_text = " ".join(stripped_line_list)
    children = text_to_children(stripped_text)
    return ParentNode("blockquote", children)

def block_to_unordered_list(block: str) -> ParentNode:
    line_list = block.split('\n')
    children_list = []
    for line in line_list:
        child_node = text_to_children(line[2:])
        children_list.append(ParentNode("li", child_node))
    return ParentNode("ul", children_list)

def block_to_ordered_list(block: str) -> ParentNode:
    line_list = block.split('\n')
    children_list = []
    for line in line_list:
        line_parts = line.split(". ", 1)
        child_node = text_to_children(line_parts[1])
        children_list.append(ParentNode("li", child_node))
    return ParentNode("ol", children_list)

def block_to_paragraph(block: str) -> ParentNode:
    line_list = block.split('\n')
    children = text_to_children(" ".join(line_list))
    return ParentNode("p", children)

def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            split_block = block.split("# ", 1)
            if split_block[0] == "":
                return split_block[1].strip()
            continue
    raise Exception("Title extraction failed: No h1 header detected")