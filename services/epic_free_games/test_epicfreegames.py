import epicfreegames

def test_get_games():
    games = epicfreegames.get_games()
    assert type(games) == str


def test_next_update():
    pass
