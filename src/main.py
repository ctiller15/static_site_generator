import os
from textnode import TextNode, TextType


def copy_directory(dir_name, target_dir_name):
    if os.path.exists(dir_name):
        dir_items = os.listdir(dir_name)
        for item in dir_items:
            print(os.path.join(item))
        

def main():
    copy_directory("static", "public")
    textnode = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(textnode)

if __name__ == "__main__":
    main()