import sys

from kilvin import log
from kilvin.utils import join_path

LIST = "list.html"
SINGLE = "single.html"


class Page:
    def __init__(self, name, rel_path, html_path, fmatter, body, is_index=False):
        self.name = name

        self.rel_path = rel_path
        self.save_path = html_path
        self.meta = fmatter
        self.body = body
        self.is_index = is_index

        self.page_list = []
        self.dir_list = []

    @property
    def url(self):
        return join_path("/", self.rel_path, self.name)

    @property
    def pages(self):
        return self.page_list

    @property
    def sorted_pages(self):
        self.page_list.sort()
        return self.pages

    @property
    def save_dir(self):
        return self.save_path.parent

    @property
    def template(self):
        try:
            templ = self.meta["template"]
        except KeyError:
            log.error(f"{self.name}.md: Invalid front matter.")
            sys.exit(1)

        if templ != None:
            return templ
        elif self.is_index:
            return LIST
        else:
            return SINGLE

    @property
    def dirs(self):
        return self.dir_list

    def __lt__(self, other):
        try:
            return self.meta["date"] > other.meta["date"]
        except KeyError:
            return self.url > other.url
