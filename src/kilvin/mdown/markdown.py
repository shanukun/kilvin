import pathlib

import frontmatter
import jinja2
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension


def render(md_path):
    tl = jinja2.FileSystemLoader("./layouts")
    env = jinja2.Environment(loader=tl)
    with open(md_path) as f:
        post = frontmatter.load(f)

        temp = env.get_template("./default.html")
        html = markdown.markdown(
            post.content,
            extensions=[
                CodeHiliteExtension(),
                "fenced_code",
                "sane_lists",
                "footnotes",
                "md_in_html",
            ],
        )

        out = temp.render(title=post["title"], content=html)
    return out
