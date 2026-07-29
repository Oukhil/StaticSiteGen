import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_default_tag(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)

    def test_default_value(self):
        node = HTMLNode()
        self.assertIsNone(node.value)

    def test_default_children(self):
        node = HTMLNode()
        self.assertIsNone(node.children)

    def test_default_props(self):
        node = HTMLNode()
        self.assertIsNone(node.props)

    def test_to_html_props(self):
        node = HTMLNode(
            "tag",
            "value",
            None,
            {"key1": "value1", "key2": "value2"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' key1="value1" key2="value2"',
        )

    def test_repr(self):
        node = HTMLNode(
            "tag",
            "value",
            [],
            {"key": "value"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(tag, value, [], {'key': 'value'})",
        )

if __name__ == "__main__":
    unittest.main()