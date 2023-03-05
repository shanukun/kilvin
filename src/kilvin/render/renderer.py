import sys
from collections import defaultdict
from pathlib import Path

import jinja2
from markdown import Markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.toc import TocExtension

from . import feed


def is_same_path(path, other):
    CONTENT = Path("./content")
    path = CONTENT / Path(path)
    other = CONTENT / Path(other)
    return path.samefile(other)


class Renderer:
    """
    Handles the rendering and saving of all markdown file with suitable context.
    """

    # Layout path in kilvin dir.
    LAYOUT = "layouts"

    # Extensions required for converting markdown to html.
    EXTENSIONS = [
        CodeHiliteExtension(),
        TocExtension(),
        "fenced_code",
        "footnotes",
        "md_in_html",
        "sane_lists",
        "tables",
        "abbr",
        "legacy_attrs",
    ]
    FS = jinja2.FileSystemLoader(LAYOUT)

    def __init__(self, config):
        self.config = config
        self.md_conv = Markdown(extensions=self.EXTENSIONS)
        self.env = jinja2.Environment(loader=self.FS)

        self.pages = defaultdict(list)
        self.tags = []

    def get_template(self, templt):
        try:
            return self.env.get_template(templt)
        except jinja2.exceptions.TemplateNotFound:
            print(f"Error: Template {templt} not found.")
            sys.exit(1)

    def render_markdown(self, page):
        html = self.md_conv.reset().convert(page.body)
        page.body = html
        self.tags.extend(page.meta.get("tags", ""))
        self.pages[page.template].append(page)

    def get_site_context(self):
        site = {}
        for key, value in self.config.items():
            site[key] = value
        site["tags"] = self.tags
        site["pages"] = self.pages
        return site

    def save_pages(self):
        site = self.get_site_context()

        for temp_name in self.pages:
            templ = self.get_template(temp_name)
            for page in self.pages[temp_name]:
                sorted_pages = page.pages
                if page.is_index and not is_same_path(page.rel_path, "./"):
                    sorted_pages.sort()
                    feed.build_feed(self.config, sorted_pages, page.save_dir)

                # TODO make template rendering part of render_markdown func.
                out = templ.render(
                    site=site,
                    meta=page.meta,
                    pages=sorted_pages,
                    dirs=page.dirs,
                    body=page.body,
                )
                with open(page.save_path, "w") as f:
                    f.write(out)


def render(page_list, config):
    renderer = Renderer(config)
    for page in page_list:
        renderer.render_markdown(page)
        for child_page in page.pages:
            renderer.render_markdown(child_page)
    renderer.save_pages()
