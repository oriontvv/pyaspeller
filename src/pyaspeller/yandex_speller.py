"""
Contains specific details for Yandex speller
"""
from __future__ import annotations
import collections
import logging
from typing import Iterable
from urllib.parse import urlencode

import requests

from .errors import BadArgumentError
from .speller import Speller


class YandexSpeller(Speller):
    """
    Yandex speller implementation.
    """

    _supported_langs = {"en", "ru", "uk"}

    def __init__(
        self,
        format_text=None,
        lang=None,
        config_path=None,
        dictionary=None,
        report_type=None,
        max_requests=2,
        is_debug=False,
        check_yo=False,
        ignore_urls=False,
        ignore_tags=False,
        ignore_capitalization=False,
        ignore_digits=False,
        ignore_latin=False,
        ignore_roman_numerals=False,
        ignore_uppercase=False,
        find_repeat_words=False,
        flag_latin=False,
        by_words=False,
    ):

        self._lang = None
        self.lang = lang or self._supported_langs

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
        self._ignore_latin = ignore_latin
        self._ignore_roman_numerals = ignore_roman_numerals
        self._ignore_uppercase = ignore_uppercase
        self._find_repeat_words = find_repeat_words
        self._flag_latin = flag_latin
        self._by_words = by_words

        self._max_requests = max_requests
        self._is_debug = is_debug

        self._api_query = "https://speller.yandex.net/services/spellservice.json/checkText"

    @property
    def format(self):
        """Get format"""
        return self._format

    @format.setter
    def format(self, value):
        """Set format"""
        self._format = value

    @property
    def lang(self):
        """Get lang"""
        return self._lang

    @lang.setter
    def lang(self, language):
        """Set lang"""
        if isinstance(language, str):
            self._lang = [language]
        elif isinstance(language, collections.abc.Iterable):
            self._lang = list(language)

        if any(lang not in self._supported_langs for lang in self._lang):
            raise BadArgumentError("Unsupported language")

    @property
    def config_path(self):
        """Get config_path"""
        return self._config_path

    @config_path.setter
    def config_path(self, value):
        """Set config_path"""
        self._config_path = value or ""
        if not isinstance(self._config_path, str):
            msg = f"config_path must be a string: {self._config_path}"
            raise BadArgumentError(msg)

    @property
    def dictionary(self):
        """Get dictionary"""
        return self._dictionary

    @dictionary.setter
    def dictionary(self, value):
        """Set dictionary"""
        self._dictionary = value or {}
        if not isinstance(self._dictionary, dict):
            msg = f"dictionary must be a dict: {self._dictionary}"
            raise BadArgumentError(msg)

    @property
    def report_type(self):
        """Get report_type"""
        return self._report_type

    @report_type.setter
    def report_type(self, value):
        """Set report_type"""
        self._report_type = value or "console"

    @property
    def check_yo(self):
        """Get check_yo"""
        return self._check_yo

    @check_yo.setter
    def check_yo(self, value):
        """Set check_yo"""
        self._check_yo = value

    @property
    def ignore_urls(self):
        """Get ignore_urls"""
        return self._ignore_urls

    @ignore_urls.setter
    def ignore_urls(self, value):
        """Set ignore_urls"""
        self._ignore_urls = value

    @property
    def ignore_tags(self):
        """Get ignore_tags"""
        return self._ignore_tags

    @ignore_tags.setter
    def ignore_tags(self, value):
        """Set ignore_tags"""
        self._ignore_tags = value

    @property
    def ignore_capitalization(self):
        """Get ignore_capitalization"""
        return self._ignore_capitalization

    @ignore_capitalization.setter
    def ignore_capitalization(self, value):
        """Set ignore_capitalization"""
        self._ignore_capitalization = value

    @property
    def ignore_digits(self):
        """Get ignore_digits"""
        return self._ignore_digits

    @ignore_digits.setter
    def ignore_digits(self, value):
        """Set ignore_digits"""
        self._ignore_digits = value

    @property
    def ignore_latin(self):
        """Get ignore_latin"""
        return self._ignore_latin

    @ignore_latin.setter
    def ignore_latin(self, value):
        """Set ignore_latin"""
        self._ignore_latin = value

    @property
    def ignore_roman_numerals(self):
        """Get ignore_roman_numerals"""
        return self._ignore_roman_numerals

    @ignore_roman_numerals.setter
    def ignore_roman_numerals(self, value):
        """Set ignore_roman_numerals"""
        self._ignore_roman_numerals = value

    @property
    def ignore_uppercase(self):
        """Get ignore_uppercase"""
        return self._ignore_uppercase

    @ignore_uppercase.setter
    def ignore_uppercase(self, value):
        """Set ignore_uppercase"""
        self._ignore_uppercase = value

    @property
    def find_repeat_words(self):
        """Get find_repeat_words"""
        return self._find_repeat_words

    @find_repeat_words.setter
    def find_repeat_words(self, value):
        """Set find_repeat_words"""
        self._find_repeat_words = value

    @property
    def flag_latin(self):
        """Get flag_latin"""
        return self._flag_latin

    @flag_latin.setter
    def flag_latin(self, value):
        """Set flag_latin"""
        self._flag_latin = value

    @property
    def by_words(self):
        """Get by_words"""
        return self._by_words

    @by_words.setter
    def by_words(self, value):
        """Set by_words"""
        self._by_words = value

    @property
    def max_requests(self):
        """Get max_requests"""
        return self._max_requests

    @max_requests.setter
    def max_requests(self, value):
        """Set max_requests"""
        self._max_requests = value

    @property
    def is_debug(self):
        """Get is_debug"""
        return self._is_debug

    @is_debug.setter
    def is_debug(self, value):
        """Set is_debug"""
        self._is_debug = value

    def _spell_text(self, text: str) -> list[dict]:
        lang = ",".join(self._lang)
        data = {"text": text, "options": self.api_options, "lang": lang, "format": self.format}
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
        if self._ignore_uppercase:
            options |= 1
        if self._ignore_digits:
            options |= 2
        if self._ignore_urls:
            options |= 4
        if self._find_repeat_words:
            options |= 8
        if self._ignore_latin:
            options |= 16
        if self._flag_latin:
            options |= 128
        if self._by_words:
            options |= 256
        if self._ignore_capitalization:
            options |= 512
        if self._ignore_roman_numerals:
            options |= 2048
        return options
