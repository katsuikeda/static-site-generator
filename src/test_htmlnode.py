import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_to_props(self):
        node = HTMLNode(
            "a",
            "Go to boot.dev",
            None,
            {"class": "link", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="link" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "This is a div",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "This is a div",
        )
        self.assertIsNone(
            node.children,
        )
        self.assertIsNone(
            node.props,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "This is a paragraph",
            None,
            {"class": "px-4"},
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(p, This is a paragraph, children: None, {'class': 'px-4'})",
        )

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_grandchildren(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "div",
                    [
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                    ],
                ),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b><div>Normal text<i>italic text</i></div>Normal text</p>",
        )


if __name__ == "__main__":
    unittest.main()
