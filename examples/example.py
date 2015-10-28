from __future__ import print_function
import pyaspeller


def spelled(text):
    speller = pyaspeller.YandexSpeller(lang='en', find_repeat_words=False,
                                       ignore_digits=True)
    return speller.spell(text)

if __name__ == "__main__":
    spelled("42 is a cUl maagic namber")
