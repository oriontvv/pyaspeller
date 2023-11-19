from __future__ import annotations
import pytest
import requests_mock

from pyaspeller.errors import BadArgumentError
from pyaspeller import YandexSpeller


@pytest.fixture
def speller() -> YandexSpeller:
    return YandexSpeller()


def test_bad_single_lang_property() -> None:
    with pytest.raises(BadArgumentError):
        YandexSpeller(lang="qwe")


def test_correct_lang_property() -> None:
    sp = YandexSpeller(lang=("ru", "en"))
    assert sp.lang == ["ru", "en"], "Bad language"


def test_correct_single_lang_property() -> None:
    sp = YandexSpeller(lang=("en",))
    assert sp.lang == ["en"], "Bad language"


def test_correct_single_lang_str_property() -> None:
    sp = YandexSpeller(lang="uk")
    assert sp.lang == ["uk"], "Bad language"


def test_check_lang_property(speller: YandexSpeller) -> None:
    speller.lang = "en"
    assert speller.lang == ["en"], "Bad language"


def test_param_max_requests(speller: YandexSpeller) -> None:
    assert speller.max_requests == 2, "Bad default max_requests"
    speller.max_requests = 4
    assert speller.max_requests == 4, "Bad max_requests"


def test_param_is_debug(speller: YandexSpeller) -> None:
    assert not speller.is_debug, "Bad default is_debug"
    speller.is_debug = True
    assert speller.is_debug, "Bad is_debug"


def test_param_format(speller: YandexSpeller) -> None:
    assert speller.format == "plain", "Bad default format: " + str(speller.format)
    speller.format = "html"
    assert speller.format == "html", "Bad format: " + str(speller.format)


def test_param_config_path(speller: YandexSpeller) -> None:
    assert speller.config_path == "", "Bad default config_path: " + str(
        speller.config_path
    )
    speller.config_path = "/path/to/config"
    assert speller.config_path == "/path/to/config", "Bad config_path: " + str(
        speller.config_path
    )

    with pytest.raises(BadArgumentError):
        speller.config_path = ["/path"]


def test_param_dictionary(speller: YandexSpeller) -> None:
    assert speller.dictionary == {}, "Bad default dictionary: " + str(
        speller.dictionary
    )
    speller.dictionary = {"answer": 42}
    assert speller.dictionary == {"answer": 42}, "Bad dictionary: " + str(
        speller.dictionary
    )

    with pytest.raises(BadArgumentError):
        speller.dictionary = ["/path"]


def test_param_report_type(speller: YandexSpeller) -> None:
    assert speller.report_type == "console", "Bad default report_type"
    speller.report_type = "file"
    assert speller.report_type == "file", "report_type not setted: " + str(
        speller.report_type
    )

    speller.report_type = ""
    assert speller.report_type == "console", "Bad report_type: " + str(
        speller.report_type
    )


def test_param_check_yo(speller: YandexSpeller) -> None:
    assert speller.check_yo is False, "Bad default check_yo"
    speller.check_yo = True
    assert speller.check_yo, "Bad check_yo: " + str(speller.check_yo)


def test_param_ignore_tags(speller: YandexSpeller) -> None:
    assert not speller.ignore_tags, "Bad default ignore_tags"
    speller.ignore_tags = True
    assert speller.ignore_tags, "Bad ignore_tags: " + str(speller.ignore_tags)


def test_param_ignore_digits(speller: YandexSpeller) -> None:
    assert not speller.api_options & 2, "Bad ignore_digits option"
    assert not speller.ignore_digits, "Bad default ignore_digits"
    speller.ignore_digits = True
    assert speller.api_options & 2, "Bad ignore_digits option"


def test_param_ignore_urls(speller: YandexSpeller) -> None:
    assert not speller.api_options & 4, "Bad ignore_urls option"
    assert not speller.ignore_urls, "Bad default ignore_urls"
    speller.ignore_urls = True
    assert speller.api_options & 4, "Bad ignore_urls option"


