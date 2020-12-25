"""
Contains definitions of spellers
"""

import os
import logging
from typing import Iterable

import requests

from .errors import BadArgumentError


_subs = {
    '\r\n': '\n',  # Fix Windows
    '\r': '\n',  # Fix MacOS
    '\n+': '\n',  # Repeat line ends
}


def _prepare_text(text):
    for src, dst in _subs.items():
        text = text.replace(src, dst)
    return text.strip()


def _get_content(text: str) -> str:
    if not isinstance(text, str):
        raise BadArgumentError(f"Unsupported type for {text}")

    if text.startswith(('http://', 'https://')):
        content = requests.get(text)
    else:
        content = text

    return _prepare_text(content)


class Speller:
    """
    Base spell class. Implements spelling logic for files.
    """

    def spell(self, text: str) -> Iterable[object]:
        """
        Runs spell checking for text or URI and yields suggestions for changes

        >>> spelled = speller.spell("42 is a cool maagic namber")
        >>> for p in spelled: print(p)
        {'code': 1, 'pos': 12, 'row': 0, 'col': 12, 'len': 6,
            'word': 'maagic', 's': ['magic']}
        {'code': 1, 'pos': 19, 'row': 0, 'col': 19, 'len': 6,
            'word': 'namber', 's': ['number']}

        """
        yield from self._spell(text, apply=False)

    def _spell(self, text: str, apply=False) -> Iterable[object]:
        if isinstance(text, str) and os.path.exists(text):
            self.spell_path(text, apply)
            return

        content = _get_content(text)
        for change in self._spell_text(content):
            yield change

    def spelled(self, text: str) -> str:
        """
        Runs spell checking and apply suggestions

        >>> result = speller.spelled("tesst message")
        >>> assert result == 'test message'
        """
        for change in self._spell(text, apply=True):
            if change['s']:
                word = change['word']
                suggestion = change['s'][0]
                text = text.replace(word, suggestion)
        return text

    def spell_path(self, path: str, apply: bool) -> None:
        """
            Traverse through path and apply spelling
        """
        if not os.path.exists(path):
            logging.warning("Path not found: '%s'", path)
            return

        if os.path.isfile(path):
            self._spell_file(path, apply)
            return

        for root, _, fnames in os.walk(path):
            for fname in fnames:
                fullpath = os.path.join(root, fname)
                self._spell_file(fullpath, apply)

    def _spell_text(self, text: str) -> Iterable[dict]:
        raise NotImplementedError()

    def _spell_file(self, path: str, apply: bool) -> None:
        with open(path) as infile:
            content = infile.read()
            updated = self.spelled(content)

        if apply:
            with open(path, 'w') as outfile:
                outfile.write(updated)
        else:
            print(path + ": ")
            print(updated)
