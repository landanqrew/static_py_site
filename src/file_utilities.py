import os
import shutil

def empty_directory_recursively(dir_path: str):
    contents: list[str] = os.listdir(dir_path)
    if len(contents) == 0:
        print(f"no items identified in directory ({dir_path})")
        return
    for item in contents:
        item_path = os.path.join(dir_path, item)
        if os.path.isfile(item_path):
            print(f"removing {item_path}")
            os.remove(item_path)
        else:
            print(f"entering directory: {item_path}")
            empty_directory_recursively(item_path)
            print(f"removing directory: {item_path}")
            os.rmdir(item_path)

def copy_folder_structure(origin_path: str, destination_path: str):
    empty_directory_recursively(destination_path)
    print(f"copying folder structure from ({origin_path}) to ({destination_path}) ...")
    shutil.copytree(src=origin_path, dst=destination_path, dirs_exist_ok=True)



if __name__ == "__main__":
    dir_path: str = "public"
    empty_directory_recursively(dir_path)
    copy_folder_structure("static", "public")
