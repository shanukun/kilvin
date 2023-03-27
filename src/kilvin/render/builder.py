import sys
from collections import defaultdict
from pathlib import Path

import jinja2
from jinja2.exceptions import TemplateError, TemplateNotFound
from markdown import Markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.toc import TocExtension

from kilvin import log

from . import feed


def is_same_path(path, other):
    CONTENT = Path("./content")
    path = CONTENT / Path(path)
    other = CONTENT / Path(other)
    return path.samefile(other)


class KMarkdown(Markdown):
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

    def __init__(self):
        super().__init__(extensions=self.EXTENSIONS)

    def convert(self, source):
        super().reset()
        return super().convert(source)


class TempEngine:
    # Layout path in kilvin dir.
    LAYOUT = "layouts"
    FS = jinja2.FileSystemLoader(LAYOUT)

    def __init__(self):
        self.env = jinja2.Environment(loader=self.FS)

    def get_template(self, templt):
        try:
            return self.env.get_template(templt)
        except TemplateNotFound:
            log.error(f"Template {templt} not found.")
            sys.exit(1)


class Builder:
    """
    Handles the rendering and saving of all markdown file with suitable context.
    """

    def __init__(self, config):
        self.config = config
        self.conv = KMarkdown()
        self.temp_engine = TempEngine()

        self.pages = defaultdict(list)
        self.tags = []

    def get_site_context(self):
        site = {}
        for key, value in self.config.items():
            site[key] = value

        site["tags"] = self.tags
        site["pages"] = self.pages

        return site

    def render_markdown(self, page):
        html = self.conv.convert(page.body)
        page.body = html
        self.tags.extend(page.meta.get("tags", ""))
        self.pages[page.template].append(page)

    def render_template(self, site, page, template):
        try:
            out = template.render(
                site=site,
                meta=page.meta,
                pages=page.sorted_pages,
                dirs=page.dirs,
                body=page.body,
            )
            with open(page.save_path, "w") as f:
                f.write(out)
        except TemplateError as e:
            log.error(f"{e.message}")
            sys.exit(1)

    def build_feed(self, page):
        if page.is_index and not is_same_path(page.rel_path, "./"):
            feed.build(self.config, page.sorted_pages, page.save_dir)

    def save_pages(self):
        site = self.get_site_context()
        for temp_name in self.pages:
            templ = self.temp_engine.get_template(temp_name)
            for page in self.pages[temp_name]:
                self.render_template(site, page, templ)
                self.build_feed(page)


def render(page_list, config):
    builder = Builder(config)
    for page in page_list:
        builder.render_markdown(page)
        for child_page in page.pages:
            builder.render_markdown(child_page)
    builder.save_pages()
