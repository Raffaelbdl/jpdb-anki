from bs4 import BeautifulSoup


def get_spelling(jpdb: BeautifulSoup) -> str:
    """Extracts spelling from JPDB page."""
    spelling = ""
    contents = jpdb.find(class_="primary-spelling").find("ruby").contents
    for s in contents:
        s = str(s)
        if "<rt>" in s:
            in_s = s.strip("<rt>").strip("</rt>")
            if len(in_s) > 0:
                s = "[" + in_s + "]"
            else:
                s = ""
        spelling += s
    return spelling
