import genanki
from tqdm import tqdm

from japanese_manager.anki import AnkiNote, load_model
from japanese_manager.database import Database
from japanese_manager.fields import pitch


def make_package_from_vocabulary_list(url: str):
    db = Database(pitch_dictionary=pitch.load_pitch_dictionary(), model=load_model())

    vocab_entries = db.get_list(url)

    deck = genanki.Deck(db.deck_id, "Python deck")
    for e in tqdm(vocab_entries, desc="Creating notes"):
        deck.add_note(AnkiNote.from_note(db.get_note(e), model=db.model))

    genanki.Package(deck).write_to_file("output.apkg")


if __name__ == "__main__":
    make_package_from_vocabulary_list(
        "https://jpdb.io/novel/5829/kuma-kuma-kuma-bear/vocabulary-list"
        # "https://jpdb.io/novel/5706/koguma-no-kuuku-monogatari-haru-to-natsu/vocabulary-list"
    )
