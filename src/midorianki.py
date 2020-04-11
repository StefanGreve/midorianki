#!/usr/bin/env python

import os
import csv
import random

import click
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

def export(file, name, dest):
    """
        Function that converts CSV files from Midori to an APKG deck. Source
        file should be in form of `kanji,kana,meaning`.

        Args:
            file: Path to CSV file.
            name: Deck filename and title.
            dest: APKG target directory.

        Returns:
            Zero if the method executed successfully.
    """
    
    notes = []
    model_id = random.randrange(1 << 30, 1 << 31)

    if name == "not provided":
        name = Path(file).stem

    with open(Path(file), 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            notes.append(
                genanki.Note(
                    model = generate_model("JA-EN", model_id),
                    fields = [row[0], row[1], row[2]],
                )
            )

    deck = genanki.Deck(model_id, name)
    package = genanki.Package(deck)

    for note in notes:
        deck.add_note(note)

    package.write_to_file(Path(dest).joinpath(f"{name}.apkg"))

    click.secho(f"Created '{name}.apkg' with {len(deck.notes)} new cards in '{dest}'.", fg = 'yellow')

    return 0

@click.command()
@click.option('--file', type = click.Path(), help = "Path to CSV file.")
@click.option('--name', type = click.STRING, default = "not provided", help = "Deck filename and title.")
@click.option('--dest', type = click.Path(), default = os.getcwd(), help = "APKG target directory.")
def cli(file, name, dest):
    export(file, name, dest)

if __name__ == '__main__':
    cli()
