import os
from pathlib import Path, PurePath

import frontmatter

from kilvin import utils
from kilvin.mdown import markdown

DIR_CONTENT = "content"
DIR_PUBLIC = "public"


class Page:
    def __init__(self, name, html_path, fmatter, body, is_index=False):
        # content/{path}
        self.url = name
        self.save_path = html_path
        self.meta = fmatter
        self.body = body
        self.is_index = is_index

        self._page_list = []

    def get_pages(self):
        return self._page_list

    def insert_page(self, page):
        self._page_list.append(page)


# content/pages/post.md -> ./pages/post.md
def get_rel_path(full_path) -> Path:
    return Path("/".join(list(full_path.parts)[1:]))


def build_dir(dir_path):
    try:
        if not dir_path.exists():
            dir_path.mkdir()
    except FileExistsError:
        print(f"{dir_path} already exists.")


def gen_html_path(md_path):
    file_name = md_path.name
    rel_path = get_rel_path(md_path.parent)

    final_path = Path(DIR_PUBLIC) / rel_path
    build_dir(final_path)

    html_file = "index.html"
    if file_name == "_index.md":
        return final_path / html_file
    else:
        index_dir = final_path / Path(file_name).stem
        index_dir.mkdir()
        return index_dir / html_file


# file_path: ./content/*/file.md
def process_md_file(file_path: Path, parent):
    fmatter = frontmatter.load(file_path)

    page = Page(
        file_path.stem,
        gen_html_path(file_path),
        fmatter.metadata,
        fmatter.content,
        False if parent else True,
    )
    if parent:
        parent.insert_page(page)
    return page


def process_non_md_file(file_path: Path):
    rel_path = get_rel_path(file_path)
    final_path = Path(DIR_PUBLIC) / rel_path
    print(f"{file_path} - {final_path}")
    utils.copy_file(file_path, final_path)


@utils.is_kilvin_dir
def build_proj(config):
    content_path = Path(DIR_CONTENT)

    page_list = []

    # TODO recursive method extra info for dirs
    for root, _, files in os.walk(content_path):
        root_path = Path(root)
        root_index = root_path / "_index.md"

        root_page = None
        if root_index.exists():
            root_page = process_md_file(root_index, None)
            page_list.append(root_page)

        for file in files:
            file_path = root_path / Path(file)

            if file_path.suffix == ".md" and file_path.stem != "_index":
                process_md_file(file_path, root_page)
            elif file_path.suffix != ".md":
                process_non_md_file(file_path)

    markdown.render(page_list, config)

    utils.copy_dir("./static", "./public/static")

    print("Building finished.")
