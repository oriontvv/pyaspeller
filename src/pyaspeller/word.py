"""
Contains definitions of Word class
"""

from __future__ import annotations
import warnings

from pyaspeller.errors import BadArgumentError
from pyaspeller.yandex_speller import YandexSpeller


class Word:
    """
    Class for spelling of single word.
    """

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002 ANN003
        warnings.warn("Class Word is deprecated. Use YandexSpeller().spelled(text) instead")
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
    def answer(self) -> list[dict]:
        if self._answer is None:
            self._answer = self._spell_text(self.text)
        return self._answer  # type: ignore

    @property
    def correct(self) -> bool:
        return not self.answer

    @property
    def variants(self) -> list[str] | None:
        answer = self.answer
        if not answer:
            return None
        return answer[0]["s"]

    @property
    def spellsafe(self) -> str | None:
        variants = self.variants
        if not variants:
            return None
        return variants[0]
