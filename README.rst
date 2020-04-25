Python text speller
===================

|Build Status| |Coverage Status| |Code Health| |Gitter Chat|

|PyPI badge| |Installs badge| |License badge| |Doc badge|

|Requirements Status| |Python versions|

License
-------

`pyaspeller`_ (Python Yandex Speller) is a search tool typos in the text, files and websites.
Used API `Yandex.Speller <https://tech.yandex.ru/speller/doc/dg/concepts/About-docpage/>`_.

.. _pyaspeller: https://github.com/oriontvv/pyaspeller
.. _Apache 2.0 License: http://www.apache.org/licenses/LICENSE-2.0

Features (under development)
----------------------------

.. code-block:: bash

    $ pyaspeller "testt reques"
    {u'code': 1,
     u'col': 0,
     u'len': 5,
     u'pos': 0,
     u'row': 0,
     u's': [u'test'],
     u'word': u'testt'}
    {u'code': 1,
     u'col': 6,
     u'len': 6,
     u'pos': 6,
     u'row': 0,
     u's': [u'request'],
     u'word': u'reques'}


You could use class ``Word`` for single word queries:

.. code-block:: python

    >>> from pyaspeller import Word
    >>> check = Word('tesst')
    >>> check.correct
    False
    >>> check.variants
    [u'test']
    >>> check.spellsafe
    u'test'


For whole text you could use:

.. code-block:: python

    >>> from pyaspeller import YandexSpeller
    >>> speller = YandexSpeller()
    >>> text = 'В суббботу утромь.'
    >>> changes = {change['word']: change['s'][0] for change in speller.spell(text)}
    >>> for word, suggestion in changes.items():
    ...     text = text.replace(word, suggestion)
    >>> text
    'В субботу утром.'

Installation
------------

To install ``pyaspeller``, simply do:

.. code-block:: bash

    $ pip install pyaspeller
    $ pyaspeller --help


Restrictions API Yandex.Speller
-------------------------------
    speller has some `restrictions <https://yandex.ru/legal/speller_api/>`_

 [ ~ Dependencies scanned by `PyUp.io <https://pyup.io/>`_ ~ ]
 
.. |Gitter Chat| image:: https://badges.gitter.im/Join%20Chat.svg
    :target: https://gitter.im/oriontvv/pyaspeller?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
    :alt: Join the chat at https://gitter.im/oriontvv/pyaspeller

.. |Build Status| image:: https://secure.travis-ci.org/oriontvv/pyaspeller.png
    :target:  https://secure.travis-ci.org/oriontvv/pyaspeller
    :alt: Build Status

.. |Coverage Status| image:: https://img.shields.io/coveralls/oriontvv/pyaspeller.svg
    :target: https://coveralls.io/r/oriontvv/pyaspeller
    :alt: Coverage Status

.. |Code Climate| image:: https://codeclimate.com/github/oriontvv/pyaspeller/badges/gpa.svg
    :target:  https://codeclimate.com/github/oriontvv/pyaspeller
    :alt: Code Climate

.. |Code Health| image:: https://landscape.io/github/oriontvv/pyaspeller/master/landscape.svg?style=flat
    :target: https://landscape.io/github/oriontvv/pyaspeller/master
    :alt: Code Health

.. |PyPI badge| image:: http://img.shields.io/pypi/v/pyaspeller.svg?style=flat
    :target: http://badge.fury.io/py/pyaspeller
    :alt: PyPI

.. |Installs badge| image:: http://img.shields.io/pypi/dm/pyaspeller.svg?style=flat
    :target: https://crate.io/packages/pyaspeller/
    :alt: Installs

.. |License badge| image:: http://img.shields.io/badge/license-Apache%202.0-green.svg?style=flat
    :alt: license

.. |Doc badge| image:: https://readthedocs.org/projects/pyaspeller/badge/?version=latest
    :target: https://readthedocs.org/projects/pyaspeller/?badge=latest
    :alt: Documentation Status

.. |Requirements Status| image:: https://requires.io/github/oriontvv/pyaspeller/requirements.svg?branch=master
    :target: https://requires.io/github/oriontvv/pyaspeller/requirements/?branch=master
    :alt: Requirements Status

.. |Python versions| image:: https://img.shields.io/pypi/pyversions/pyaspeller.svg
    :target: https://img.shields.io/pypi/pyversions/pyaspeller.svg
    :alt: Python versions
    

