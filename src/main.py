import os
import shutil

from copy_static import copy_files_recursive
from page_generator import generate_page

DIR_PATH_STATIC = "./static"
DIR_PATH_PUBLIC = "./public"
DIR_PATH_CONTENT = "./content"
PATH_TEMPLATE = "./template.html"


def main():
    # Delete anything in the public directory
    if os.path.exists(DIR_PATH_PUBLIC):
        print("\nDeleting public directory...")
        shutil.rmtree(DIR_PATH_PUBLIC)

    # Copy static files from static to public
    print("Copying static files to public directory...")
    copy_files_recursive(DIR_PATH_STATIC, DIR_PATH_PUBLIC)

    # Generate a page from content/index.md using template.html and write it to public/index.html
    print("Generating page...")
    generate_page(
        os.path.join(DIR_PATH_CONTENT, "index.md"),
        PATH_TEMPLATE,
        os.path.join(DIR_PATH_PUBLIC, "index.html"),
    )


main()
