<h1 align="center">MidoriAnki</h1>

<p align="center">
    <a href="https://github.com/StefanGreve/midorianki/actions/workflows/python-app.yml" title="Continuous Integration" target="_blank">
        <img src="https://github.com/StefanGreve/midorianki/actions/workflows/python-app.yml/badge.svg">
    </a>
    <a href="https://github.com/StefanGreve/midorianki/actions/workflows/codeql-analysis.yml" title="CodeQL Analysis" target="_blank">
        <img src="https://github.com/StefanGreve/midorianki/actions/workflows/codeql-analysis.yml/badge.svg">
    </a>
    <a href="https://github.com/StefanGreve/midorianki" title="Release Version">
        <img src="https://img.shields.io/badge/Release-4.0.0-blue">
    </a>
    <a title="Supported Python Versions">
        <img src="https://img.shields.io/badge/Python-3.11%20--%203.14-blue">
    </a>
    <a href="https://www.gnu.org/licenses/gpl-3.0.en.html" title="License Information" target="_blank" rel="noopener noreferrer">
        <img src="https://img.shields.io/badge/License-GPLv3-blue.svg">
    </a>
</p>

This project is a CLI that converts CSV files from
[Midori](https://apps.apple.com/us/app/midori-japanese-dictionary/id385231773)
into [Anki](https://apps.ankiweb.net/) APKG decks. You can also use your own CSV
files as long as they follow the `kanji,kana,meaning` convention mandated by the
`midorianki` application.

## Screenshot

![Screenshot](https://raw.githubusercontent.com/StefanGreve/midorianki/abb402bd031616eb0051dc7f1199d18aa6f2e89b/samples/screenshot.png)

## Installation

Follow the installation steps below to set up this terminal application. See also
`pyproject.toml` to examine the dependency graph.

[`uv`](https://docs.astral.sh/uv/) is the recommended way to install this
Python application in an isolated environment:

```bash
uv tool install git+https://github.com/StefanGreve/midorianki.git
```

Once installed, run it directly with `midorianki <args>`.

## Basic Usage

Get help:

```bash
midorianki --help
```

Create a new Anki deck:

```bash
midorianki convert --path <csv> [--name <string>] [--dest <path>]
```

The deck name defaults to `csv`'s file stem if `--name` is not specified.
The default target directory is always the current working directory.

Pass `--no-verbose` before the command to silence status output (errors are still
reported); it is a global flag, so it must precede the subcommand:

```bash
midorianki --no-verbose convert --path <csv>
```

Install shell completion for your shell (bash, zsh, fish, or PowerShell) with:

```bash
midorianki --install-completion
```

Or print the completion script to stdout and place it yourself by using the
`--show-completion` flag.

The `import` command pushes an existing `.apkg` deck straight into your local
Anki collection via [AnkiConnect](https://ankiweb.net/shared/info/2055492159),
from where Anki's own sync carries it to AnkiWeb.

```bash
midorianki import --path ./deck_title.apkg
```

The deck lands under the name baked into the `.apkg`; use `convert --name` to set
that name beforehand. Pass `--host`/`--port` if AnkiConnect does not listen on the
default `127.0.0.1:8765`.

> [!IMPORTANT]
> In order to use the `import` command, you need the `AnkiConnect` add-on. To install it, navigate to
> `Tools > Add-ons`, click `Get Add-ons...` and enter the code `2055492159`. Afterwards, restart Anki.
> Anki must be running whenever you import a deck.

### Example

```bash
# download a test file
curl https://gist.githubusercontent.com/StefanGreve/5d8d3111eb4e29bbce691f6ef2ebb656/raw/4a8b081086fa4174b64c6f86be33fb07fa36590f/kaze-no-uta-wo-kike.csv --output test.csv

# creates a deck_title.apkg file in the home directory
midorianki convert --path ./test.csv --name "deck_title" --dest $HOME
# import the deck into Anki
midorianki import --path $HOME/deck_title.apkg
```

## Developer Notes

Set up a development environment with `uv`, which creates a managed virtual
environment and installs the runtime and dev dependencies:

```bash
git clone https://github.com/StefanGreve/midorianki.git
cd midorianki/
uv sync --all-groups
```

Run the application from this environment with `uv run midorianki <args>`.

Public functions are documented with
[Google-style docstrings](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings). [`ruff`](https://docs.astral.sh/ruff/) enforces linting (including the docstring convention) and formatting; its configuration lives in `pyproject.toml`. Run the
checks from the development environment:

```bash
uv run ruff check       # lint
uv run ruff format      # apply formatting (--check to verify only)
```
