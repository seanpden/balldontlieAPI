import os
from dotenv import load_dotenv
from balldontlie.balldontlie import BalldontlieAPI


def main() -> None:
    _ = load_dotenv()
    key = os.getenv("API_KEY")
    api = BalldontlieAPI(key)
    print(api.get_players(first_name="Anthony"))
    # print(api.get_teams())
