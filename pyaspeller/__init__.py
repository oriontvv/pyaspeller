# coding=utf-8
import logging
from pprint import pprint
import sys
from pyaspeller.speller import YandexSpeller

__version__ = '0.0.5'
__all__ = ['main']


def check_version():
    if sys.version_info < (2, 7):
        raise SystemExit('Python %s detected. Python 2.7 or greater '
                         'required.' % str(sys.version_info))


def create_args_parser():
    from argparse import ArgumentParser

    description = "Search tool typos in the text, files and websites."
    parser = ArgumentParser(description=description, prog='pyaspeller')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + __version__)

    parser.add_argument('text_or_path_or_url', nargs='?', default='')

    parser.add_argument('--config_path', default=None,
                        help="Configuration file path")

    parser.add_argument('--debug', action="store_const",
                        help="print debug information",
                        dest="log_level", const=logging.DEBUG,
                        default=logging.WARNING)

    parser.add_argument('--verbose', action="store_const",
                        help="increase verbosity level",
                        dest="log_level", const=logging.INFO,
                        default=logging.WARNING)

    parser.add_argument('-f', '--format', default='auto',
                        choices=('plain', 'html', 'markdown', 'auto'),
                        help="formats")

    parser.add_argument('-l', '--lang', default=['en', 'ru'], nargs='+',
                        choices=('en', 'ru', 'uk', 'kk'), help="languages")

    parser.add_argument('-c', '--config', default=None,
                        help="config path")

    parser.add_argument('-d', '--dictionary', default=None,
                        help="path to custom json dictionary file")

    parser.add_argument('-r', '--report_type', default='console',
                        choices=('console', 'html', 'markdown', 'json'),
                        help="type of report")

    parser.add_argument('--check_yo', default=True, action='store_true',
                        help="check the correctness of using the " +
                             "letter “Ё” (Yo) in Russian texts")

    parser.add_argument('--find-repeat-words', action='store_true',
                        help="highlight repetitions of words, consecutive. " +
                             "For example, I flew to to to Cyprus")

    parser.add_argument('--flag-latin', action='store_true',
                        help="celebrate words, written in Latin, as erroneous")

    parser.add_argument('--ignore-tags', action='store_true',
                        help="ignore HTML tags. "
                             "Default: code,kbd,object,samp,script,style,var "
                             "Option to formats html and markdown")

    parser.add_argument('--ignore_capitalization', action='store_true',
                        help="ignore the incorrect use of UPPERCASE/lowercase "
                             "letters, for example, in the word moscow")

    parser.add_argument('--ignore_digits', action='store_true',
                        help="ignore words with numbers, such as avp17h4534")

    parser.add_argument('--ignore-latin', action='store_true',
                        help="ignore words, written in Latin, like 'madrid'")

    parser.add_argument('--ignore-roman-numerals', action='store_true',
                        help="ignore Roman numerals I, II, III, ...")

    parser.add_argument('--ignore_uppercase', action='store_true',
                        help="ignore words written in capital letters")

    parser.add_argument('--ignore_urls', action='store_true',
                        help="ignore Internet addresses, email "
                             "addresses and filenames")

    parser.add_argument('--max-requests', default=2,
                        help="Max count of requests at a time")

    return parser


def create_speller(args):
    speller = YandexSpeller(format=args.format,
                            lang=args.lang,
                            config_path=args.config_path,
                            dictionary=args.dictionary,
                            report_type=args.report_type,
                            is_debug=args.log_level == logging.DEBUG,
                            check_yo=args.check_yo,
                            ignore_urls=args.ignore_urls,
                            ignore_tags=args.ignore_tags,
                            ignore_capitalization=args.ignore_capitalization,
                            ignore_digits=args.ignore_digits,
                            ignore_latin=args.ignore_latin,
                            ignore_roman_numerals=args.ignore_roman_numerals,
                            ignore_uppercase=args.ignore_uppercase,
                            find_repeat_words=args.find_repeat_words,
                            flag_latin=args.flag_latin)

    return speller


def main():
    check_version()

    args = create_args_parser().parse_args()
    logging.basicConfig(level=args.log_level)

    speller = create_speller(args)

    result = speller.spell(args.text_or_path_or_url)
    for generator in result:
        for item in generator:
            pprint(item)
