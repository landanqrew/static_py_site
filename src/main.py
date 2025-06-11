import os
from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from file_utilities import copy_folder_structure
from generate_content import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    # replace public folder with contents of static folder
    copy_folder_structure("static", "public")
    
    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

if __name__ == "__main__":
    print(main())