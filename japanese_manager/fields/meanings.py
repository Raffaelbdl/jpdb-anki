from bs4 import BeautifulSoup


def get_meanings(jpdb: BeautifulSoup) -> list[str]:
    """Extracts meanings from JPDB page."""
    meanings = list(
        map(
            lambda x: x.text,
            jpdb.find(class_="subsection-meanings").find_all(class_="description"),
        )
    )
    return meanings
