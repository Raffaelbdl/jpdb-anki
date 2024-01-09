from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup
import requests


def load_url(url: str) -> BeautifulSoup:
    return BeautifulSoup(requests.get(url).content, "html.parser")


def get_base_url(url: str) -> str:
    return "https://" + url.split("/")[2]


def get_vocab_entries_from_one_page(jpdb: BeautifulSoup) -> list[str]:
    vocab_entries = jpdb.find_all(class_="vocabulary-spelling")
    return [s.find("a", href=True)["href"] for s in vocab_entries]


def get_all_vocab_entries(root_url: str) -> list[str]:
    base_url = get_base_url(root_url)

    jpdb = load_url(root_url)
    vocab_entries = get_vocab_entries_from_one_page(jpdb)
    vocab_entries = [base_url + e.strip("#a") for e in vocab_entries]

    if jpdb.find(class_="pagination without-next"):
        return vocab_entries

    next_root = jpdb.find(class_="pagination").find_all("a", href=True)[-1]["href"][:-2]
    vocab_entries += get_all_vocab_entries(base_url + next_root)
    return vocab_entries
