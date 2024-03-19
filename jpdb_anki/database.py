import json
import os
import pathlib
import pickle

import genanki
from tqdm import tqdm
import yaml

from jpdb_anki.anki import AnkiNote
from jpdb_anki.fields import note
from jpdb_anki.scraping import get_all_vocab_entries, get_vocab_entries_from_text

NOTES_DIRECTORY = os.path.join("data", "notes")
LISTS_DIRECTORY = os.path.join("data", "lists")


def safe_pickle_load(path: pathlib.Path):
    with path.open("rb") as file:
        return pickle.load(file)


def safe_pickle_dump(obj, path: pathlib.Path):
    with path.open("wb") as file:
        return pickle.dump(obj, file)


def safe_json_dump(obj, path: pathlib.Path):
    with path.open("w") as file:
        json.dump(obj, file)


def safe_json_load(path: pathlib.Path):
    with path.open("r") as file:
        return json.load(file)


def safe_yaml_load(path: pathlib.Path):
    with path.open("r") as file:
        return yaml.load(file, yaml.SafeLoader)


def list_key(url: str) -> str:
    tmp = url.split("/")
    return tmp[-2] + "_" + tmp[-1]


def note_key(url: str) -> str:
    return url.split("/")[-1]


class Database:
    notes: dict[str, pathlib.Path]  # {expression: path / contains pickled note}
    lists: dict[str, pathlib.Path]  # {url: path / contains json list of urls}

    def __init__(
        self,
        *,
        pitch_dictionary: dict | None = None,
        model: genanki.Model | None = None
    ) -> None:
        self.pitch_dictionary = pitch_dictionary
        self.model = model
        self.deck_id = safe_yaml_load(pathlib.Path("./config.yaml"))["deck_id"]

        self.load()

    def load(self) -> None:
        os.makedirs(NOTES_DIRECTORY, exist_ok=True)
        os.makedirs(LISTS_DIRECTORY, exist_ok=True)
        self.notes = {
            note: pathlib.Path(os.path.join(NOTES_DIRECTORY, note))
            for note in os.listdir(NOTES_DIRECTORY)
        }
        self.lists = {
            list_: pathlib.Path(os.path.join(LISTS_DIRECTORY, list_))
            for list_ in os.listdir(LISTS_DIRECTORY)
        }

    def contains_note(self, key: str) -> bool:
        return key in self.notes

    def contains_list(self, key: str) -> bool:
        return key in self.lists

    def get_note(self, url: str) -> note.Note:
        key = note_key(url)

        if self.contains_note(key):
            return safe_pickle_load(self.notes[key])

        path = pathlib.Path(os.path.join(NOTES_DIRECTORY, key))
        self.notes[key] = path

        note_ = note.Note.from_jpdb(url, pitch_dictionary=self.pitch_dictionary)
        safe_pickle_dump(note_, path)

        return note_

    def get_list(self, url: str) -> list[str]:
        key = list_key(url)

        if self.contains_list(key):
            return safe_json_load(self.lists[key])

        print("Creating new list", key)

        list_ = pathlib.Path(os.path.join(LISTS_DIRECTORY, key))
        self.lists[key] = list_

        vocab = get_all_vocab_entries(url)
        safe_json_dump(vocab, list_)

        print("List", key, " created.")

        return vocab

    def write_apkg_from_db(self, filepath: str) -> None:
        """Writes the apkg file with all the current notes.

        Args:
            filepath: A string path to the wanted apkg file location.
        """
        return self.write_apkg_from_list(filepath, self.notes)

    def write_apkg_from_list(self, filepath: str, urls: list[str]) -> None:
        """Writes the apkg file from a list of vocabulary entries.

        This is also compatible with a list of expressions.

        Args:
            filepath: A string path to the wanted apkg file location.
            urls: A list of vocabulary entries.
        """
        deck = genanki.Deck(self.deck_id, "Python deck")
        for e in tqdm(urls, desc="Generating Package."):
            deck.add_note(AnkiNote.from_note(self.get_note(e), model=self.model))
        genanki.Package(deck).write_to_file(filepath)

        print("APKG successfully generated.")

    def write_apkg_from_text(self, filepath: str, textpath: str) -> None:
        """Writes the apkg file with all the words in a given text.

        Args:
            filepath: A string path to the wanted apkg file location.
            textpath: A string path to the text to parse.
        """
        with open(textpath, "r") as file:
            text = file.read()
        vocab_entries = get_vocab_entries_from_text(text)
        self.write_apkg_from_list(filepath, vocab_entries)
