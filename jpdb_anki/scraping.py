from bs4 import BeautifulSoup
import requests
import spacy
from tqdm import tqdm


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

    without_prev = jpdb.find(class_="pagination without-prev")
    if without_prev:
        next_root = without_prev.find_all("a", href=True)[-1]["href"][:-2]
        vocab_entries += get_all_vocab_entries(base_url + next_root)
        return vocab_entries

    next_root = jpdb.find(class_="pagination").find_all("a", href=True)[-1]["href"][:-2]
    vocab_entries += get_all_vocab_entries(base_url + next_root)
    return vocab_entries


def get_vocab_entry_from_search(expression: str) -> str:
    search_url = "https://jpdb.io/search?q=" + expression
    jpdb = load_url(search_url)
    if jpdb.find(class_="results details"):
        links = jpdb.find_all("link", href=True)
        for l in links:
            if "canonical" in l.attrs["rel"]:
                return l.attrs["href"].strip("#a")
    entry = (
        jpdb.find(class_="results search")
        .find(class_="view-conjugations-link")
        .attrs["href"]
    )
    return get_base_url(search_url) + entry.strip("#a")


def get_vocab_entries_from_text(text: str) -> list[str]:
    tokenized = spacy.load("ja_ginza")(text)
    seen_tokens = set()
    vocab_entries = []

    for i, sent in enumerate(tokenized.sents):
        for token in tqdm(sent, f"Searching expressions for sentence {i}."):
            if token.norm_ in seen_tokens:
                continue
            seen_tokens.add(token.norm_)

            try:
                vocab_entries.append(get_vocab_entry_from_search(token.norm_))
            except AttributeError:
                continue

    return vocab_entries
