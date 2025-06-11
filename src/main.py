import os
import sys
from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from file_utilities import copy_folder_structure
from generate_content import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main(base_path: str = "/"):
    # replace public folder with contents of static folder
    copy_folder_structure(dir_path_static, dir_path_public)
    
    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, base_path)

if __name__ == "__main__":
    system_args: list[str] = sys.argv
    base_path: str = "/"
    if len(system_args) > 1:
        base_path = system_args[1]

    print(main(base_path))