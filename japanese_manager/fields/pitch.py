import json
import os
import pathlib

# region Generate SVG from https://github.com/IllDepence/SVG_pitch


def hira_to_mora(hira: str) -> list[str]:
    """Converts hiragana to mora.

    Args:
        hira: A string of hiragana.
    Returns:
        mora: A list of moras.

    Example:
        in:  'しゅんかしゅうとう'
        out: ['しゅ', 'ん', 'か', 'しゅ', 'う', 'と', 'う']
    """

    mora_arr = []
    combiners = [
        "ゃ",
        "ゅ",
        "ょ",
        "ぁ",
        "ぃ",
        "ぅ",
        "ぇ",
        "ぉ",
        "ャ",
        "ュ",
        "ョ",
        "ァ",
        "ィ",
        "ゥ",
        "ェ",
        "ォ",
    ]

    i = 0
    while i < len(hira):
        if i + 1 < len(hira) and hira[i + 1] in combiners:
            mora_arr.append("{}{}".format(hira[i], hira[i + 1]))
            i += 2
        else:
            mora_arr.append(hira[i])
            i += 1
    return mora_arr


def circle(x, y, o=False):
    r = ('<circle r="5" cx="{}" cy="{}" style="opacity:1;fill:#000;" />').format(x, y)
    if o:
        r += (
            '<circle r="3.25" cx="{}" cy="{}" style="opacity:1;fill:#fff;"' "/>"
        ).format(x, y)
    return r


def text(x, mora):
    # letter positioning tested with Noto Sans CJK JP
    if len(mora) == 1:
        return (
            '<text x="{}" y="67.5" style="font-size:20px;font-family:sans-'
            'serif;fill:#000;">{}</text>'
        ).format(x, mora)
    else:
        return (
            '<text x="{}" y="67.5" style="font-size:20px;font-family:sans-'
            'serif;fill:#000;">{}</text><text x="{}" y="67.5" style="font-'
            'size:14px;font-family:sans-serif;fill:#000;">{}</text>'
        ).format(x - 5, mora[0], x + 12, mora[1])


def path(x, y, typ, step_width):
    if typ == "s":  # straight
        delta = "{},0".format(step_width)
    elif typ == "u":  # up
        delta = "{},-25".format(step_width)
    elif typ == "d":  # down
        delta = "{},25".format(step_width)
    return (
        '<path d="m {},{} {}" style="fill:none;stroke:#000;stroke-width' ':1.5;" />'
    ).format(x, y, delta)


def pitch_svg(word: str, patt, silent=False):
    """Draw pitch accent patterns in SVG

    Examples:
        はし HLL (箸)
        はし LHL (橋)
        はし LHH (端)
    """

    mora = hira_to_mora(word)

    if len(patt) - len(mora) != 1 and not silent:
        print(
            ("pattern should be number of morae + 1 (got: {}, {})").format(word, patt)
        )
    positions = max(len(mora), len(patt))
    step_width = 35
    margin_lr = 16
    svg_width = max(0, ((positions - 1) * step_width) + (margin_lr * 2))

    svg = (
        '<svg class="pitch" width="{0}px" height="75px" viewBox="0 0 {0} 75' '">'
    ).format(svg_width)
    svg += '<rect width="{0}px" height="75px" style="fill:rgb(255,255,255);opacity:1"></rect>'.format(
        svg_width
    )

    chars = ""
    for pos, mor in enumerate(mora):
        x_center = margin_lr + (pos * step_width)
        chars += text(x_center - 11, mor)

    circles = ""
    paths = ""
    for pos, accent in enumerate(patt):
        x_center = margin_lr + (pos * step_width)
        if accent in ["H", "h", "1", "2"]:
            y_center = 5
        elif accent in ["L", "l", "0"]:
            y_center = 30
        circles += circle(x_center, y_center, pos >= len(mora))
        if pos > 0:
            if prev_center[1] == y_center:
                path_typ = "s"
            elif prev_center[1] < y_center:
                path_typ = "d"
            elif prev_center[1] > y_center:
                path_typ = "u"
            paths += path(prev_center[0], prev_center[1], path_typ, step_width)
        prev_center = (x_center, y_center)

    svg += chars
    svg += paths
    svg += circles
    svg += "</svg>"

    return svg


# endregion


def pitch_position_to_pattern(mora: list[str], position: int) -> str:
    length = len(mora)
    if position == 0:
        return "0" + "1" * length
    if position == 1:
        return "1" + "0" * length
    if position == length + 1:
        return "0" + "1" * (length - 1) + "0"
    if position >= 2:
        return "0" + "1" * (position - 1) + "0" * (length - position + 1)


PITCH_DATA_DIRECTORY = os.path.join("data", "pitch")
PITCH_DICTIONARY_PATH = os.path.join(PITCH_DATA_DIRECTORY, "pitch_dictionary.json")


def load_pitch_dictionary(*, alt_path: str | None = None) -> dict:
    """Loads a pitch dictionary.
    Args:
        alt_path: An alternative path to a pitch dictionary.
    Returns:
        The pitch dictionary.

    Structure of the pitch dictionary
    ```
    {
        expression:
            {
                spelling 0: pitch_position 0,
                spelling 1: pitch_position 1,
            }
    }
    ```
    """
    path = pathlib.Path(alt_path if alt_path else PITCH_DICTIONARY_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        with path.open("r") as file:
            return json.load(file)

    print("Creating pitch dictionary...")

    pitch_dictionary = {}
    for bank_file in os.listdir(PITCH_DATA_DIRECTORY):
        if "term_meta_bank" in bank_file:
            with open(os.path.join(PITCH_DATA_DIRECTORY, bank_file), "r") as file:
                bank = json.load(file)

        for expression, _, pitch_data in bank:
            spelling = pitch_data["reading"]
            position = pitch_data["pitches"][0]["position"]

            if expression in pitch_dictionary:
                pitch_dictionary[expression][spelling] = position
            else:
                pitch_dictionary[expression] = {spelling: position}

    with path.open("w") as file:
        json.dump(pitch_dictionary, file)

    return pitch_dictionary


def get_pitch_position(pitch_dictionary: dict, expression: str, spelling: str) -> int:
    return pitch_dictionary[expression][spelling]


class Pitch:
    __slots__ = ["expression", "spelling", "mora", "html"]

    @classmethod
    def from_expression_and_spelling(
        cls, expression: str, spelling: str, *, pitch_dictionary: dict | None = None
    ):
        """Creates an instance of Pitch given an expression and spelling"""
        pitch = Pitch()
        pitch.expression = expression
        pitch.spelling = spelling
        pitch.mora = hira_to_mora(spelling)

        pitch_dictionary = (
            pitch_dictionary if pitch_dictionary else load_pitch_dictionary()
        )
        try:
            pitch_position = get_pitch_position(pitch_dictionary, expression, spelling)
        except KeyError:
            return None

        pitch_pattern = pitch_position_to_pattern(pitch.mora, pitch_position)
        pitch.html = pitch_svg(spelling, pitch_pattern)
        return pitch
