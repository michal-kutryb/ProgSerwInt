"""Module containing tournament_team-related domain models"""

from typing import Optional
from asyncpg import Record
from pydantic import BaseModel, ConfigDict
from typing import Optional


class TournamentTeamIn(BaseModel):
    """Model representing tournament_team's DTO attributes."""
    tournament_id: int
    team_id: int


class TournamentTeam(TournamentTeamIn):
    """Model representing tournament_team's attributes in the database."""

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    @classmethod
    def from_record(cls, record: Record) -> "TournamentTeam":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            TournamentTeamDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            tournament_id=record_dict.get("tournament_id"),  # type: ignore
            team_id=record_dict.get("team_id"),  # type: ignore
        )
