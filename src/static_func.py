import os
import shutil

def copy_static() -> list[str]:

    root = os.curdir
    source = os.path.join(root, 'static')
    destination = os.path.join(root, 'public')

    if os.path.exists(destination):
        try:
            shutil.rmtree(destination)
        except Exception as e:
            print(f"Error with removing destination directory: {e}")
        try:
            os.mkdir(destination)
        except Exception as e:
            print(f"Error with creating destination directory: {e}")

    copy_list = recursive_content_copy(source, destination)

    print("Files coppied:\n")
    for copy in copy_list:
        print(copy)

def recursive_content_copy(source: str, destination: str) -> list[str]:

    dir_content_list = os.listdir(source)
    copy_list = []
    for dir_content in dir_content_list:
        current_source = os.path.join(source, dir_content)
        current_destination = os.path.join(destination, dir_content)
        if os.path.isfile(current_source):
            copy_path = shutil.copy(current_source, current_destination)
            copy_list.append(copy_path)
        elif os.path.isdir(current_source):
            if not os.path.exists(current_destination):
                os.mkdir(current_destination)
            new_copy_list = recursive_content_copy(current_source, current_destination)
            copy_list.extend(new_copy_list)
    return copy_list