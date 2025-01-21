"""Module containing tournament-related domain models"""
import datetime
from typing import Optional, List
from asyncpg import Record
from pydantic import BaseModel, ConfigDict
from typing import Optional


class TournamentIn(BaseModel):
    """Model representing tournament's DTO attributes."""
    name: str
    date: datetime.date
    max_teams_count: int
    preffered_rank: str


class Tournament(TournamentIn):
    """Model representing tournament's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    @classmethod
    def from_record(cls, record: Record) -> "Tournament":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            TournamentDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),  # type: ignore
            name=record_dict.get("name"),  # type: ignore
            date=record_dict.get("date"),
            max_teams_count=record_dict.get("max_teams_count"),
            preffered_rank=record_dict.get("preffered_rank"),
        )
