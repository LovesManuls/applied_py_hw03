import pytest
from src.links.aux_for_handlers import *

@pytest.mark.parametrize("a, expected", [
    (2, 2),
    (10, 10),
])
def test_gen_short_code(length : int, expected):
    assert len(gen_short_code(length)) == expected  # Нужная длина


@pytest.mark.parametrize("length, expected", [
    (1, True),
    (6, True),
    (8, True),
])
def test_gen_short_code(length : int, expected):
    assert gen_short_code(length).isalpha() == expected  # Валидный код без пробелов...


@pytest.mark.parametrize("new_link_dict, expected", [
    ({ "orig_url": "https://recsyswiki.com/wiki/Main_Page", "short_code": "RecSys"}, True),
    ({ "orig_url": "https://www.wikipedia.org/", "short_code": "dnjsjws"}, True),
])
def test_fill_fields_initially(new_link_dict : int, expected):
    assert type(fill_fields_initially(new_link_dict)) == dict