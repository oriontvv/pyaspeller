from __future__ import print_function
import os
import logging
import re
import six
from six.moves.urllib.parse import quote

import json


def read_url(url):
    assert url, "Empty url"

    if six.PY2:
        import urllib2
        return urllib2.urlopen(url).read()

    if six.PY3:
        import urllib.request
        with urllib.request.urlopen(url) as response:
            return response.read()


class Speller(object):
    """
    Spell class.
    """
    def spell(self, target):
        if target.startswith(('http://', 'https://')):
            yield self._spell_url(target)

        elif os.path.exists(target):
            for res in self._spell_path(target):
                yield res

        elif target:
            yield self._spell_text(target)

        else:
            raise NotImplementedError()

    def _spell_text(self, text):
        logging.info("spelling text: " + text)
        return NotImplemented

    def _spell_url(self, url):
        logging.info("spelling url: " + url)
        content = read_url(url)
        yield self._spell_text(content)

    def _spell_file(self, path):
        with open(path) as f:
            content = f.read()
            yield self._spell_text(content)

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


class YandexSpeller(Speller):

    def __init__(self, options):
        self._options = options
        self._query_template = 'http://speller.yandex.net/services/spellservice.json/' + \
                               'checkText?text={text}&lang={lang}'

    def _spell_text(self, text):

        words = '+'.join(re.findall(r'\w+', text))
        lang = ','.join(self._options.lang)
        query = self._query_template.format(text=quote(words), lang=lang)
        logging.debug("query: " + query)

        responce = read_url(query).decode('utf-8')

        assert responce, "Bad responce for url: " + query
        logging.debug("responce: " + responce)

        responce = json.loads(responce)
        for item in responce:
            yield item
