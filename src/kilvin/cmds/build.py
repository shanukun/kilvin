import pathlib
import os

def build_proj():
    for root, dirs, files in os.walk("./content"):
        root_path_parts = list(pathlib.PurePath(root).parts)
        del root_path_parts[0]
        public_path = pathlib.Path("./public") / '/'.join(root_path_parts)
        for dir in dirs:
            print(f"::{dir}")
            dir_path = public_path / dir
            dir_path.mkdir()
    print("Building finished.")








