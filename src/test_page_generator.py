import unittest

from page_generator import (
    extract_title,
)


class TestExtractTitle(unittest.TestCase):
    def test_basic_title(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_title_with_extra_spaces(self):
        markdown = "#      Hello    World        "
        self.assertEqual(extract_title(markdown), "Hello    World")

    def test_no_title(self):
        with self.assertRaises(ValueError):
            markdown = "Just plain text\nMore text"
            extract_title(markdown)

    def test_no_space(self):
        with self.assertRaises(ValueError):
            markdown = "#Header without space"
            extract_title(markdown)

    def test_wrong_header_level(self):
        with self.assertRaises(ValueError):
            markdown = "## Second level header"
            extract_title(markdown)


if __name__ == "__main __":
    unittest.main()
