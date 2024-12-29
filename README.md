# Python text speller

[![CI](https://github.com/oriontvv/pyaspeller/workflows/ci/badge.svg)](https://github.com/oriontvv/pyaspeller/actions)       [![Coverage Status](https://img.shields.io/coveralls/oriontvv/pyaspeller.svg)](https://coveralls.io/r/oriontvv/pyaspeller) [![Pypi](http://img.shields.io/pypi/v/pyaspeller.svg?style=flat)](https://pypi.org/project/pyaspeller)


[pyaspeller](https://github.com/oriontvv/pyaspeller) (Python Yandex Speller) is a cli tool and pure python library for searching typos in texts, files and websites.

Spell checking uses [Yandex.Speller API](https://tech.yandex.ru/speller/doc/dg/concepts/About-docpage/). ([restrictions](<https://yandex.ru/legal/speller_api/>))

## Installation

* Highly recommend to use latest [uv](https://docs.astral.sh/uv/getting-started/installation/)
* `uv add pyaspeller` (for library mode)

## Features

* Command line tool

You can correct your local files or web pages

```bash 
$ uvx pyaspeller ./doc
$ uvx pyaspeller https://team-tricky.github.io
$ uvx pyaspeller "в суббботу утромъ"
в субботу утром
```

* Library 

Use speller for your code

```python
>>> from pyaspeller import YandexSpeller
>>> speller = YandexSpeller()
>>> fixed = speller.spelled('Triky Custle is a great puzzle game.')
>>> fixed
'Tricky Castle is a great puzzle game.'
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

Also, there are available [rust](https://github.com/oriontvv/ryaspeller/) and [javascript](https://github.com/hcodes/yaspeller) versions of this speller.
