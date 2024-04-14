import pytest

from fastbots import Page

@pytest.fixture
def page():
    return Page(None, 'test_locator')

@pytest.mark.parametrize("locator_name,expected", [
('test_locator', '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]'),
('test1_locator', '//*[@id=\'search\']/div[1]/div[1]/div/span[1]/div[1]/div[2]'),
('test2_locator', "//*[@id=\"search\"]/div[1]/div[1]/div/span[1]/div[1]/div[2]"),
('test3_locator', "//*[@id='search']/div[1]/div[1]/div/span[1]/div[1]/div[2]")
])
def test__locator__(page, locator_name, expected):
    assert page.__locator__(locator_name) == expected