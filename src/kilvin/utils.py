import functools
import pathlib
import shutil
import sys
from pathlib import Path

DIR_PUBLIC = "public"


def is_kilvin_dir(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cwd = pathlib.Path(".")
        config_path = cwd / "config.toml"
        if not config_path.exists():
            print("Error: Unable to locate config file.")
            sys.exit(1)
        return func(*args, **kwargs)

    return wrapper


def clean_public():
    path = pathlib.Path(DIR_PUBLIC)

    if not path.exists():
        print(f"{DIR_PUBLIC} does not exist")
        sys.exit(1)

    for fd in path.iterdir():
        if fd.is_dir():
            shutil.rmtree(fd)
        else:
            fd.unlink()


def copy_dir(src, dst):
    shutil.copytree(src, dst)


def copy_file(src, dst):
    shutil.copyfile(src, dst)
