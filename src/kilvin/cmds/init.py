CONFIG = """title = ''
author = ''
default-template = ''
"""

ARCHE = """---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
---
"""

CONFIG_FILE = "config.toml"


def gen_file(file_path, data):
    with open(file_path, "w") as f:
        f.write(data)


def init(path):
    dirs = ["archetypes", "public", "content", "static", "layouts"]

    abs_path = path.absolute()

    try:
        abs_path.mkdir()
        for dir in dirs:
            dir_path = abs_path / dir
            dir_path.mkdir()

        gen_file(abs_path / CONFIG_FILE, CONFIG)
        gen_file(abs_path / "layouts" / "default.md", ARCHE)

        print(f"{path} directory for the project created.")
    except FileExistsError:
        print("Directory already exists.")
