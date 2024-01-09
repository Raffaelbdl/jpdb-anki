import os
import pathlib

import genanki

from japanese_manager.fields import note


FORMAT_DIRECTORY = os.path.join("data", "anki")

recognition_qfmt_path = pathlib.Path(
    os.path.join(FORMAT_DIRECTORY, "recognition_qfmt.txt")
)
recognition_afmt_path = pathlib.Path(
    os.path.join(FORMAT_DIRECTORY, "recognition_afmt.txt")
)
recall_qfmt_path = pathlib.Path(os.path.join(FORMAT_DIRECTORY, "recall_qfmt.txt"))
recall_afmt_path = pathlib.Path(os.path.join(FORMAT_DIRECTORY, "recall_afmt.txt"))
css_path = pathlib.Path(os.path.join(FORMAT_DIRECTORY, "css.txt"))


def safe_read(path: pathlib.Path) -> str:
    with path.open("r") as f:
        return f.read()


def load_formats() -> dict:
    return {
        "recognition_qfmt": safe_read(recognition_qfmt_path),
        "recognition_afmt": safe_read(recognition_afmt_path),
        "recall_qfmt": safe_read(recall_qfmt_path),
        "recall_afmt": safe_read(recall_afmt_path),
        "css": safe_read(css_path),
    }


def load_model() -> genanki.Model:
    formats = load_formats()
    return genanki.Model(
        1697807219,
        "Python model",
        fields=[
            {"name": "Expression"},
            {"name": "PartOfSpeech"},
            {"name": "Spelling"},
            {"name": "Pitch"},
            {"name": "Frequency"},
            {"name": "Meanings"},
            {"name": "Examples"},
        ],
        templates=[
            {
                "name": "Recognition",
                "qfmt": formats["recognition_qfmt"],
                "afmt": formats["recognition_afmt"],
            },
            {
                "name": "Recall",
                "qfmt": formats["recall_qfmt"],
                "afmt": formats["recall_afmt"],
            },
        ],
        css=formats["css"],
    )


class AnkiNote(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0], self.fields[1])

    @classmethod
    def from_note(cls, note: note.Note, *, model: genanki.Model | None = None):
        expression = note.expression
        part_of_speech = note.part_of_speech
        spelling = note.spelling
        pitch = note.pitch.html if note.pitch else ""
        frequency = note.frequency

        meanings = ""
        for meaning in note.meanings:
            meanings += meaning + "<br>"

        examples = ""
        for i, example in enumerate(note.examples):
            examples += str(i) + ". " + example[0] + "<br>" + example[1] + "<br>"

        return AnkiNote(
            model=model,
            fields=[
                expression,
                part_of_speech,
                spelling,
                pitch,
                frequency,
                meanings,
                examples,
            ],
        )
