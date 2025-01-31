# JPDB Anki Note Creator (Not updated!)

![Python Version](https://img.shields.io/badge/Python->=3.10-blue)
![Code Style](https://img.shields.io/badge/Code_Style-black-black)

An add-on in development is available here: [https://github.com/Raffaelbdl/kuma-browser](https://github.com/Raffaelbdl/kuma-browser).

[**Installation**](#installation) 
| [**Example Usage**](#example-usage)

This project helps creating Anki note from the website [JPDB](https://jpdb.io/).

## Installation
This package requires Python 3.10 or later.

First clone the project:
```bash
git clone https://github.com/Raffaelbdl/jpdb-anki
cd jpdb-anki
```

Then install the Python requirements. I recommend using a virtual envrionment.
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Create a `config.yaml` file with a deck id. Use `import random; random.randrange(1 << 30, 1 << 31)` to generate an ID.
```yaml
deck_id: 1294895494
```

## Example Usage
### Scrape a JPDB vocabulary list

This command scrapes all the vocabulary entries from the provided list, generates the files for each entry and writes an APKG file for the provided list.

```bash
python -m jpdb_anki -t scrape -vl https://jpdb.io/novel/5829/kuma-kuma-kuma-bear/vocabulary-list
```

### Create a note from an expression

This command searches for the provided expression and writes a note in the database based on the first search result.

```bash
python -m jpdb_anki -t search -e 熊
```

### Generate an APKG file from your database

This command writes an APKG file with your saved notes.

```bash
python -m jpdb_anki -t generate
```

### Generate an APKG file from a text file

This command writes an APKG file by parsing a text file.

First, create a text file, for instance `example.txt` and dump the text you want to parse in it.
Then use the next command to generate the APKG:

```bash
python -m jpdb_anki -t parse -txt example.txt
```

## Provided template
I provide my template. You can change the template in the directory `./data/anki/`.

![kuma](./resources/kuma.png)
