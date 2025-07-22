import urllib.request
import datetime
import email.utils
import pathlib
import html
from html.parser import HTMLParser

BASE_URL = "http://www.shigahochi.co.jp/"
TOP_URL = BASE_URL


def build_rss():
    now = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=9))
    )
    last_build = email.utils.format_datetime(now)

    try:
        req = urllib.request.Request(
            TOP_URL,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            html_data = resp.read().decode("shift_jis", errors="ignore")
    except Exception as e:
        print(f"ERROR: failed to fetch {TOP_URL}: {e}")
        return False

    class Parser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.in_p = False
            self.in_a = False
            self.curr_link = ""
            self.curr_title = ""
            self.items = []

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "p" and attrs.get("class") == "sp-caption-txt1":
                self.in_p = True
            elif tag == "a" and self.in_p:
                self.in_a = True
                self.curr_link = attrs.get("href", "")

        def handle_data(self, data):
            if self.in_a:
                self.curr_title += data

        def handle_endtag(self, tag):
            if tag == "a" and self.in_a:
                self.in_a = False
            elif tag == "p" and self.in_p:
                if self.curr_title and self.curr_link:
                    self.items.append((self.curr_title.strip(), self.curr_link))
                self.in_p = False
                self.curr_title = ""
                self.curr_link = ""

    parser = Parser()
    parser.feed(html_data)

    items = []
    for title, link in parser.items:
        if not link.startswith("http"):
            link = BASE_URL + link.lstrip("./")
        pub = email.utils.format_datetime(now)
        items.append(
            f"<item><title>{html.escape(title)}</title>"
            f"<link>{link}</link><guid>{link}</guid>"
            f"<pubDate>{pub}</pubDate></item>"
        )

    if not items:
        print("No items scraped. rss.xml will not be updated.")
        return False

    rss = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0">\n<channel>\n'
        '<title>滋賀報知新聞 新着記事</title>\n'
        f'<link>{TOP_URL}</link>\n'
        '<description>滋賀報知新聞トップページの新着記事をRSS配信</description>\n'
        f'<lastBuildDate>{last_build}</lastBuildDate>\n'
        + "\n".join(items) +
        '\n</channel>\n</rss>'
    )

    pathlib.Path("rss.xml").write_text(rss, encoding="utf-8")
    print("[DEBUG] rss.xml written")
    return True


if __name__ == "__main__":
    build_rss()
