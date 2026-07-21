import pytest

from greeter import greet

@pytest.mark.parametrize("name, expected", [
    ("Chaz", "Hello, Chaz!"),
    ("Sarah", "Hello, Sarah!"),
])
def test_greeter(name, expected):
    assert greet(name)
