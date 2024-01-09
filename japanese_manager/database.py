import json
import os
import pathlib
import pickle

import genanki

from japanese_manager.fields import note
from japanese_manager.scraping import get_all_vocab_entries

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
        self.deck_id = 1294895494

        self.load()

    def load(self) -> None:
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
