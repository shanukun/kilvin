class Page:
    def __init__(self, name, html_path, fmatter, body, is_index=False):
        # content/{path}
        self.url = name
        self.save_path = html_path
        self.meta = fmatter
        self.body = body
        self.is_index = is_index

        self.page_list = []
        self.dir_list = []

    @property
    def pages(self):
        return self.page_list

    @property
    def template(self):
        templ = self.meta['template']
        if templ != None:
            return templ
        elif self.is_index:
            return "text.html"
        else:
            return "text.html"
            

    @property
    def dirs(self):
        return self.dir_list

    def insert_page(self, page):
        self.page_list.append(page)

    def insert_dir(self, dir):
        self.dir_list.append(dir)

    def __lt__(self, other):
        try:
            return self.meta["date"] > other.meta["date"]
        except KeyError:
            return self.url > other.url
