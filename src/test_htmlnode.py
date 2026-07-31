import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>',)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "value")
        self.assertEqual(node.to_html(), 'value')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_without_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_without_tag(self):
            child_node = LeafNode("span", "child")
            parent_node = ParentNode(None, [child_node])
            with self.assertRaises(ValueError):
                parent_node.to_html()



if __name__ == "__main__":
    unittest.main()