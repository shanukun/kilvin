import frontmatter
import jinja2
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension


def render(md_path, tmp="./default.html", files=[]):
    tl = jinja2.FileSystemLoader("./layouts")
    env = jinja2.Environment(loader=tl)
    with open(md_path) as f:
        post = frontmatter.load(f)

        temp = env.get_template(tmp)
        html = markdown.markdown(
            post.content,
            extensions=[
                CodeHiliteExtension(),
                "fenced_code",
                "footnotes",
                "md_in_html",
                "sane_lists",
                "tables",
                "abbr",
                "legacy_attrs",
            ],
        )

        out = temp.render(title=post["title"], content=html, files=files)
    return out
