import unittest

from textnode import TextNode, TextType
from node_func import (
    split_nodes_delimiter, extract_markdown_images, extract_markdown_links,
    split_nodes_image, split_nodes_link, text_to_textnodes,
    markdown_to_blocks, block_to_block_type, BlockType
)
class TestNodeFunc(unittest.TestCase):
    def test_eq_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes1 = [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
        ]
        new_nodes2 = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes1, new_nodes2)

    def test_eq_delim_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes1 = [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("bold block", TextType.BOLD),
        TextNode(" word", TextType.TEXT),
        ]
        new_nodes2 = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes1, new_nodes2)

    def test_eq_delim_italic(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes1 = [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("italic block", TextType.ITALIC),
        TextNode(" word", TextType.TEXT),
        ]
        new_nodes2 = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes1, new_nodes2)

    def test_wrong_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], ".", TextType.CODE)

    def test_wrong_no_closing_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_start_with_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_end_with_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and there is no third.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" and there is no third.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_two_nodes(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node, node1])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_without_image(self):
        node = TextNode(
            "This is text without an image.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text without an image.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_empty_list(self):
        node = TextNode(
                    "",
                    TextType.TEXT,
                )
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_image([node])

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_basic(self):
        textnodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
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
            ],
            textnodes
        )

    def test_text_to_textnodes_empty_string(self):
        with self.assertRaises(ValueError):
            textnodes = text_to_textnodes("")

    def test_text_to_textnodes_plain_text(self):
        textnodes = text_to_textnodes("Nada")
        self.assertListEqual([TextNode("Nada", TextType.TEXT),], textnodes)

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


if __name__ == "__main__":
    unittest.main()