def test_param_find_repeat_words(speller: YandexSpeller) -> None:
    assert not speller.api_options & 8, "Bad find_repeat_words option"
    assert not speller.find_repeat_words, "Bad default find_repeat_words"
    speller.find_repeat_words = True
    assert speller.api_options & 8, "Bad find_repeat_words option"


def test_param_ignore_capitalization(speller: YandexSpeller) -> None:
    assert not speller.api_options & 512, "Bad ignore_capitalization option"
    assert not speller.ignore_capitalization, "Bad default ignore_capitalization"
    speller.ignore_capitalization = True
    assert speller.api_options & 512, "Bad ignore_capitalization option"


def test_spelled(speller: YandexSpeller) -> None:
    result = speller.spelled("tesst message")
    assert result == "test message"


def test_spelled_text(speller: YandexSpeller) -> None:
    result = speller.spelled_text("tesst message")
    assert result == "test message"


def test_spell_text(speller: YandexSpeller) -> None:
    result = speller.spell_text("tesst message")
    assert result == [
        {
            "code": 1,
            "pos": 0,
            "row": 0,
            "col": 0,
            "len": 5,
            "word": "tesst",
            "s": ["test", "text", "this"],
        }
    ]


def test_spelled_url(speller: YandexSpeller) -> None:
    url = "https://some-url.org"
    with requests_mock.Mocker() as mock:
        mock.post(
            speller._api_query,
            json=[
                {
                    "code": 1,
                    "pos": 12,
                    "row": 0,
                    "col": 12,
                    "len": 6,
                    "word": "maagic",
                    "s": ["magic"],
                }
            ],
        )
        mock.get(url, json={"some": "maagic"})
        result = speller.spelled(url)
        assert result == '{"some": "magic"}'

        result = speller.spell_url(url)
        assert result == '{"some": "magic"}'


def test_spell_url(speller: YandexSpeller) -> None:
    url = "https://some-url.org"
    data = [
        {
            "code": 1,
            "pos": 12,
            "row": 0,
            "col": 12,
            "len": 6,
            "word": "maagic",
            "s": ["magic"],
        }
    ]
    with requests_mock.Mocker() as mock:
        mock.post(
            speller._api_query,
            json=data,
        )
        mock.get(url, json={"some": "maagic"})
        result = list(speller.spell(url))
        assert result == data


@pytest.mark.parametrize("bad_argument", [0, True, None, ["tesst "], {"bad": "arg"}])
def test_spelled_list_of_strings(
    speller: YandexSpeller, bad_argument: int | bool | None | list | dict
) -> None:
    with pytest.raises(BadArgumentError):
        speller.spelled(bad_argument)
    with pytest.raises(BadArgumentError):
        list(speller.spell(bad_argument))


def test_spell_path(speller: YandexSpeller, tmpdir: pytest.TempdirFactory) -> None:
    p = tmpdir.join("file.txt")
    p.write("tesst message")

    speller.spell_path(str(tmpdir), apply=True)

    assert p.read() == "test message"

    speller.spell_path("./bad_path_doesnt_raise_error", apply=False)


def test_spell_path_without_applying(
    speller: YandexSpeller, tmpdir: pytest.TempdirFactory
) -> None:
    p = tmpdir.join("file.txt")
    p.write("tesst message")

    speller.spell_path(str(tmpdir), apply=False)

    assert p.read() == "tesst message"


def test_spell_path_file(speller: YandexSpeller, tmpdir: pytest.TempdirFactory) -> None:
    p = tmpdir.join("file.txt")
    p.write("tesst message")

    speller.spell_path(p, apply=True)

    assert p.read() == "test message"


def test_spelled_path_file(
    speller: YandexSpeller, tmpdir: pytest.TempdirFactory
) -> None:
    p = tmpdir.join("file.txt")
    p.write("tesst message")

    speller.spelled(str(p))

    assert p.read() == "test message"
