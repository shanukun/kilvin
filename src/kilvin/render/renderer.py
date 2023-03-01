import sys
from collections import defaultdict

import jinja2
import random
from markdown import Markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.toc import TocExtension


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

    def build_site(self):
        site = {}
        for key, value in self.config.items():
            site[key] = value
        site["tags"] = self.tags
        site["pages"] = self.pages
        return site

    def save_pages(self):
        site = self.build_site()

        for temp_name in self.pages:
            templ = self.get_template(temp_name)
            for page in self.pages[temp_name]:
                sorted_pages = page.pages
                sorted_pages.sort()

                out = templ.render(
                    cfg=site,
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
        print(page.url)
        renderer.render_markdown(page)
        for child_page in page.pages:
            renderer.render_markdown(child_page)
    renderer.save_pages()
