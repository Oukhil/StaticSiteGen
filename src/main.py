import os
import shutil
import sys

from static_func import copy_static
from page_gen import generate_pages_recursive

source_dir = "./docs"

def main() -> None:

    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[0]

    if os.path.exists(source_dir):
        try:
            shutil.rmtree(source_dir)
        except Exception as e:
            print(f"Error with removing destination directory: {e}")
    try:
        os.mkdir(source_dir)
    except Exception as e:
        print(f"Error with creating destination directory: {e}")

    copy_static("./static", source_dir)
    generate_pages_recursive("./content", "./template.html", source_dir, basepath)

main()