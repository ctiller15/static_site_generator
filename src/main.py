import os
import shutil

from utils import extract_title, markdown_to_html_node

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    if os.path.exists(dir_path_content):
        if os.path.isfile(dir_path_content):
            if dir_path_content.endswith(".md"):
                generate_page(dir_path_content, template_path, dest_dir_path)
            # check if markdown, and then generate page.
        else:
            # Create the folder in the dest path if it does not exist.
            if not os.path.exists(dest_dir_path):
                os.mkdir(dest_dir_path)
            # find all items in there.
            folder_content = os.listdir(dir_path_content)
            for item in folder_content:
                new_content_dir_path = os.path.join(*[dir_path_content, item])
                new_dest_dir_path = os.path.join(*[dest_dir_path, item]).replace(".md", ".html")
                generate_pages_recursive(new_content_dir_path, template_path, new_dest_dir_path)

def generate_page(from_path, template_path, dest_path):
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    f_template_doc = open(template_path, "r", encoding="utf-8")
    template_doc = f_template_doc.read()
    f_template_doc.close()
    if os.path.exists(from_path):
        with open(from_path, 'r') as f:
            data = f.read()
            md_html = markdown_to_html_node(data)
            html_content = md_html.to_html()
            md_title = extract_title(data)

            full_html_doc = template_doc.replace("{{ Title }}", md_title).replace("{{ Content }}", html_content)
            # write doc to dest path.
            
            with open(dest_path, 'w') as g:
                g.write(full_html_doc)


def copy_directory(dir_name, target_dir_name):
    if not os.path.exists(target_dir_name):
        os.mkdir(target_dir_name)

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
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_directory("static", "public")
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()