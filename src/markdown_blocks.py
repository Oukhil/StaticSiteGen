from enum import Enum


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