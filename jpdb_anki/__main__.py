import os

from absl import flags, app
import genanki
from tqdm import tqdm

from jpdb_anki.anki import AnkiNote, load_model
from jpdb_anki.database import Database, NOTES_DIRECTORY
from jpdb_anki.fields import pitch
from jpdb_anki.scraping import get_vocab_entry_from_search


flags.DEFINE_enum(
    "task",
    "scrape",
    ["generate", "scrape", "search"],
    "Select task to perform.",
    short_name="t",
)
flags.DEFINE_string(
    "vocablist",
    None,
    "Url to JPDB vocabulary list. Url should finish with '/vocabulary-list",
    short_name="vl",
)
flags.DEFINE_string(
    "expression", None, "Expression to search to create a note.", short_name="e"
)
FLAGS = flags.FLAGS


def make_package_from_vocabulary_list(url: str) -> None:
    db = Database(pitch_dictionary=pitch.load_pitch_dictionary(), model=load_model())

    vocab_entries = db.get_list(url)

    deck = genanki.Deck(db.deck_id, "Python deck")
    for e in tqdm(vocab_entries, desc="Creating notes"):
        deck.add_note(AnkiNote.from_note(db.get_note(e), model=db.model))

    genanki.Package(deck).write_to_file("output.apkg")


def generate_apkg() -> None:
    db = Database(pitch_dictionary=pitch.load_pitch_dictionary(), model=load_model())

    deck = genanki.Deck(db.deck_id, "Python deck")
    for e in tqdm(os.listdir(NOTES_DIRECTORY), desc="Creating notes"):
        deck.add_note(AnkiNote.from_note(db.get_note(e), model=db.model))

    genanki.Package(deck).write_to_file("output.apkg")
    print("APKG successfully generated.")


def create_note_from_search(expression: str) -> None:
    db = Database(pitch_dictionary=pitch.load_pitch_dictionary(), model=load_model())
    db.get_note(get_vocab_entry_from_search(expression))

    print("Note created for ", expression)


def main(_):
    if FLAGS.task == "scrape":
        make_package_from_vocabulary_list(FLAGS.vocablist)
    elif FLAGS.task == "generate":
        generate_apkg()
    elif FLAGS.task == "search":
        create_note_from_search(FLAGS.expression)


if __name__ == "__main__":
    app.run(main)
