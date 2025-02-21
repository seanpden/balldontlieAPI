from pydantic import BaseModel
from typing import Generic, List, Optional, TypeVar


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
    height: Optional[str] = None
    weight: Optional[str] = None
    jersey_number: Optional[str] = None
    college: Optional[str] = None
    country: Optional[str] = None
    draft_year: Optional[int] = None
    draft_round: Optional[int] = None
    draft_number: Optional[int] = None
    team: Team


class Meta(BaseModel):
    prev_cursor: Optional[int] = None
    next_cursor: Optional[int] = None
    per_page: int


class APIResponse(BaseModel, Generic[T]):
    data: List[T] | T
    meta: Optional[Meta] = None
