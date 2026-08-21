import unittest

from textnode import TextNode, TextType
from node_func import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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



if __name__ == "__main__":
    unittest.main()