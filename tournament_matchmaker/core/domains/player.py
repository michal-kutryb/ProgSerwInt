"""Module containing player-related domain models"""

from typing import Optional
from asyncpg import Record
from pydantic import BaseModel, ConfigDict
from typing import Optional


class PlayerIn(BaseModel):
    """Model representing player's DTO attributes."""
    name: str
    rank: str
    team_id: Optional [int] = None


class Player(PlayerIn):
    """Model representing player's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    @classmethod
    def from_record(cls, record: Record) -> "Player":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            PlayerDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),  # type: ignore
            name=record_dict.get("name"),  # type: ignore
            rank=record_dict.get("rank"),
            team_id=record_dict.get("team_id", None),  # type: ignore
        )
