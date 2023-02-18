import os
import pathlib

from kilvin.mdown import markdown


def build_proj():
    for root, dirs, files in os.walk("./content"):
        root_path_parts = list(pathlib.PurePath(root).parts)
        del root_path_parts[0]
        public_path = pathlib.Path("./public") / "/".join(root_path_parts)
        for dir in dirs:
            dir_path = public_path / dir
            dir_path.mkdir()
        for file in files:
            md_file = pathlib.PurePath(root) / file
            html_file = public_path / file
            print(html_file)
            html_file = html_file.with_suffix('.html')
            out = markdown.render(md_file)
            with open(html_file, "w") as hf:
                hf.write(out)

    print("Building finished.")
