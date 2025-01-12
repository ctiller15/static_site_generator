import os
import shutil

from utils import extract_title, markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    if os.path.exists(from_path):
        with open(from_path, 'r') as f:
            data = f.read()
            print(data)
            md_html = markdown_to_html_node(data)
            print(md_html)
            html_content = md_html.to_html()
            md_title = extract_title(data)
            print(md_title)
            print(html_content)


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
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()