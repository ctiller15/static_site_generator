import os
import shutil
from textnode import TextNode, TextType


def copy_directory(dir_name, target_dir_name):
    if os.path.exists(dir_name):
        dir_items = os.listdir(dir_name)
        for item in dir_items:
            source_path = os.path.join(*[dir_name, item])
            target_path = os.path.join(*[target_dir_name, item])
            if os.path.exists(source_path):
                if os.path.isfile(source_path):
                    # add file from source to target dir.
                    shutil.copy(source_path, target_path)
                else:
                    if os.path.exists(target_path):
                        shutil.rmtree(target_path)

                    os.mkdir(target_path)
                    # recurse with the new dir name.
                    copy_directory(source_path, target_path)
        

def main():
    copy_directory("static", "public")

if __name__ == "__main__":
    main()