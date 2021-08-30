import pytest
from services.leekduck import LeekDuck


@pytest.fisture
def leek(duck):
    """ фікстура """
    return LeekDuck()


def test_init(leek):
    pass
