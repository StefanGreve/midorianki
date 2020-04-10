#!/usr/bin/env python
import csv
import errno
import random

import genanki
from pathlib import Path

def generate_model(model_name, model_id):
    font = "font-family: Meiryo"
    card = """
        .card {
            font-family: arial;
            font-size: 20px;
            text-align: center;
            color: black;
            background-color: white;
        }
        .card1 {
            background-color: #969696;
        }
        .card2 {
            background-color: #969696;
        }
    """
    return genanki.Model(
        model_id,
        model_name,
        fields = [
            { 'name' : 'kanji' },
            { 'name' : 'kana' },
            { 'name' : 'meaning' }
        ],
        templates = [
            {
                'name' : 'Forward Card Template',
                'qfmt' : '<strong style="font-family: Meiryo; font-size: 60px;">{{kanji}}</strong>',
                'afmt' : '{{FrontSide}}<hr id="answer"><span style="font-family: Meiryo; font-size: 30px;">{{kana}}</span><br><strong style="font-size: 40px;">{{meaning}}</strong>'
            },
            {
                'name' : 'Backward Card Template',
                'qfmt' : '<strong style="font-size: 40px;">{{meaning}}</strong>',
                'afmt' : '{{FrontSide}}<hr id="answer"><strong style="font-family: Meiryo; font-size: 60px">{{kanji}}</strong><br><span style="font-family: Meiryo; font-size: 30px;">{{kana}}</span>'
            }
        ],
        css = card
    )

def export(filename, target_dir = Path.cwd()):
    notes = []
    name = Path(filename).stem
    model_id = random.randrange(1 << 30, 1 << 31)

    # read csv file and create new notes
    cwd = Path.cwd().joinpath("samples/source")

    with open(cwd.joinpath(filename), 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            notes.append(
                genanki.Note(
                    model = generate_model("JA-EN", model_id),
                    fields = [row[0], row[1], row[2]],
                )
            )

    # create & store deck to target_dir
    deck = genanki.Deck(model_id, name)
    package = genanki.Package(deck)

    for note in notes:
        deck.add_note(note)

    package.write_to_file(Path(target_dir).joinpath(f"{name}.apkg"))
    print(f"Created deck with {len(deck.notes)} new flashcards in '{target_dir}'.")
    return 0

if __name__ == '__main__':
    export("風の歌を聴け.csv")
