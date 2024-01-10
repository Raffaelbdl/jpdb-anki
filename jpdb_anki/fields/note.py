from jpdb_anki.fields import examples, meanings, pitch, spelling
from jpdb_anki.scraping import load_url


class Note:
    expression: str
    reading: str
    frequency: int
    spelling: str
    part_of_speech: str
    meanings: list[str]
    pitch: pitch.Pitch
    examples: list[str]
    url: str

    @classmethod
    def from_jpdb(cls, url: str, *, pitch_dictionary: dict | None = None):
        jpdb = load_url(url)

        note = Note()
        note.expression = jpdb.find("title").text.split(" ")[0]
        note.reading = (
            jpdb.find("meta", attrs={"name": "description"})
            .attrs["content"]
            .split(" ")[4][1:-1]
        )
        freq = jpdb.find(class_="tag tooltip")
        note.frequency = int(freq.text.split(" ")[-1]) if freq else 100000
        note.spelling = spelling.get_spelling(jpdb)
        note.part_of_speech = jpdb.find(class_="part-of-speech").contents[-1].text
        note.meanings = meanings.get_meanings(jpdb)
        note.pitch = pitch.Pitch.from_expression_and_reading(
            note.expression, note.reading, pitch_dictionary=pitch_dictionary
        )
        note.examples = examples.get_examples(jpdb)
        note.url = url

        return note