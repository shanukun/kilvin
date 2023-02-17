import datetime
import os
import pathlib
import sys
from string import Template

FM = Template(
    """---
template:
title:
date: $today
draft: True
---
"""
)


def check_kilvin_dir():
    cwd = pathlib.Path(".")
    config_path = cwd / "config.toml"
    if not config_path.exists():
        print("Error: Unable to locate config file.")
        sys.exit()


def create_new_file(path):
    check_kilvin_dir()
    head, tail = os.path.split(path)
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")

    content_path = pathlib.Path("content")

    try:
        head_path = content_path / pathlib.Path(head)
        head_path.mkdir()
    except FileExistsError:
        pass

    file_path = content_path / head / tail
    if file_path.exists():
        print("File already exists.")
    else:
        with open(file_path, "w") as f:
            f.write(FM.substitute(today=today))
    print(f"Create {file_path}.")
