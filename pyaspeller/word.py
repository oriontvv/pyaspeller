"""
Contains definitions of Word class
"""
from typing import Optional
import warnings

from .yandex_speller import YandexSpeller
from .errors import BadArgumentError


class Word:
    """
    Class for spelling of single word.
    """

    def __init__(self, *args, **kwargs):
        warnings.warn("Class Word is deprecated. Use Speller().spelled(text)")
        if 'text' in kwargs:
            text = kwargs.pop('text')
        else:
            text = args[0]

        if len(text.split()) > 1:
            msg = 'Bad argument. Multiple words were detected.'
            raise BadArgumentError(msg)

        self._spell_text = YandexSpeller(*args[1:], **kwargs)._spell_text

        self.text = text
        self._answer = None

    @property
    def answer(self):
        if self._answer is None:
            self._answer = self._spell_text(self.text)
        return self._answer

    @property
    def correct(self) -> bool:
        return not self.answer

    @property
    def variants(self) -> Optional[str]:
        if self.correct:
            return None
        return self.answer[0]['s']

    @property
    def spellsafe(self) -> Optional[str]:
        if self.correct:
            return None
        try:
            return self.variants[0]
        except IndexError:
            return None
