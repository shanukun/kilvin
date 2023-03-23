from kilvin import log

CONFIG_TEMP = """title = ''
url = ''
description = ''

[author]
name = ''
email = ''
"""

CONFIG_FILE = "config.toml"


def gen_file(file_path, data):
    with open(file_path, "w") as f:
        f.write(data)


def create_project(path):
    dirs = ["public", "content", "static", "layouts"]

    abs_path = path.absolute()

    try:
        abs_path.mkdir()
        for dir in dirs:
            dir_path = abs_path / dir
            dir_path.mkdir()

        gen_file(abs_path / CONFIG_FILE, CONFIG_TEMP)

        log.succ(f"{path} directory for the project created.")
    except FileExistsError:
        log.info("Directory already exists.")
