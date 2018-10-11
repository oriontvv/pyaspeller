from __future__ import print_function

import collections
import os
import logging
import re
import requests

from .errors import BadArgumentError


class Speller(object):
    """
    Base spell class. Implements spelling logic for files.
    """

    def spell(self, text):
        if isinstance(text, (list, tuple)):
            text = ','.join(text)

        text = self._prepare_text(text)

        if text.startswith(('http://', 'https://')):
            yield self._spell_url(text)

        elif os.path.exists(text):
            for item in self._spell_path(text):
                yield item

        elif text:
            for item in self._spell_text(text):
                yield item

        else:
            raise NotImplementedError()

    def _spell_text(self, text):
        logging.info("spelling text: " + text)
        return NotImplemented

    def _spell_url(self, url):
        logging.info("spelling url: " + url)
        content = requests.get(url)
        for item in self._spell_text(content):
            yield item

    def _spell_file(self, path):
        with open(path) as f:
            content = f.read()
            for item in self._spell_text(content):
                yield item

    def _spell_path(self, path):
        logging.info("spelling path: " + path)
        if os.path.isfile(path):
            yield self._spell_file(path)
        else:
            for root, dirs, fnames in os.walk(path):
                for fname in fnames:
                    fullpath = os.path.join(root, fname)
                    print(fullpath, end=': ')
                    for res in self._spell_file(fullpath):
                        yield res

    def _prepare_text(self, text):
        subs = {
            '\r\n': '\n',  # Fix Windows
            '\r': '\n',  # Fix MacOS
            '\s+\n': '\n',  # Trailing spaces
            '\s+': ' ',  # Repeat spaces
            '\n+': '\n',  # Repeat line ends
        }
        for src, dst in subs.items():
            text = text.replace(src, dst)
        return text.strip()

    def _strip_tags(self, text):
        return re.sub('<[^<]+?>', '', text)


class YandexSpeller(Speller):
    """
    Yandex speller implementation.
    """
    _supported_langs = {'en', 'ru', 'uk'}

    def __init__(self, format_text=None, lang=None, config_path=None,
                 dictionary=None, report_type=None, max_requests=2,
                 is_debug=False, check_yo=False, ignore_urls=False,
                 ignore_tags=False, ignore_capitalization=False,
                 ignore_digits=False, ignore_latin=False,
                 ignore_roman_numerals=False, ignore_uppercase=False,
                 find_repeat_words=False, flag_latin=False, by_words=False):

        self._lang = ['en', 'ru']
        self.lang = lang
        self._format = format_text
        self._config_path = config_path or ''
        self._dictionary = dictionary or {}
        self._report_type = report_type or 'console'

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

        self._api_query = 'https://speller.yandex.net/services/' \
                          'spellservice.json/checkText'

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
        elif isinstance(language, collections.Iterable):
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
        self._config_path = value or ''
        if not isinstance(self._config_path, str):
            raise BadArgumentError("config_path must be string: {}".format(
                self._config_path))

    @property
    def dictionary(self):
        """Get dictionary"""
        return self._dictionary

    @dictionary.setter
    def dictionary(self, value):
        """Set dictionary"""
        self._dictionary = value or {}
        if not isinstance(self._dictionary, dict):
            raise BadArgumentError("dictionary must be dict: {}".format(
                self._dictionary))

    @property
    def report_type(self):
        """Get report_type"""
        return self._report_type

    @report_type.setter
    def report_type(self, value):
        """Set report_type"""
        self._report_type = value or 'console'

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

    def _spell_text(self, text):
        lang = ','.join(self._lang)
        data = {
            'text': text,
            'options': self.api_options,
            'lang': lang,
        }
        if self.format:
            data['format'] = self.format
        response = requests.post(url=self._api_query, data=data).json()
        logging.debug('{}?{}'.format(
            self._api_query, requests.compat.urlencode(data)))
        logging.debug("response: " + str(response))
        return response

    @property
    def api_options(self):
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


class Word(object):
    """
    Class for quick spelling of single word.
    """

    def __init__(self, *args, **kwargs):
        if 'text' in kwargs:
            text = kwargs.pop('text')
        else:
            text = args[0]
        super(Word, self).__init__(*args[1:], **kwargs)

        if len(text.split()) > 1:
            raise BadArgumentError('Bad argument. Several words detected.')

        self._spell_text = YandexSpeller(*args[1:], **kwargs)._spell_text
        self.text = text
        self._answer = None

    @property
    def answer(self):
        if self._answer is None:
            self._answer = self._spell_text(self.text)
        return self._answer

    @property
    def correct(self):
        return not self.answer

    @property
    def variants(self):
        if self.correct:
            return
        return self.answer[0]['s']

    @property
    def spellsafe(self):
        if self.correct:
            return
        try:
            return self.variants[0]
        except IndexError:
            return
