import xml.etree.ElementTree as ET
from datetime import datetime, timezone

NAMESPACE = "http://www.w3.org/2005/Atom"


def build_feed(config, sorted_pages, save_path):
    feed = ET.Element("feed", xmlns=NAMESPACE)
    ET.SubElement(feed, "title").text = config["title"]
    ET.SubElement(feed, "id").text = config["url"]
    ET.SubElement(feed, "url", href=config["url"])
    ET.SubElement(feed, "updated").text = datetime.now(timezone.utc).isoformat()

    author = ET.SubElement(feed, "author")
    ET.SubElement(author, "name").text = config["author"]["name"]
    ET.SubElement(author, "email").text = config["author"]["email"]

    for page in sorted_pages:
        entry = ET.Element("entry")
        ET.SubElement(entry, "title").text = page.meta["title"]

        ET.SubElement(entry, "updated").text = page.meta["date"].isoformat()
        ET.SubElement(entry, "id").text = page.url
        link = "{}/{}/{}".format(config["url"], page.rel_path, page.url)
        ET.SubElement(entry, "link", href=link)
        ET.SubElement(
            entry, "summary", type="html"
        ).text = "<h2>{subtitle}</h2>{body}".format(
            subtitle=page.meta["subtitle"], body=page.body
        )
        feed.append(entry)

    xml_file = save_path / "index.xml"

    with open(xml_file, "wb") as f:
        f.write(ET.tostring(feed, encoding="UTF-8", xml_declaration=True, method="xml"))
