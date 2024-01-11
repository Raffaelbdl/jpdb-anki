"""Command line tasks.

Three tasks are currently available:

- scraping: `python -m jpdb_anki -t scrape -vl $vocabulary-list-url
    Scrapes a vocabulary list from JPDB and creates an APKG file
    that can be imported into Anki.

- generating: `python -m jpdb_anki -t generate
    Loads saved notes and creates and APKG file that can be imported 
    into Anki.

- search: `python -m jpdb_anki -t search -e $expression
    Creates a note for an expression by searching JPDB.
    In the case of multiple search results from JPDB, the most 
    used word will be selected.
"""

from absl import flags, app

from jpdb_anki.anki import load_model
from jpdb_anki.database import Database
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


def main(_):
    db = Database(pitch_dictionary=pitch.load_pitch_dictionary(), model=load_model())

    if FLAGS.task == "scrape":
        vocab_entries = db.get_list(FLAGS.vocablist)
        db.write_apkg_from_list("output.apkg", vocab_entries)

    elif FLAGS.task == "generate":
        db.write_apkg_from_db("output.apkg")

    elif FLAGS.task == "search":
        db.get_note(get_vocab_entry_from_search(FLAGS.expression))


if __name__ == "__main__":
    app.run(main)
