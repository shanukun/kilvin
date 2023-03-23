import datetime
from contextlib import suppress
from pathlib import Path
from string import Template

from kilvin import log
from kilvin.utils import is_kilvin_dir, join_path

CONTENT = "content"

FM = Template(
    """---
template:
title:
subtitle: 
date: $today
draft: True
---
"""
)


@is_kilvin_dir
def create_new_file(new_file):
    new_file = Path(new_file)
    new_dir, ext = new_file.parent, new_file.suffix

    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")

    content_path = Path(CONTENT)

    # create the dir for the new file if doesn't exist
    with suppress(FileExistsError):
        head_path = join_path(content_path, Path(new_dir))
        head_path.mkdir()

    file_path = join_path(content_path, new_file)

    try:
        with open(file_path, "w") as f:
            if ext == ".md":
                f.write(FM.substitute(today=today))
        log.succ(f"{file_path} created.")
    except FileExistsError as e:
        log.error(f"{e.filename} : {e.strerror}.")
