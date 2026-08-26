# Changelog

## Version 3.1.0 (Unreleased)

### Added

- Support for Python 3.12, 3.13, and 3.14.

### Changed

- Migrated the build system from `setup.py` (setuptools) to a `pyproject.toml`-based build using the
  `hatchling` backend, managed with [`uv`](https://docs.astral.sh/uv/).
- Consolidated the runtime and development dependencies from `requirements/*.txt` into
  `pyproject.toml`.

### Removed

- `setup.py`, `MANIFEST.in`, and the `requirements/*.txt` files, superseded by `pyproject.toml`.

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
