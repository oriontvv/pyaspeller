import pytest
from pyaspeller.errors import BadArgumentError

from pyaspeller import YandexSpeller


@pytest.fixture
def speller():
    return YandexSpeller()


def test_bad_single_lang_property():
    with pytest.raises(BadArgumentError):
        YandexSpeller(lang="qwe")


def test_correct_lang_property():
    sp = YandexSpeller(lang=("ru", "en"))
    assert sp.lang == ["ru", "en"], "Bad language"


def test_correct_single_lang_property():
    sp = YandexSpeller(lang=("en",))
    assert sp.lang == ["en"], "Bad language"


def test_correct_single_lang_str_property():
    sp = YandexSpeller(lang="uk")
    assert sp.lang == ["uk"], "Bad language"


def test_check_lang_property(speller):
    speller.lang = "en"
    assert speller.lang == ["en"], "Bad language"


def test_param_max_requests(speller):
    assert speller.max_requests == 2, "Bad default max_requests"
    speller.max_requests = 4
    assert speller.max_requests == 4, "Bad max_requests"


def test_param_is_debug(speller):
    assert not speller.is_debug, "Bad default is_debug"
    speller.is_debug = True
    assert speller.is_debug, "Bad is_debug"


def test_param_format(speller):
    assert speller.format == "plain", "Bad default format: " + str(speller.format)
    speller.format = "html"
    assert speller.format == "html", "Bad format: " + str(speller.format)


def test_param_config_path(speller):
    assert speller.config_path == "", "Bad default config_path: " + str(speller.config_path)
    speller.config_path = "/path/to/config"
    assert speller.config_path == "/path/to/config", "Bad config_path: " + str(speller.config_path)

    with pytest.raises(BadArgumentError):
        speller.config_path = ["/path"]


def test_param_dictionary(speller):
    assert speller.dictionary == {}, "Bad default dictionary: " + str(speller.dictionary)
    speller.dictionary = {"answer": 42}
    assert speller.dictionary == {"answer": 42}, "Bad dictionary: " + str(speller.dictionary)

    with pytest.raises(BadArgumentError):
        speller.dictionary = ["/path"]


def test_param_report_type(speller):
    assert speller.report_type == "console", "Bad default report_type"
    speller.report_type = "file"
    assert speller.report_type == "file", "report_type not setted: " + str(speller.report_type)

    speller.report_type = ""
    assert speller.report_type == "console", "Bad report_type: " + str(speller.report_type)


def test_param_check_yo(speller):
    assert speller.check_yo is False, "Bad default check_yo"
    speller.check_yo = True
    assert speller.check_yo, "Bad check_yo: " + str(speller.check_yo)


def test_param_ignore_tags(speller):
    assert not speller.ignore_tags, "Bad default ignore_tags"
    speller.ignore_tags = True
    assert speller.ignore_tags, "Bad ignore_tags: " + str(speller.ignore_tags)


def test_param_ignore_uppercase(speller):
    assert not speller.api_options & 1, "Bad ignore_uppercase option"
    assert not speller.ignore_uppercase, "Bad default ignore_uppercase"
    speller.ignore_uppercase = True
    assert speller.api_options & 1, "Bad ignore_uppercase option"


def test_param_ignore_digits(speller):
    assert not speller.api_options & 2, "Bad ignore_digits option"
    assert not speller.ignore_digits, "Bad default ignore_digits"
    speller.ignore_digits = True
    assert speller.api_options & 2, "Bad ignore_digits option"


def test_param_ignore_urls(speller):
    assert not speller.api_options & 4, "Bad ignore_urls option"
    assert not speller.ignore_urls, "Bad default ignore_urls"
    speller.ignore_urls = True
    assert speller.api_options & 4, "Bad ignore_urls option"


def test_param_find_repeat_words(speller):
    assert not speller.api_options & 8, "Bad find_repeat_words option"
    assert not speller.find_repeat_words, "Bad default find_repeat_words"
    speller.find_repeat_words = True
    assert speller.api_options & 8, "Bad find_repeat_words option"


