import datetime
import os
import pathlib
from contextlib import suppress
from string import Template

from kilvin import utils

FM = Template(
    """---
template:
title:
date: $today
draft: True
---
"""
)


@utils.is_kilvin_dir
def create_new_file(path):
    head, tail = os.path.split(path)
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")

    content_path = pathlib.Path("content")

    # create the dir for the new file if doesn't exist
    with suppress(FileExistsError):
        head_path = content_path / pathlib.Path(head)
        head_path.mkdir()

    file_path = content_path / head / tail
    if file_path.exists():
        print("File already exists.")
    else:
        with open(file_path, "w") as f:
            f.write(FM.substitute(today=today))
        print(f"Create {file_path}.")
