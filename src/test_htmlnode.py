import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
