# JPDB Anki Note Creator

![Python Version](https://img.shields.io/badge/Python->=3.10-blue)
![Code Style](https://img.shields.io/badge/Code_Style-black-black)

[**Installation**](#installation) 
| [**Example Usage**](#example-usage)

## Installation
This package requires Python 3.10 or later.

```bash
pip install --upgrade pip
pip install -r requirements.txt
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