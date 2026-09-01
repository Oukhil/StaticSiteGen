import unittest

from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_more_whitespaces(self):
        md = """
This is **bolded** paragraph      

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line   

- This is a list
- with items    
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_more_newlines(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_haeadings_with_one_hashtag(self):
        block_type = block_to_block_type("# This is a heading\nBla-bla a heading am I\nCan you tell what I am?")
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_haeadings_with_six_hashatags(self):
        block_type = block_to_block_type("###### This is a heading\nBla-bla a heading am I\nCan you tell what I am?")
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_haeadings_hashtag_no_space(self):
        block_type = block_to_block_type("#This is a heading\nBla-bla a heading am I\nCan you tell what I am?")
        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_haeadings_with_seven_hashtags(self):
        block_type = block_to_block_type("####### This is a heading\nBla-bla a heading am I\nCan you tell what I am?")
        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block_type = block_to_block_type("```\nThis is a code\nBla-bla a code am I\nCan you tell what I am?\n```")
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block_type = block_to_block_type(">This is a quote\n> Bla-bla a quote am I\n>Can you tell what I am?")
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block_type = block_to_block_type("- This is an unordered list\n- Bla-bla an unordered list am I\n- Can you tell what I am?")
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block_type = block_to_block_type("1. This is an ordered list\n2. Bla-bla an ordered list am I\n3. Can you tell what I am?")
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        block_type = block_to_block_type("This is a paragraph\nBla-bla a paragraph am I\nCan you tell what I am?")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )



if __name__ == "__main__":
    unittest.main()