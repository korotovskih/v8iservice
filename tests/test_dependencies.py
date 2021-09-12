import pytest

from app.dependencies import parse_infobases_catalog


def test_parse_infobases_catalog():

    catalog = parse_infobases_catalog("tests/files")

    assert catalog
    assert catalog.get_infobases("testlist")
    assert catalog.get_infobases("notfound") is None
