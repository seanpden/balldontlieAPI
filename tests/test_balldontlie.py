from typing import List
import pytest
import os
from dotenv import load_dotenv
from balldontlie.balldontlie import BalldontlieAPI
from balldontlie.models import Player, Team

load_dotenv()


def test_balldontlie_init():
    with pytest.raises(ValueError):
        _ = BalldontlieAPI
        _ = BalldontlieAPI(None)
    assert BalldontlieAPI("api_key")


def test_balldontlie_internal_get_teams():
    api = BalldontlieAPI(os.getenv("API_KEY"))
    teams = api._get_teams()
    assert teams
    assert teams.get("data")
    assert teams.get("data")[0].get("id") == 1


def test_balldontlie_internal_get_team():
    api = BalldontlieAPI(os.getenv("API_KEY"))

    id = "1"
    with pytest.raises(TypeError):
        _ = api._get_team(id)

    id = 1
    teams = api._get_team(id)
    assert teams
    assert teams.get("data")
    assert teams.get("data").get("id") == 1


def test_balldontlie_get_teams():
    api = BalldontlieAPI(os.getenv("API_KEY"))
    teams = api.get_teams()
    assert teams
    assert teams.data
    assert isinstance(teams.data, List)
    assert isinstance(teams.data[0], Team)
    assert teams.data[0].id == 1


def test_balldontlie_get_team():
    api = BalldontlieAPI(os.getenv("API_KEY"))

    id = "1"
    with pytest.raises(TypeError):
        _ = api.get_team(id)

    id = 1
    teams = api.get_team(id)
    assert teams
    assert teams.data
    assert isinstance(teams.data, Team)
    assert teams.data.id == 1


def test_balldontlie_internal_get_players():
    api = BalldontlieAPI(os.getenv("API_KEY"))
    players = api._get_players()
    assert players
    assert players.get("data")
    assert players.get("data")[0].get("id") == 1


def test_balldontlie_internal_get_player():
    api = BalldontlieAPI(os.getenv("API_KEY"))

    id = "1"
    with pytest.raises(TypeError):
        _ = api._get_player(id)

    id = 1
    players = api._get_player(id)
    assert players
    assert players.get("data")
    assert players.get("data").get("id") == 1


def test_balldontlie_get_players():
    api = BalldontlieAPI(os.getenv("API_KEY"))
    search = "Davis"
    players = api.get_players(last_name=search)
    assert players
    assert players.data
    assert isinstance(players.data, List)
    assert isinstance(players.data[0], Player)
    assert players.data[0].last_name == search


def test_balldontlie_get_player():
    api = BalldontlieAPI(os.getenv("API_KEY"))

    id = "1"
    with pytest.raises(TypeError):
        _ = api.get_player(id)

    id = 1
    players = api.get_player(id)
    assert players
    assert players.data
    assert isinstance(players.data, Player)
    assert players.data.id == 1
