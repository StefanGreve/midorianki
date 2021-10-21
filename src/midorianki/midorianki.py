#!/usr/bin/env python3

"""
CLI for transforming CSV files from Midori into APKG decks.

Copyright (C) 2020  Stefan Greve (greve.stefan@outlook.jp)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path
from typing import Dict, Iterable, Union

import genanki
from tqdm import tqdm

from . import config, utils


def progressbar_options(iterable: Iterable, desc: str, unit: str, color: str=config.GREEN, char: str='\u25CB', disable: bool=False) -> dict:
    """
    Return custom optional arguments for `tqdm` progressbars.
    """
    return {
        'iterable': iterable,
        'bar_format': "{l_bar}%s{bar}%s{r_bar}" % (color, config.RESET_ALL),
        'ascii': char.rjust(9, ' '),
        'desc': desc,
        'unit': unit.rjust(1, ' '),
        'total': len(iterable),
        'disable': not disable
    }

def generate_model(model_name: str, model_id: int) -> Dict:
    """
    Generates a model that defines the template used for deck this creation.
    Excpects all fields to follow the order of `kanji,kana,meaning`.
    """
    return genanki.Model(
        model_id,
        model_name,
        fields = [
            { 'name': 'kanji' },
            { 'name': 'kana' },
            { 'name': 'meaning' }
        ],
        templates = [
            {
                'name': 'Forward Card Template',
                'qfmt': '<strong style="font-family: Meiryo; font-size: 60px;">{{kanji}}</strong>',
                'afmt': '{{FrontSide}}<hr id="answer"><span style="font-family: Meiryo; font-size: 30px;">{{kana}}</span><br><strong style="font-size: 40px;">{{meaning}}</strong>'
            },
            {
                'name': 'Backward Card Template',
                'qfmt': '<strong style="font-size: 40px;">{{meaning}}</strong>',
                'afmt': '{{FrontSide}}<hr id="answer"><strong style="font-family: Meiryo; font-size: 60px">{{kanji}}</strong><br><span style="font-family: Meiryo; font-size: 30px;">{{kana}}</span>'
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

def export(file: Union[str, Path], name: str, dest: Union[str, Path], verbose: bool=False) -> int:
    """
    Converts CSV files into APKG decks. Expects all fields in the CSV file to
    follow the order of `kanji,kana,meaning`. Returns a randomly generated model
    id.
    """
    notes = []
    model_id = random.randrange(1 << 30, 1 << 31)

    with open(file, mode='r', encoding="utf-8") as file_handler:
        reader = csv.reader(file_handler)
        for row in reader:
            notes.append(
                genanki.Note(
                    model = generate_model("JA-EN", model_id),
                    fields = [row[0], row[1], row[2]],
                )
            )

    deck = genanki.Deck(model_id, name or Path(file).stem)
    package = genanki.Package(deck)

    for note in tqdm(**progressbar_options(notes, f"Convert ID={model_id}", 'note', disable=verbose)):
        deck.add_note(note)

    deck_name = Path(dest).joinpath(f"{deck.name}.apkg")
    package.write_to_file(deck_name)

    utils.print_on_success(f"Created {str(deck_name.name)!r} with {len(deck.notes)} new cards in {str(deck_name.parent)!r}.", verbose)

    return model_id
