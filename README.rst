Python text speller
===================

|Build Status| |Coverage Status| |Code Climate|

|PyPI badge| |Installs badge| |Wheel badge| |License badge| |Doc badge|


License
-------

`pyaspeller`_ is open sourced under the `Apache 2.0 License <http://www.apache.org/licenses/LICENSE-2.0>`_

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


Installation
------------

To install ``pyaspeller``, simply do:

.. code-block:: bash

    $ pip install pyaspeller
    $ pyaspeller --help


.. |Build Status| image:: https://secure.travis-ci.org/oriontvv/pyaspeller.png
    :target:  https://secure.travis-ci.org/oriontvv/pyaspeller
    :alt: Build Status

.. |Coverage Status| image:: https://img.shields.io/coveralls/oriontvv/pyaspeller.svg
    :target: https://coveralls.io/r/oriontvv/pyaspeller
    :alt: Coverage Status

.. |Code Climate| image:: https://codeclimate.com/github/oriontvv/pyaspeller/badges/gpa.svg
    :target:  https://codeclimate.com/github/oriontvv/pyaspeller
    :alt: Code Climate

.. |PyPI badge| image:: http://img.shields.io/pypi/v/pyaspeller.svg?style=flat
    :target: http://badge.fury.io/py/pyaspeller
    :alt: PyPI

.. |Installs badge| image:: http://img.shields.io/pypi/dm/pyaspeller.svg?style=flat
    :target: https://crate.io/packages/pyaspeller/
    :alt: Installs

.. |Wheel badge| image:: http://img.shields.io/badge/wheel-no-red.svg?style=flat
    :alt: Whell support

.. |License badge| image:: http://img.shields.io/badge/license-Apache%202.0-green.svg?style=flat
    :alt: license

.. |Doc badge| image:: https://readthedocs.org/projects/pyaspeller/badge/?version=latest
    :target: https://readthedocs.org/projects/pyaspeller/?badge=latest
    :alt: Documentation Status