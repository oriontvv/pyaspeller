from pprint import pprint

from pyaspeller import YandexSpeller

speller = YandexSpeller(lang="en", ignore_digits=True)
spelled = speller.spelled("42 is a cUl maagic namber")
assert spelled == "42 is a cool magic number"


changes = speller.spell("42 is a cUl maagic namber")
for change in changes:
    pprint(change)

"""
{'code': 1,
 'col': 8,
 'len': 3,
 'pos': 8,
 'row': 0,
 's': ['cool', 'call', 'cull'],
 'word': 'cUl'}
{'code': 1,
 'col': 12,
 'len': 6,
 'pos': 12,
 'row': 0,
 's': ['magic'],
 'word': 'maagic'}
{'code': 1,
 'col': 19,
 'len': 6,
 'pos': 19,
 'row': 0,
 's': ['number'],
 'word': 'namber'}
"""
