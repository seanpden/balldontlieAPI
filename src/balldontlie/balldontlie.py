import requests
from typing import List, Optional
from balldontlie.models import APIResponse, Player, Team


class BalldontlieAPI:
    def __init__(self, api_key: str | None) -> None:
        if not api_key:
            raise ValueError("api_key required!")
        self._api_key = api_key
        self._headers = {"Authorization": self._api_key}
        self.base_url = "https://api.balldontlie.io/v1/"

    def _check_for_errors(self, resp: requests.Response):
        if resp.status_code == 401:
            raise requests.exceptions.HTTPError(
                f"{resp.status_code}: Unauthorized - You either need an API key or your account tier does not have access to the endpoint."
            )

        if resp.status_code == 400:
            raise requests.exceptions.HTTPError(
                f"{resp.status_code}: Bad Request -- The request is invalid. The request parameters are probably incorrect."
            )

        if resp.status_code == 404:
            raise requests.exceptions.HTTPError(
                f"{resp.status_code}: Not Found -- The specified resource could not be found."
            )

        if resp.status_code == 406:
            raise requests.exceptions.HTTPError(
                f"{resp.status_code}: Not Acceptable -- You requested a format that isn't json."
            )

        if resp.status_code == 429:
            raise requests.exceptions.HTTPError(
                f"{resp.status_code}: Too Many Requests -- You're rate limited. \n{resp.headers}"
            )

        if resp.status_code == 500:
            raise requests.exceptions.HTTPError(
                f"{resp.status_code}: Internal Server Error -- We had a problem with our server. Try again later."
            )

        if resp.status_code == 503:
            raise requests.exceptions.HTTPError(
                f"{resp.status_code}: Service Unavailable -- We're temporarily offline for maintenance. Please try again later."
            )

    def _get_teams(self) -> dict:
        url: str = f"{self.base_url}/teams"
        resp = requests.get(url=url, headers=self._headers)

        self._check_for_errors(resp)

        return resp.json()

    def get_teams(self) -> APIResponse[Team]:
        teams = self._get_teams()
        return APIResponse[Team](**teams)

    def _get_team(self, id: int) -> dict:
        if not isinstance(id, int):
            raise TypeError("Argument 'id' should be of type 'int'.")

        url: str = f"{self.base_url}/teams/{str(id)}"
        resp = requests.get(url=url, headers=self._headers)

        self._check_for_errors(resp)

        return resp.json()

    def get_team(self, id: int) -> APIResponse[Team]:
        team = self._get_team(id)
        return APIResponse[Team](**team)

    def _get_players(
        self,
        cursor: Optional[int] = None,
        search: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        team_ids: Optional[str] = None,
        player_ids: Optional[str] = None,
    ) -> dict:
        url: str = f"{self.base_url}/players"
        payload = {
            "cursor": cursor,
            "search": search,
            "first_name": first_name,
            "last_name": last_name,
            "team_ids": team_ids,
            "player_ids": player_ids,
        }
        resp = requests.get(url=url, headers=self._headers, params=payload)

        self._check_for_errors(resp)

        return resp.json()

    def get_players(
        self,
        cursor: Optional[int] = None,
        search: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        team_ids: Optional[str] = None,
        player_ids: Optional[str] = None,
    ) -> APIResponse[Player]:
        players = self._get_players(
            cursor, search, first_name, last_name, team_ids, player_ids
        )
        players = APIResponse[Player](**players)

        while players.meta and players.meta.next_cursor:
            next_page = self.get_players(
                cursor=players.meta.next_cursor,
                search=search,
                first_name=first_name,
                last_name=last_name,
                team_ids=team_ids,
                player_ids=player_ids,
            )

            # For LSP to stop screaming
            assert isinstance(next_page.data, List)
            assert isinstance(players.data, List)
            assert next_page.meta

            players.data.extend(next_page.data)
            players.meta.next_cursor = next_page.meta.next_cursor

        return players

    def _get_player(self, id: int) -> dict:
        if not isinstance(id, int):
            raise TypeError("Argument 'id' should be of type 'int'.")

        url: str = f"{self.base_url}/players/{str(id)}"
        resp = requests.get(url=url, headers=self._headers)

        self._check_for_errors(resp)

        return resp.json()

    def get_player(self, id: int) -> APIResponse[Player]:
        player = self._get_player(id)
        return APIResponse[Player](**player)
