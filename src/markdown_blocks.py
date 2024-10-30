from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING.value
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE.value
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH.value
        return BlockType.QUOTE.value
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return BlockType.PARAGRAPH.value
        return BlockType.ULIST.value
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH.value
        return BlockType.ULIST.value
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH.value
            i += 1
        return BlockType.OLIST.value
    return BlockType.PARAGRAPH.value


def markdown_to_html_node(markdown):
    # Split the markdown into blocks
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    # Loop over each block
    for block in blocks:
        block_node = block_to_html_node(block)
        block_nodes.append(block_node)

    return ParentNode("div", block_nodes, None)


def block_to_html_node(block):
    # Determine the type of block
    block_type = block_to_block_type(block)
    # Based on the type of block, create a new HTMLNode with the proper data
    match block_type:
        case BlockType.QUOTE.value:
            return quote_to_html_node(block)
        case BlockType.ULIST.value:
            return ulist_to_html_node(block)
        case BlockType.OLIST.value:
            return olist_to_html_node(block)
        case BlockType.CODE.value:
            return code_to_html_node(block)
        case BlockType.HEADING.value:
            return heading_to_html_node(block)
        case (
            _
        ):  # Default case is always paragraph block due to the block_to_block_type()
            return paragraph_to_html_node(block)


def text_to_children(text: str) -> list:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


# block = "> quote\n> more quote"
def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        # Remove '>' and surrounding white space from each line
        cleaned_line = line[2:]
        cleaned_lines.append(cleaned_line)
    text = " ".join(cleaned_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


# block = "* list\n* items"
# or block = "- list\n- items"
# <ul><li>inline markdown children</li><li>inline markdown children</li></ul>
def ulist_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        # Remove '- ' or '* '
        cleaned_line = line[2:]
        children = text_to_children(cleaned_line)
        li_node = ParentNode("li", children)
        li_nodes.append(li_node)
    return ParentNode("ul", li_nodes)


def olist_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        # Remove '1. ', '2. '...
        cleaned_line = line[3:]
        children = text_to_children(cleaned_line)
        li_node = ParentNode("li", children)
        li_nodes.append(li_node)
    return ParentNode("ol", li_nodes)


def code_to_html_node(block: str) -> ParentNode:
    # Remove preceding '```\n' and following '\n```'
    lines = block.split("\n")
    text = "\n".join(lines[1:-1])
    children = text_to_children(text)
    code_node = ParentNode("code", children)
    return ParentNode("pre", [code_node])


# "### This is a heading"
def heading_to_html_node(block: str) -> ParentNode:
    # Determine the heading level
    heading_level = len(block.split(" ")[0])
    text = block[heading_level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{heading_level}", children)
