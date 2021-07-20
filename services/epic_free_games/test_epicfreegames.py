import pytest
import datetime
from services.epic_free_games import epicfreegames


@pytest.fixture
def epic_obj():
    epic = epicfreegames.EFG()
    return epic


def test_self_data(epic_obj):
    assert type(epic_obj.data) == dict
    assert epic_obj.data.get('data') is not None


def test_get_games(epic_obj):
    games = epic_obj.get_games()
    assert type(games) == str


def test_next_update(epic_obj):
    nupdate = epic_obj.next_update()
    assert type(nupdate) == datetime.datetime
