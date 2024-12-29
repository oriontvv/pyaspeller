"""
Contains definitions of spellers.
"""

from __future__ import annotations
import logging
import os
from typing import Iterable, Union
from pathlib import Path

import requests

from pyaspeller.errors import BadArgumentError, EncodingError

_subs = {
    "\r\n": "\n",  # Fix Windows
    "\r": "\n",  # Fix MacOS
    "\n+": "\n",  # Repeat line ends
}


def _prepare_text(text: str) -> str:
    for src, dst in _subs.items():
        text = text.replace(src, dst)
    return text.strip()


def _fetch_content(text: str) -> str:
    content = requests.get(text).text
    return _prepare_text(content)


def is_url(text: str) -> bool:
    return text.startswith(("http://", "https://"))


def is_path(path: Union[str, Path]) -> bool:
    return os.path.exists(path)


class Speller:
    """
    Base spell class. Implements spelling logic for files.

    Parameters:
        :: encoding: encoding to use for opening and saving files
    """

    encoding: str | None = None

    def spell(self, text: str) -> Iterable[object]:
        """
        Runs spell checking for text or URI and yields suggestions for changes.

        >>> spelled = speller.spell("42 is a cool maagic namber")
        >>> for p in spelled: print(p)
        {'code': 1, 'pos': 12, 'row': 0, 'col': 12, 'len': 6,
            'word': 'maagic', 's': ['magic']}
        {'code': 1, 'pos': 19, 'row': 0, 'col': 19, 'len': 6,
            'word': 'namber', 's': ['number']}

        """
        if not isinstance(text, (str, Path)):
            raise BadArgumentError(f"Unsupported type for {text}")

        if is_path(text):
            self.spell_path(text, apply=False)
            return

        if is_url(text):
            content = _fetch_content(text)
            yield from self._spell_text(content)

        else:
            yield from self._spell_text(text)

    def spelled(self, text: str) -> str:
        """
        Runs spell checking and apply suggestions.

        >>> result = speller.spelled("tesst message")
        >>> assert result == 'test message'
        """
        if not isinstance(text, (str, Path)):
            raise BadArgumentError(f"Unsupported type for {text}")

        if is_path(text):
            self.spell_path(text, apply=True)
            return ""

        if is_url(text):
            content = _fetch_content(text)
        else:
            content = text

        changes = self._spell_text(content)
        return self._apply_suggestion(content, changes)

    def spell_path(self, path: str, apply: bool) -> None:
        """
        Traverse through path and apply spelling
        """
        if not os.path.exists(path):
            logging.warning("Path not found: '%s'", path)
            return

        if os.path.isfile(path):
            # iterate over changes
            list(self._spell_file(path, apply))
            return

        for root, _, fnames in os.walk(path):
            for fname in fnames:
                fullpath = os.path.join(root, fname)
                # iterate over changes
                list(self._spell_file(fullpath, apply))

    def spell_url(self, url: str) -> str:
        """
        Run spell checking for url.
        """
        content = _fetch_content(url)
        changes = self._spell_text(content)
        return self._apply_suggestion(content, changes)

    def spelled_text(self, text: str) -> str:
        """
        Run spell checking and apply suggestions for text.
        """
        changes = self._spell_text(text)
        return self._apply_suggestion(text, changes)

    def spell_text(self, text: str) -> list[dict]:
        """
        Run spell checking for text.
        """
        return self._spell_text(text)

    def _spell_text(self, text: str) -> list[dict]:
        raise NotImplementedError()

    def _apply_suggestion(self, text: str, changes: Iterable[dict]) -> str:
        raise NotImplementedError()

    def _spell_file(self, path: str, apply: bool) -> Iterable[dict]:
        with open(path, encoding=self.encoding) as infile:
            try:
                content = infile.read()
            except UnicodeDecodeError as e:
                raise EncodingError(
                    "Encoding of the source file differs from the one was set. Please check encoding."
                ) from e

            changes = self._spell_text(content)

            if apply:
                updated = self._apply_suggestion(content, changes)
                with open(path, "w", encoding=self.encoding) as outfile:
                    outfile.write(updated)
            else:
                yield from changes
