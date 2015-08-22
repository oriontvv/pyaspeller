import os
import logging


class Speller(object):
    """
    Spell class.
    """
    def __init__(self, options):
        self._options = options

    def spell(self, target):
        if target.startswith(('http://', 'https://')):
            return self._spell_url(target)

        if os.path.exists(target):
            return self._spell_path(target)

        self._spell_text(target)

    def _spell_text(self, text):
        logging.info("spelling text: " + text)

    def _spell_url(self, url):
        logging.info("spelling url: " + url)

    def _spell_path(self, path):
        logging.info("spelling path: " + path)
