import os

from markdown_blocks import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
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

