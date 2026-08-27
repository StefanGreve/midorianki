#!/usr/bin/env python3

"""Command-line entry point for the midorianki application."""

from .cli import app


def main() -> None:
    """Run the Typer application."""
    app()


if __name__ == "__main__":
    main()
