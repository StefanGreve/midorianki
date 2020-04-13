#!/usr/bin/env python

import os
import csv
import random

import click
import genanki
from tqdm import tqdm
from pathlib import Path
from colorama import Fore

def generate_model(model_name, model_id):
    """
        Generates a model that defines the template used for the deck creation.
        Excpects fields in `kanji,kana,meaning` convention for each single card.

        Args:
            model_name: The name of your model as displayed in Anki/Cards.
            model_id:   An ID for keeping track of your model.

        Returns:
            A model suitable for Japanese deck creation.
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
        css = """
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
    )

def export(file, name, dest, model_id = random.randrange(1 << 30, 1 << 31)):
    """
        Function that converts CSV files from Midori to an APKG deck. Source
        file should be in form of `kanji,kana,meaning`.

        Args:
            file: Path to CSV file.
            name: Deck filename and title.
            dest: APKG target directory.

        Returns:
            The ID of the generated anki model used for this deck creation.
    """

    notes = []

    if name == "not provided":
        name = Path(file).stem

    click.secho(f"Model ID: {model_id}")
    click.secho("Generating model for notes...", nl = False)

    with open(Path(file), 'r', encoding = "utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            notes.append(
                genanki.Note(
                    model = generate_model("JA-EN", model_id),
                    fields = [ row[0], row[1], row[2] ],
                )
            )

    click.secho("Done!")

    deck = genanki.Deck(model_id, name)
    package = genanki.Package(deck)

    for note in tqdm(notes,
                     bar_format = "{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET),
                     unit ='note',
                     desc = "Deck Processing",
                     ascii = "123456789*",
                     total = len(notes)):
        deck.add_note(note)

    package.write_to_file(Path(dest).joinpath(f"{name}.apkg"))

    click.secho(f"Created '{name}.apkg' with {len(deck.notes)} new cards in '{dest}'.")

    return model_id

@click.command()
@click.option('--file', type = click.Path(), help = "Path to CSV file.")
@click.option('--name', type = click.STRING, default = "not provided", help = "Deck filename and title.")
@click.option('--dest', type = click.Path(), default = os.getcwd(), help = "APKG target directory.")
def cli(file, name, dest):
    export(file, name, dest)

if __name__ == '__main__':
    cli()
