from pydantic import BaseModel
from typing import Generic, TypeVar


T = TypeVar("T")


class Team(BaseModel):
    id: int
    conference: str
    division: str
    city: str
    name: str
    full_name: str
    abbreviation: str


class Player(BaseModel):
    id: int
    first_name: str
    last_name: str
    position: str
    height: str | None = None
    weight: str | None = None
    jersey_number: str | None = None
    college: str | None = None
    country: str | None = None
    draft_year: int | None = None
    draft_round: int | None = None
    draft_number: int | None = None
    team: Team


class Meta(BaseModel):
    prev_cursor: int | None = None
    next_cursor: int | None = None
    per_page: int


class APIResponse(BaseModel, Generic[T]):
    data: list[T] | T
    meta: Meta | None = None
