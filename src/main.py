from static_func import copy_static
from page_gen import generate_page

def main():

    copy_static()
    generate_page("content/index.md", "template.html", "public/index.html")

main()