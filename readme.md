<h1 align="center">MidoriAnki</h1>

<p align="center">
    <a href="https://github.com/StefanGreve/midorianki/actions/workflows/python-app.yml" title="Continuous Integration" target="_blank">
        <img src="https://github.com/StefanGreve/midorianki/actions/workflows/python-app.yml/badge.svg">
    </a>
    <a href="https://github.com/StefanGreve/midorianki/actions/workflows/codeql-analysis.yml" title="Code QL Analysis" target="_blank">
        <img src="https://github.com/StefanGreve/midorianki/actions/workflows/codeql-analysis.yml/badge.svg">
    </a>
    <a href="https://github.com/StefanGreve/midorianki" title="Release Version">
        <img src="https://img.shields.io/badge/Release-3.1.0%20-blue">
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
files as long they follow the `kanji,kana,meaning` convention mandated by the
`midorianki` application.

## Screenshot

![Screenshot](https://raw.githubusercontent.com/StefanGreve/midorianki/abb402bd031616eb0051dc7f1199d18aa6f2e89b/samples/screenshot.png)

## Setup

Follow along the setup guide below to install this terminal application. See also
`pyproject.toml` to examine the dependency graph.

<details>
<summary>Installation</summary>

[`uv`](https://docs.astral.sh/uv/) is the recommended way to install this
Python application in an isolated environment:

```bash
uv tool install git+https://github.com/StefanGreve/midorianki.git
```

Set up a development environment with `uv`, which creates a managed virtual
environment and installs the runtime and dev dependencies:

```bash
git clone https://github.com/StefanGreve/midorianki.git
cd midorianki/
uv sync --all-groups
```

Run the application from the development environment with `uv run midorianki`.

</details>

## Basic Usage

<details>
<summary>Command Line Usage</summary>

Get help:

```cli
midorianki --help
```

Create a new Anki deck:

```cli
midorianki convert --file <csv> [--name <string>|--dest <path>]
```

The deck name defaults to `csv`'s file stem if `--name` is not specified.
The default target directory is always the current working directory.

### Example

```bash
curl https://gist.githubusercontent.com/StefanGreve/5d8d3111eb4e29bbce691f6ef2ebb656/raw/4a8b081086fa4174b64c6f86be33fb07fa36590f/kaze-no-uta-wo-kike.csv --output test.csv
# creates a deck_title.apkg file in the home directory
midorianki convert --file ./test.csv --name "deck_title" --dest $HOME
```

</details>

## Developer Notes

Public functions are documented with
[Google-style docstrings](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings).

[`ruff`](https://docs.astral.sh/ruff/) enforces linting (including the docstring
convention) and formatting; its configuration lives in `pyproject.toml`. Run the
checks from the development environment:

```bash
uv run ruff check       # lint
uv run ruff format      # apply formatting (--check to verify only)
```
