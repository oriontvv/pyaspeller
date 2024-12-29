"""
Contains specific details for Yandex speller
"""

from __future__ import annotations
import collections
import logging
from typing import Iterable
from urllib.parse import urlencode

import requests

from pyaspeller.errors import BadArgumentError
from pyaspeller.speller import Speller


class YandexSpeller(Speller):
    """
    Yandex speller implementation.
    """

    _supported_langs = ["en", "ru", "uk"]

    def __init__(
        self,
        format_text: str | None = None,
        lang: str | list[str] | None = None,
        config_path: str | None = None,
        dictionary: dict | None = None,
        report_type: str | None = None,
        max_requests: int = 2,
        is_debug: bool = False,
        check_yo: bool = False,
        ignore_urls: bool = False,
        ignore_tags: bool = False,
        ignore_capitalization: bool = False,
        ignore_digits: bool = False,
        find_repeat_words: bool = False,
        encoding: str | None = None,
    ) -> None:
        self._lang: list[str] = []
        self.lang = lang or self._supported_langs  # type: ignore

        if format_text == "auto" or not format_text:
            self._format = "plain"
        else:
            self._format = format_text
        self._config_path = config_path or ""
        self._dictionary = dictionary or {}
        self._report_type = report_type or "console"

        self._check_yo = check_yo
        self._ignore_urls = ignore_urls
        self._ignore_tags = ignore_tags
        self._ignore_capitalization = ignore_capitalization
        self._ignore_digits = ignore_digits
        self._find_repeat_words = find_repeat_words
        self._max_requests = max_requests
        self._is_debug = is_debug

        self._api_query = "https://speller.yandex.net/services/spellservice.json/checkText"
        self.encoding = encoding

    @property
    def format(self) -> str:
        """Get format"""
        return self._format

    @format.setter
    def format(self, value: str) -> None:
        """Set format"""
        self._format = value

    @property
    def lang(self) -> list[str]:
        """Get lang"""
        return self._lang

    @lang.setter
    def lang(self, language: str | Iterable[str]) -> None:
        """Set lang"""
        if isinstance(language, str):
            self._lang = [language]
        elif isinstance(language, collections.abc.Iterable):
            self._lang = list(language)

        if any(lang not in self._supported_langs for lang in self._lang):
            raise BadArgumentError("Unsupported language")

    @property
    def config_path(self) -> str:
        """Get config_path"""
        return self._config_path

    @config_path.setter
    def config_path(self, value: str) -> None:
        """Set config_path"""
        self._config_path = value or ""
        if not isinstance(self._config_path, str):
            msg = f"config_path must be a string: {self._config_path}"
            raise BadArgumentError(msg)

    @property
    def dictionary(self) -> dict:
        """Get dictionary"""
        return self._dictionary

    @dictionary.setter
    def dictionary(self, value: dict) -> None:
        """Set dictionary"""
        self._dictionary = value or {}
        if not isinstance(self._dictionary, dict):
            msg = f"dictionary must be a dict: {self._dictionary}"
            raise BadArgumentError(msg)

    @property
    def report_type(self) -> str:
        """Get report_type"""
        return self._report_type

    @report_type.setter
    def report_type(self, value: str) -> None:
        """Set report_type"""
        self._report_type = value or "console"

    @property
    def check_yo(self) -> bool:
        """Get check_yo"""
        return self._check_yo

    @check_yo.setter
    def check_yo(self, value: bool) -> None:
        """Set check_yo"""
        self._check_yo = value

    @property
    def ignore_urls(self) -> bool:
        """Get ignore_urls"""
        return self._ignore_urls

    @ignore_urls.setter
    def ignore_urls(self, value: bool) -> None:
        """Set ignore_urls"""
        self._ignore_urls = value

    @property
    def ignore_tags(self) -> bool:
        """Get ignore_tags"""
        return self._ignore_tags

    @ignore_tags.setter
    def ignore_tags(self, value: bool) -> None:
        """Set ignore_tags"""
        self._ignore_tags = value

    @property
    def ignore_capitalization(self) -> bool:
        """Get ignore_capitalization"""
        return self._ignore_capitalization

    @ignore_capitalization.setter
    def ignore_capitalization(self, value: bool) -> None:
        """Set ignore_capitalization"""
        self._ignore_capitalization = value

    @property
    def ignore_digits(self) -> bool:
        """Get ignore_digits"""
        return self._ignore_digits

    @ignore_digits.setter
    def ignore_digits(self, value: bool) -> None:
        """Set ignore_digits"""
        self._ignore_digits = value

    @property
    def find_repeat_words(self) -> bool:
        """Get find_repeat_words"""
        return self._find_repeat_words

    @find_repeat_words.setter
    def find_repeat_words(self, value: bool) -> None:
        """Set find_repeat_words"""
        self._find_repeat_words = value

    @property
    def max_requests(self) -> int:
        """Get max_requests"""
        return self._max_requests

    @max_requests.setter
    def max_requests(self, value: int) -> None:
        """Set max_requests"""
        self._max_requests = value

    @property
    def is_debug(self) -> bool:
        """Get is_debug"""
        return self._is_debug

    @is_debug.setter
    def is_debug(self, value: bool) -> None:
        """Set is_debug"""
        self._is_debug = value

    def _spell_text(self, text: str) -> list[dict]:
        lang = ",".join(self._lang)
        data = {
            "text": text,
            "options": self.api_options,
            "lang": lang,
            "format": self.format,
        }
        response = requests.post(url=self._api_query, data=data).json()

        args = urlencode(data)
        logging.debug("%s?%s", self._api_query, args)
        logging.debug("response: %s", response)
        return response

    def _apply_suggestion(self, text: str, changes: Iterable[dict]) -> str:
        for change in changes:
            if change["s"]:
                word = change["word"]
                suggestion = change["s"][0]
                text = text.replace(word, suggestion)
        return text

    @property
    def api_options(self) -> int:
        """
        current spelling settings
        :return: api options as number
        """
        options = 0
        if self._ignore_digits:
            options |= 2
        if self._ignore_urls:
            options |= 4
        if self._find_repeat_words:
            options |= 8
        if self._ignore_capitalization:
            options |= 512
        return options
