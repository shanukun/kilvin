import os
from pathlib import Path

import frontmatter

from kilvin import log
from kilvin.render import renderer
from kilvin.render.page import Page
from kilvin.utils import copy_dir, copy_file, is_kilvin_dir, join_path

DIR_CONTENT = "content"
DIR_PUBLIC = "public"
_INDEX = "_index.md"
INDEX = "index.html"


def is_md(file):
    file = Path(file)
    return file.suffix == ".md"


def is_index(file):
    file = Path(file)
    return file.stem == "_index"


def get_rel_path(full_path) -> Path:
    return Path("/".join(list(full_path.parts)[1:]))


def get_public_path(path):
    return join_path(Path(DIR_PUBLIC), path)


def build_dir(dir_path):
    """
    Util func for creating directory with given path.
    """
    try:
        if not dir_path.exists():
            dir_path.mkdir()
    except FileExistsError:
        log.info(f"{dir_path} already exists.")


def gen_html_path(md_path):
    """
    Create the required directories for pages.
    > content/dir/blog.md -> public/dir/blog/index.html < and returns the path.
    """

    rel_path = get_rel_path(md_path.parent)
    final_path = get_public_path(rel_path)

    build_dir(final_path)

    if is_index(md_path):
        html_path = join_path(final_path, INDEX)
    else:
        index_dir = join_path(final_path, md_path.stem)
        try:
            index_dir.mkdir()
        except FileExistsError:
            pass
        html_path = join_path(index_dir, INDEX)
    return rel_path, html_path


def process_md(file_path: Path, parent):
    """
    Process all markdown file found in content dir and create a raw page (Page)
    out of it.

    file_path: Path to a markdown file. Eg: ./content/*/file.md
    parent: Refers to the Page object created from _index.md in directory.
    """
    fmatter = frontmatter.load(file_path)

    rel_path, html_path = gen_html_path(file_path)

    # unrendered page
    raw_page = Page(
        name=file_path.stem if parent else rel_path,
        rel_path=rel_path,
        html_path=html_path,
        fmatter=fmatter.metadata,
        body=fmatter.content,
        is_index=False if parent else True,
    )
    if parent:
        parent.insert_page(raw_page)
    return raw_page


def process_non_md(file_path: Path):
    """
    All the files other than markdown should be directly copied to appropriate
    directory in public directory.
    """
    rel_path = get_rel_path(file_path)
    final_path = get_public_path(rel_path)

    copy_file(file_path, final_path)


def find_pages():
    """
    Seek all the files in content dirs.
    """
    content_path = Path(DIR_CONTENT)

    pages = []

    prev_index = None
    for root, dirs, files in os.walk(content_path):
        # ./content/*/
        root_path = Path(root)

        # ./content/*/_index.md
        index_md = join_path(root_path, _INDEX)

        index_page = None
        if index_md.exists():
            index_page = process_md(index_md, None)
            pages.append(index_page)

        index_page = index_page if index_page else prev_index

        for file in files:
            file_path = join_path(root_path, Path(file))

            if is_md(file_path) and not is_index(file_path):
                raw_page = process_md(file_path, index_page)
                if not index_page:
                    pages.append(raw_page)
            elif not is_index(file_path):
                process_non_md(file_path)

        if index_page:
            for dir in dirs:
                index_page.insert_dir(dir)
        prev_index = index_page

    return pages


@is_kilvin_dir
def build_proj(config):
    """
    Build the site from content and static files.
    """

    pages = find_pages()
    renderer.render(pages, config)

    copy_dir("./static", "./public/static")

    log.succ("Building finished.")
