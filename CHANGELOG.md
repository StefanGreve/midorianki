# Changelog

## Version 3.1.0 (Unreleased)

### Added

- An `import` command that pushes an existing APKG deck into a running Anki via the
  [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on (code `2055492159`), from where
  Anki's own sync carries it to AnkiWeb.
- Support for Python 3.12, 3.13, and 3.14.
- A `logger` module exposing `init_logger(enable_console_logger)`, which configures the package-root
  logger: the file log (`error.log`) is always written, INFO and WARNING records reach the console
  only when enabled, and errors are always reported to stderr.
- Short, color-highlighted log level names on the console (`DBG`, `INF`, `WRN`, `ERR`, `FTL`),
  rendered as `[ INF ]`.
- [`ruff`](https://docs.astral.sh/ruff/) to the `dev` dependency group for linting and formatting,
  configured in `pyproject.toml` to enforce Google-style docstrings.
- Shell completion for bash, zsh, fish, and PowerShell, provided by `typer`. Install it into the
  current shell with `midorianki --install-completion`, or print the completion script to stdout with
  `midorianki --show-completion` to place it manually.

### Changed

- Migrated the command-line interface from `argparse` to
  [`typer`](https://typer.tiangolo.com/). `--verbose` and `--no-verbose` are now global options that
  apply to every subcommand and must precede it.
- Migrated the build system from `setup.py` (setuptools) to a `pyproject.toml`-based build using the
  `hatchling` backend, managed with [`uv`](https://docs.astral.sh/uv/).
- Consolidated the runtime and development dependencies from `requirements/*.txt` into
  `pyproject.toml`.
- Replaced the `colorama` and `tqdm` dependencies with [`rich`](https://github.com/Textualize/rich)
  for progress bars and terminal output.
- Routed all status and error output through the `rich`-backed logger instead of ad-hoc print helpers.

### Removed

- `setup.py`, `MANIFEST.in`, and the `requirements/*.txt` files, superseded by `pyproject.toml`.
- The `print_on_success`, `print_on_info`, `print_on_warning`, and `print_on_error` helpers, along
  with the module-level `logger`, `shutdown`, and `clear` utilities in `utils`, superseded by the new
  `logger` module.

## Version 3.0.1 (26 Aug 2024)

### Security

- Bump `tqdm` from 4.66.1 to 4.66.3.
- Bump `setuptools` from 68.2.2 to 70.0.0.

## Version 3.0.0 (8 Nov 2023)

Refactors the entire code base to follow current best practices.

## Version 2.0.1 (21 Oct 2021)

### Changed

- Reduced verbose command output.

### Fixed

- Corrected spelling mistakes and minor code style issues.

## Version 2.0.0 (20 Oct 2021)

Rewrites the entire application from scratch by employing a well-tested design pattern, courtesy of
the Advanced Systems organization.
