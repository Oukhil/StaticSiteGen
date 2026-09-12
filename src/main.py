import os
import shutil

from static_func import copy_static
from page_gen import generate_pages_recursive

def main() -> None:

    if os.path.exists("./public"):
        try:
            shutil.rmtree("./public")
        except Exception as e:
            print(f"Error with removing destination directory: {e}")
        try:
            os.mkdir("./public")
        except Exception as e:
            print(f"Error with creating destination directory: {e}")

    copy_static()
    generate_pages_recursive("./content", "./template.html", "./public")

main()