"""
Contains definitions of Word class
"""
import warnings
from typing import Optional, Iterable, List, Dict, Any

from .errors import BadArgumentError
from .yandex_speller import YandexSpeller


class Word:
    """
    Class for spelling of single word.
    """

    def __init__(self, *args, **kwargs):
        warnings.warn("Class Word is deprecated. Use Speller().spelled(text) instead")
        if "text" in kwargs:
            text = kwargs.pop("text")
        else:
            text = args[0]

        if len(text.split()) > 1:
            msg = "Bad argument. Multiple words were detected."
            raise BadArgumentError(msg)

        self._spell_text = YandexSpeller(*args[1:], **kwargs)._spell_text

        self.text = text
        self._answer = None

    @property
    def answer(self) -> List[Dict[Any, Any]]:
        if self._answer is None:
            self._answer = self._spell_text(self.text)
        return self._answer

    @property
    def correct(self) -> bool:
        return not self.answer

    @property
    def variants(self) -> Optional[List[str]]:
        answer = self.answer
        if not answer:
            return None
        return answer[0]["s"]

    @property
    def spellsafe(self) -> Optional[str]:
        variants = self.variants
        if not variants:
            return None
        return variants[0]
