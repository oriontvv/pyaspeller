import codecs
import os
import re
from setuptools import setup, find_packages

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(BASE_PATH, 'pyaspeller', '__init__.py'), 'r',
                 'latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'\r?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


def read(f):
    return open(os.path.join(BASE_PATH, f)).read().strip()


install_requires = ['six']


class BuildFailed(Exception):
    pass


args = dict(
    name='pyaspeller',
    version=version,
    description="Search tool typos in the text, files and websites.",
    long_description='\n\n'.join((read('README.rst'), read('CHANGES.txt'))),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing :: Linguistic'],
    author='Vassiliy Taranov',
    author_email='taranov.vv@gmail.com',
    url='https://github.com/oriontvv/pyaspeller',
    license='Apache 2',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'pyaspeller = pyaspeller.__init__:main'
        ]
    },
    test_suite='tests',
    include_package_data=True,
)

setup(**args)
