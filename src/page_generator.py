import os

from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Check if required files exist
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"Markdown file not found: {from_path}")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")

    # Read the markdown file
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    # Read the template file
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Convert the markdown file to an HTML string
    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()

    # Grab the title of the page
    title = extract_title(markdown)

    # Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title that's generated
    html_content = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_string
    )

    # Create any necessary directories if they don't exist
    dirname = os.path.dirname(dest_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")
