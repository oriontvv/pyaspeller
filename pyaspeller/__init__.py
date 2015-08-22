# coding=utf-8
import logging
import sys
from pyaspeller.speller import Speller

__version__ = '0.0.1'
__all__ = ['main']


def check_version():
    if sys.version_info < (2, 7):
        raise SystemExit('ERROR: Python %s detected. Python 2.7 or greater required.',
                         sys.exc_info()[1])


def create_args_parser():
    from argparse import ArgumentParser

    description = "Python text speller"
    parser = ArgumentParser(description=description, version=__version__)

    parser.add_argument('text_or_path_or_url', nargs='?', default='')

    parser.add_argument('--verbose', action="store_const",
                        help="increase verbosity level",
                        dest="log_level", const=logging.INFO,
                        default=logging.WARNING)

    parser.add_argument('--debug', action="store_const",
                        help="print debug information",
                        dest="log_level", const=logging.DEBUG,
                        default=logging.WARNING)

    parser.add_argument('-f', '--format', default='auto',
                        choices=('plain', 'html', 'markdown', 'auto'))

    parser.add_argument('-l', '--lang', default=('en', 'ru'),
                        choices=('en', 'ru', 'uk', 'kk'))

    parser.add_argument('-c', '--config', default=None,
                        help="config path")

    parser.add_argument('-d', '--dictionary', default=None,
                        help="path to custom json dictionary file")

    parser.add_argument('-r', '--report', default='console',
                        choices=('console', 'html', 'markdown', 'json'),
                        help="type of report")

    parser.add_argument('--check-yo', default=False, action='store_true',
                        help="Check the correctness of using the " +
                             "letter “Ё” (Yo) in Russian texts")
    return parser


def main():
    check_version()

    args = create_args_parser().parse_args()
    logging.basicConfig(level=args.log_level)

    speller = Speller(args)
    speller.spell(args.text_or_path_or_url)
