import sys

import jinja2
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

        self.pages = []
        self.tags = []

    def get_default_templt(self, is_index=False):
        try:
            if is_index:
                return "text.html"
            else:
                return "text.html"
        except jinja2.exceptions.TemplateNotFound:
            print("Error: Default templates not found.")
            sys.exit(1)

    def get_template(self, page):
        templt = page.meta.get("template", None)
        if templt != None:
            return self.env.get_template(templt)
        else:
            default_templt = self.get_default_templt(page.is_index)
            return self.env.get_template(default_templt)

    def render_markdown(self, page):
        html = self.md_conv.reset().convert(page.body)
        page.body = html
        self.tags.extend(page.meta.get("tags", ""))
        self.pages.append(page)

    def build_site(self):
        site = {}
        for key, value in self.config.items():
            site[key] = value
        site["tags"] = self.tags
        site["pages"] = self.pages
        return site

    def save_pages(self):
        site = self.build_site()

        for page in self.pages:
            templ = self.get_template(page)

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
