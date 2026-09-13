import os

from markdown_blocks import markdown_to_html_node, extract_title

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_file = open(from_path)
    read_md = md_file.read()
    template_file = open(template_path)
    read_template = template_file.read()
    md_node = markdown_to_html_node(read_md)
    html_str = md_node.to_html()
    html_title = extract_title(read_md)
    end_html = read_template.replace("{{ Title }}", html_title).replace("{{ Content }}", html_str)
    dir_name = os.path.dirname(dest_path)
    if not os.path.exists(dir_name):        
        os.makedirs(dir_name)
    with open(dest_path, "w") as hmtl_file:
        hmtl_file.write(end_html)
    md_file.close()
    template_file.close()

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str) -> None:
    dir_path_list = os.listdir(dir_path_content)
    template_file = open(template_path)
    read_template = template_file.read()
    template_file.close()
    for dir_path in dir_path_list:
        current_path = os.path.join(dir_path_content, dir_path)
        dest_dir_name = os.path.join(dest_dir_path, dir_path)
        if os.path.isfile(current_path):
            if file_type(current_path) == "md":
                md_file = open(current_path)
                read_md = md_file.read()
                md_file.close()
                md_node = markdown_to_html_node(read_md)
                html_str = md_node.to_html()
                html_title = extract_title(read_md)
                replaced_template = (
                    read_template.replace("{{ Title }}", html_title).replace("{{ Content }}", html_str)
                )
                end_html = (
                    replaced_template.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
                )
                html_file_name = dest_dir_name.replace(".md", ".html")
                with open(html_file_name, "w") as hmtl_file:
                    hmtl_file.write(end_html)
        else:
            os.mkdir(dest_dir_name)
            generate_pages_recursive(current_path, template_path, dest_dir_name, basepath)


def file_type(file_name: str) -> str:
    file_parts = file_name.split('.')
    return file_parts[len(file_parts) - 1]