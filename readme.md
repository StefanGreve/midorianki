# Midori Anki

## About

This script converts from [Midori](https://apps.apple.com/us/app/midori-japanese-dictionary/id385231773) exported CSV files into [Anki](https://apps.ankiweb.net/) decks. You can also use any other CSV files that follows the  `kanji,kana,meaning` convention.

## Screenshot

![Screenshot](https://github.com/StefanGreve/midori-anki/blob/master/samples/screenshot.png "Screenshot")

## Installation

Install as script.

```bash
    # install file dependencies
    python -m venv venv/
    python -m pip install --user -r requirements.txt
```

Or build project from source if you want to use this script from any directory in your terminal:

```bash
    # enter project root, check wheel installation
    python -m pip install --user wheel
    # build wheel and install midorianki
    python setup.py bdist_wheel
    python -m pip install -e .
```

## Usage

```powershell
    # show help message
    # run as file
    python midorianki.py --help
    # or as module if you build the wheel before
    python -m midorianki --help
```

Deck name and title default to `--file` stem if `--name` is not explicitly specified in the command prompt; the default target directory is the current working directory.

```powershell
    # create new deck, path to csv file resolves relative to cwd
    python -m midorianki --file 'path/to/file.csv'
```

```powershell
    # specify target directory
    $DesktopPath = [Environment]::GetFolderPath("Desktop")
    python -m midorianki --file 'path/to/file.csv' --name 'Deck Title' --dest $DesktopPath
```
