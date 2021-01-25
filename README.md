# Python text speller

[![CI](https://github.com/oriontvv/pyaspeller/workflows/Python%20package/badge.svg)](https://github.com/oriontvv/pyaspeller/actions)       [![Coverage Status](https://img.shields.io/coveralls/oriontvv/pyaspeller.svg)](https://coveralls.io/r/oriontvv/pyaspeller)         [![CodeQuality](https://codeclimate.com/github/oriontvv/pyaspeller/badges/gpa.svg)](https://codeclimate.com/github/oriontvv/pyaspeller)          [![Requirements Status](https://requires.io/github/oriontvv/pyaspeller/requirements.svg?branch=master)](https://requires.io/github/oriontvv/pyaspeller/requirements/?branch=master)


[![Pypi](http://img.shields.io/pypi/v/pyaspeller.svg?style=flat)](https://pypi.org/project/pyaspeller)     [![PyVersions](https://img.shields.io/pypi/pyversions/pyaspeller.svg)](https://img.shields.io/pypi/pyversions/pyaspeller.svg)


[pyaspeller](https://github.com/oriontvv/pyaspeller) (Python Yandex Speller) is a search tool typos in the text, files and websites.

Used [Yandex.Speller API](https://tech.yandex.ru/speller/doc/dg/concepts/About-docpage/). ([restrictions](<https://yandex.ru/legal/speller_api/>))


## Features

You can correct your local files

```bash 
$ pyaspeller ./doc
$ pyaspeller "в суббботу утромъ"
в субботу утром
```

If you want to check a text you can use:

```python
>>> from pyaspeller import YandexSpeller
>>> speller = YandexSpeller()
>>> fixed = speller.spelled('В суббботу утромь.')
>>> fixed
'В субботу утром.'
```

You can use class `Word` for single word queries:

```python
>>> from pyaspeller import Word
>>> check = Word('tesst')
>>> check.correct
False
>>> check.variants
[u'test']
>>> check.spellsafe
u'test'
```


## Installation


To install `pyaspeller`, simply do:

```bash
$ python3 -m pip install pyaspeller
$ pyaspeller --help
```

If you're stil using version for python2 you can use outdated version:
```bash
pip install pyaspeller==0.1.0
```

## Thanks to
* Dependencies scanned by [PyUp.io](https://pyup.io/)
