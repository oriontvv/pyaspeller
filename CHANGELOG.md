# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]


## [2.0.1] - 2024-12-29
### Added
- Add python 3.11, 3.12, 3.13 to ci, drop support until 3.9
- Migrate from poetry to uv


## [2.0.0] - 2023-11-19
### Removed
- [Breaking change] Remove deprecated options `flag_latin`, `ignore_latin`, `by_words`, `ignore_roman_numerals` and `ignore_uppercase`
### Changed
- Updated ruff linter version


## [1.2.0] - 2023-07-31
### Added
- Linting with ruff
### Fixed
- Fix encoding issue on windows
### Changed
- Require python3.7+
### Removed
- Linting with flake8
- Linting with black
- Linting with isort


## [1.1.0] - 2023-02-07
### Added
- Add new methods `spell_text` and `spelled_text` for explicit deal with strings only
- Allow to recieve Pathlib.Path argument
- Increase test coverage


## [1.0.0] - 2022-12-08
### Added
- Using keep changelog format
### Changed
- Update and untie dependencies
### Removed
- Drop python3.6 from ci


## [0.2.3] - 2022-02-01
### Added
- Add python3.10 support
- Add mypy
- Add flake8
- Add poetry
### Changed
- Migrate to pyproject.toml


## [0.2.0] - 2020-12-26
### Added
- Added methods spelled, spell_path to Speller class
### Changed
- Use default format `plain`
- Rewrite unittests to pytest
- Updated example
### Removed
- Drop python2 support


## [0.1.0] - 2016-03-03
### Added
- Add python2.7 support
- Add Word quick spell class
- Testing and coverage with pytest
- Testing with tox
- Project health by landscape.io
- Add requirements status, python versions badges in readme
- Add restrictions link in readme
- Add tests, increase coverage


## [0.0.5] - 2015-10-04
### Added
- Wheel packaging


## [0.0.4] - 2015-10-08
### Added
- System script -pyaspeller-
- Packet classifiers updated
- Alpha status specified
- Contributors files added


## [0.0.3] - 2015-09-31
### Added
- Uploaded to pypi.
- Test coverage increased.
- Pretty YandexSpeller API
- Spell checking of strings with parameters.


## [0.0.2] - 2015-09-23
### Added
- Testing automated
- Coverage setup
- Basic functionality. Spell checking for strings
