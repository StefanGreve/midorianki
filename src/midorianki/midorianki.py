#!/usr/bin/env python3

"""
CLI for transforming CSV fi
les from Midori to into APKG decks.
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
from typing import Dict, Union

import genanki
from tqdm import tqdm

from . import utils, config

def progressbar_options(iterable, desc, unit, color=config.GREEN, char='\u25CB', disable=False) -> dict:
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

def export(file: Union[str, Path], name: str, dest: Union[str, Path], verbose: bool=False) -> int:
    """
    Converts CSV files into APKG decks. Expects all fields in the CSV file to
    follow the order of `kanji,kana,meaning`.
    """

    notes = []
    model_id = random.randrange(1 << 30, 1 << 31)
    name = name or Path(file).stem

    utils.print_on_info(f"Model ID: {model_id}", verbose)
    utils.print_on_info(f"Deck Name: {name}", verbose)
    utils.print_on_info("Generating model for notes... ", verbose, end='')

    with open(file, mode='r', encoding="utf-8") as file_handler:
        reader = csv.reader(file_handler)
        for row in reader:
            notes.append(
                genanki.Note(
                    model = generate_model("JA-EN", model_id),
                    fields = [ row[0], row[1], row[2] ],
                )
            )

    if verbose: print("Done!")

    deck = genanki.Deck(model_id, name)
    package = genanki.Package(deck)

    for note in tqdm(**progressbar_options(notes, f"Convert {name}", 'note', disable=verbose)):
        deck.add_note(note)

    package.write_to_file(Path(dest).joinpath(f"{name}.apkg"))

    utils.print_on_success(f"Created '{name}.apkg' containing {len(deck.notes)} new cards in {str(dest)!r}.", verbose)

    return model_id
