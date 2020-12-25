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
    if isinstance(text, (list, tuple)):
        content = ','.join(text)

    elif text.startswith(('http://', 'https://')):
        content = requests.get(text)

    elif isinstance(text, str):
        content = text

    else:
        raise BadArgumentError(f"Unsupported type for {text}")

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
        content = _get_content(text)
        for change in self._spell_text(content):
            yield change

    def spelled(self, text: str) -> str:
        """
        Runs spell checking for text and returns result as string

        >>> result = speller.spelled("tesst message")
        >>> assert result == 'test message'
        """
        changes = {change['word']: change['s'][0]
                   for change in self.spell(text)}
        for word, suggestion in changes.items():
            text = text.replace(word, suggestion)
        return text

    def spell_path(self, path: str) -> None:
        """
            Traverse through path and apply spelling
        """
        if not os.path.exists(path):
            logging.warning("Path not found: '%s'", path)
            return

        if os.path.isfile(path):
            self._spell_file(path)
            return

        for root, _, fnames in os.walk(path):
            for fname in fnames:
                fullpath = os.path.join(root, fname)
                self._spell_file(fullpath)

    def _spell_text(self, text: str) -> Iterable[dict]:
        raise NotImplementedError()

    def _spell_file(self, path: str) -> None:
        with open(path) as infile:
            content = infile.read()
            updated = self.spelled(content)

        with open(path, 'w') as outfile:
            outfile.write(updated)
