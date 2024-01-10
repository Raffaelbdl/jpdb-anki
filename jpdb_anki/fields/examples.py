from bs4 import BeautifulSoup


def get_examples(jpdb: BeautifulSoup) -> list[tuple[str, str]]:
    """Extracts examples from JPDB page."""
    examples = jpdb.find(class_="subsection-examples")
    if not examples:
        return []
    examples = examples.find_all(class_="used-in")
    jp = [e.find(class_="jp").text for e in examples]
    en = [e.find(class_="en").text for e in examples]
    return list(zip(jp, en))
