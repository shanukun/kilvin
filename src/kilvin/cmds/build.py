import os
import pathlib

import frontmatter

from kilvin.mdown import markdown

DIR_CONTENT = "content"
DIR_PUBLIC = "public"


class CFile:
    def __init__(self, name, rel_path):
        self.name = name
        self.rel_path = rel_path

        self.stem = pathlib.Path(name).stem
        self.ext = pathlib.PurePath(name).suffix

        self.md_path = pathlib.PurePath(DIR_CONTENT) / self.rel_path / self.name
        self.dir_path = pathlib.Path(DIR_PUBLIC) / self.rel_path / self.stem

        self.fmatter = self._get_fmatter()
        self.temp = "list.html" if self.stem == "_index" else "default.html"

        self._make_dir()
        self._copy_file()

    def _get_fmatter(self):
        return frontmatter.load(self.md_path)

    def _make_dir(self):
        if self.stem != "_index" and self.ext == ".md":
            self.dir_path.mkdir()

    def _copy_file(self):
        if self.ext != ".md":
            pass

    def _gen_rel_path(self, p):
        return self.rel_path / p

    def get_file_list(self):
        if self.stem == "_index":
            p = pathlib.Path(DIR_CONTENT) / self.rel_path
            return [
                self._gen_rel_path(f.stem) if f.is_dir() else self._gen_rel_path(f.stem)
                for f in p.iterdir()
                if f.stem != self.stem
            ]
        else:
            return []

    def get_html_path(self):
        if self.stem == "_index":
            return (
                pathlib.PurePath(DIR_PUBLIC)
                / self.rel_path
                / pathlib.PurePath("index.html")
            )
        else:
            return self.dir_path / pathlib.PurePath("index.html")


def build_proj():
    md_files = []
    for root, dirs, files in os.walk(DIR_CONTENT):
        rel_cur_path = "/".join(list(pathlib.PurePath(root).parts)[1:])

        public_path = pathlib.Path(DIR_PUBLIC) / rel_cur_path

        for dir in dirs:
            dir_path = public_path / dir
            dir_path.mkdir()

        for file in files:
            rel_path = pathlib.Path(rel_cur_path)
            md_files.append(CFile(file, rel_path))

    for cfile in md_files:
        out = markdown.render(
            cfile.md_path, tmp=cfile.temp, files=cfile.get_file_list()
        )
        with open(cfile.get_html_path(), "w") as f:
            f.write(out)

    print("Building finished.")
