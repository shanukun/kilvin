import sys
from datetime import datetime
from pathlib import Path

import jinja2
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.toc import TocExtension


def get_rel_path(full_path) -> Path:
    return Path("/".join(list(full_path.parts)[1:]))


class RenderedPage:
    def __init__(self, name, path, meta, body, is_index=False):
        self.url = name
        self.save_path = path
        self.meta = meta
        self.body = body
        self.is_index = is_index

        self.pages = []

    def insert_page(self, page):
        self.pages.append(page)

    def __lt__(self, other):
        try:
            return self.meta["date"] > other.meta["date"]
        except KeyError:
            return self.url > other.url


class Renderer:
    LAYOUT = "layouts"
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

    def __init__(self, config):
        self._config = config

        self._md_converter = markdown.Markdown(extensions=self.EXTENSIONS)
        self._fs = jinja2.FileSystemLoader(self.LAYOUT)
        self._env = jinja2.Environment(loader=self._fs)

        self._pages = []
        self._tags = []

    def _get_default_templt(self, is_index=False):
        try:
            if is_index:
                return "text.html"
            else:
                return "text.html"
        except jinja2.exceptions.TemplateNotFound:
            print("Error: Default templates not found.")
            sys.exit(1)

    def _get_template(self, page):
        templt = page.meta.get("template", None)

        if templt != None:
            return self._env.get_template(templt)
        else:
            default_templt = self._get_default_templt(page.is_index)
            return self._env.get_template(default_templt)

    def render_markdown(self, page) -> RenderedPage:
        html = self._md_converter.convert(page.body)
        self._md_converter.reset()

        rendered_page = RenderedPage(
            page.url, page.save_path, page.meta, html, page.is_index
        )

        self._tags.extend(page.meta.get("tags", ""))
        self._pages.append(rendered_page)

        return rendered_page

    def _build_site(self):
        site = {}
        for key, value in self._config.items():
            site[key] = value
        site["tags"] = self._tags
        site["pages"] = self._pages

        return site

    def save_pages(self):
        site = self._build_site()

        for page in self._pages:
            templ = self._get_template(page)

            sorted_pages = page.pages
            sorted_pages.sort()
            out = templ.render(
                cfg=site,
                meta=page.meta,
                pages=sorted_pages,
                body=page.body,
            )
            with open(page.save_path, "w") as f:
                f.write(out)


def render(page_list, config):
    renderer = Renderer(config)

    for page in page_list:
        index_page = renderer.render_markdown(page)
        for child_page in page.get_pages():
            rendrd_child = renderer.render_markdown(child_page)
            index_page.insert_page(rendrd_child)

    renderer.save_pages()
