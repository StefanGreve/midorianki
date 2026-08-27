#!/usr/bin/env python3

"""
Tool for converting CSV files from Midori into APKG decks.

Copyright (C) 2020-2026 Stefan Greve (stefan.ohlsen.greve@gmail.com)

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

import csv
import logging
import random
from pathlib import Path

import genanki
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)

_LOGGER = logging.getLogger(__name__)


def generate_model(model_name: str, model_id: int) -> genanki.Model:
    """
    Build the genanki model that defines the note template for a deck.

    Expects all fields to follow the order of ``kanji,kana,meaning``.

    Args:
        model_name: Human-readable name of the model (e.g. ``"JA-EN"``).
        model_id: Numeric identifier assigned to the generated model.

    Returns:
        The configured genanki model.
    """
    return genanki.Model(
        model_id,
        model_name,
        fields=[{"name": "kanji"}, {"name": "kana"}, {"name": "meaning"}],
        templates=[
            {
                "name": "Forward Card Template",
                "qfmt": '<strong style="font-family: Meiryo; font-size: 60px;">{{kanji}}</strong>',
                "afmt": '{{FrontSide}}<hr id="answer"><span style="font-family: Meiryo; font-size: 30px;">{{kana}}</span><br><strong style="font-size: 40px;">{{meaning}}</strong>',
            },
            {
                "name": "Backward Card Template",
                "qfmt": '<strong style="font-size: 40px;">{{meaning}}</strong>',
                "afmt": '{{FrontSide}}<hr id="answer"><strong style="font-family: Meiryo; font-size: 60px">{{kanji}}</strong><br><span style="font-family: Meiryo; font-size: 30px;">{{kana}}</span>',
            },
        ],
        css="""
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
            """,
    )


def export(
    file: str | Path, name: str, dest: str | Path, verbose: bool = False, logger: logging.Logger = _LOGGER
) -> int:
    """
    Convert a Midori CSV file into an APKG deck.

    Expects all fields in the CSV file to follow the order of
    ``kanji,kana,meaning``.

    Args:
        file: Path to the source CSV file.
        name: Deck title and output filename stem; falls back to the CSV file
            stem when falsy.
        dest: Directory in which the ``.apkg`` file is written.
        verbose: When ``True``, display the conversion progress bar.
        logger: Logger used to report completion; defaults to this module's
            logger, whose records propagate to the configured package logger.

    Returns:
        The randomly generated model id.
    """
    notes = []
    model_id = random.randrange(1 << 30, 1 << 31)

    with open(file, encoding="utf-8") as file_handler:
        reader = csv.reader(file_handler)
        for row in reader:
            notes.append(
                genanki.Note(
                    model=generate_model("JA-EN", model_id),
                    fields=[row[0], row[1], row[2]],
                )
            )

    deck = genanki.Deck(model_id, name or Path(file).stem)
    package = genanki.Package(deck)

    with Progress(
        TextColumn("[bold blue]ID={task.fields[model_id]}"),
        BarColumn(),
        TaskProgressColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        disable=not verbose,
    ) as progress:
        if verbose:
            progress.console.print(f"[bold]Convert {str(file)!r}[/]")
        task = progress.add_task("", total=len(notes), model_id=model_id)
        for note in notes:
            deck.add_note(note)
            progress.advance(task)

    deck_name = Path(dest) / f"{deck.name}.apkg"
    package.write_to_file(deck_name)

    logger.info(f"Created {str(deck_name.name)!r} with {len(deck.notes)} new cards in {str(deck_name.parent)!r}.")

    return model_id
