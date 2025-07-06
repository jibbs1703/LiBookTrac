"""Sample Test to Pass CI."""

import pytest


def add(a:int, b:int) -> int:
    return a+b


@pytest.mark.sample
def test_add():
    assert add(2,3) == 5