def test_param_ignore_latin(speller):
    assert not speller.api_options & 16, "Bad ignore_latin option"
    assert not speller.ignore_latin, "Bad default ignore_latin"
    speller.ignore_latin = True
    assert speller.api_options & 16, "Bad ignore_latin option"


def test_param_flag_latin(speller):
    assert not speller.api_options & 128, "Bad flag_latin option"
    assert not speller.flag_latin, "Bad default flag_latin"
    speller.flag_latin = True
    assert speller.api_options & 128, "Bad flag_latin option"


def test_param_by_words(speller):
    assert not speller.api_options & 256, "Bad by_words option"
    assert not speller.by_words, "Bad default by_words"
    speller.by_words = True
    assert speller.api_options & 256, "Bad by_words option"


def test_param_ignore_capitalization(speller):
    assert not speller.api_options & 512, "Bad ignore_capitalization option"
    assert not speller.ignore_capitalization, "Bad default ignore_capitalization"
    speller.ignore_capitalization = True
    assert speller.api_options & 512, "Bad ignore_capitalization option"


def test_param_ignore_roman_numerals(speller):
    assert not speller.api_options & 2048, "Bad ignore_roman_numerals option"
    assert not speller.ignore_roman_numerals, "Bad default ignore_capitalization"
    speller.ignore_roman_numerals = True
    assert speller.api_options & 2048, "Bad ignore_roman_numerals option"


def test_spelled(speller):
    result = speller.spelled("tesst message")
    assert result == "test message"


def test_spelled_text(speller):
    result = speller.spelled_text("tesst message")
    assert result == "test message"


def test_spell_text(speller):
    result = speller.spell_text("tesst message")
    assert result == [
        {"code": 1, "pos": 0, "row": 0, "col": 0, "len": 5, "word": "tesst", "s": ["test", "text", "this"]}
    ]


def test_spelled_url(speller, requests_mock):
    url = "https://some-url.org"
    requests_mock.post(
        speller._api_query,
        json=[{"code": 1, "pos": 12, "row": 0, "col": 12, "len": 6, "word": "maagic", "s": ["magic"]}],
    )
    requests_mock.get(url, json={"some": "maagic"})
    result = speller.spelled(url)
    assert result == '{"some": "magic"}'

    result = speller.spell_url(url)
    assert result == '{"some": "magic"}'


def test_spell_url(speller, requests_mock):
    url = "https://some-url.org"
    data = [{"code": 1, "pos": 12, "row": 0, "col": 12, "len": 6, "word": "maagic", "s": ["magic"]}]
    requests_mock.post(
        speller._api_query,
        json=data,
    )
    requests_mock.get(url, json={"some": "maagic"})
    result = list(speller.spell(url))
    assert result == data


@pytest.mark.parametrize("bad_argument", [0, True, None, ["tesst "], {"bad": "arg"}])
def test_spelled_list_of_strings(speller, bad_argument):
    with pytest.raises(BadArgumentError):
        speller.spelled(bad_argument)
    with pytest.raises(BadArgumentError):
        list(speller.spell(bad_argument))


def test_spell_path(speller, tmpdir):
    p = tmpdir.join("file.txt")
    p.write("tesst message")

    speller.spell_path(str(tmpdir), apply=True)

    assert p.read() == "test message"

    speller.spell_path("./bad_path_doesnt_raise_error", apply=False)


def test_spell_path_without_applying(speller, tmpdir):
    p = tmpdir.join("file.txt")
    p.write("tesst message")

    speller.spell_path(str(tmpdir), apply=False)

    assert p.read() == "tesst message"


def test_spell_path_file(speller, tmpdir):
    p = tmpdir.join("file.txt")
    p.write("tesst message")

    speller.spell_path(p, apply=True)

    assert p.read() == "test message"


def test_spelled_path_file(speller, tmpdir):
    p = tmpdir.join("file.txt")
    p.write("tesst message")

    speller.spelled(str(p))

    assert p.read() == "test message"
