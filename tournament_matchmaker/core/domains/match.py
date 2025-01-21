"""Module containing match-related domain models"""
import datetime
from typing import Optional
from asyncpg import Record
from pydantic import BaseModel, ConfigDict
from typing import Optional


class MatchIn(BaseModel):
    """Model representing match's DTO attributes."""
    tournament_id: int
    team1_id: int
    team2_id: int
    team1_score: int
    team2_score: int
    match_date: datetime.date


class Match(MatchIn):
    """Model representing match's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    @classmethod
    def from_record(cls, record: Record) -> "Match":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            MatchDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),  # type: ignore
            tournament_id=record_dict.get("tournament_id"),  # type: ignore
            team1_id=record_dict.get("team1_id"),  # type: ignore
            team2_id=record_dict.get("team2_id"),  # type: ignore
            team1_score=record_dict.get("team1_score"),  # type: ignore
            team2_score=record_dict.get("team2_score"),  # type: ignore
            match_date=record_dict.get("match_date"),  # type: ignore
        )

    def get_winner_team_id(self) -> int:
        """A method for getting id of the winner team of the tournament.

        Returns:
            int: The id of the winner team.
        """
        if self.team1_score == 1:
            return self.team1_id
        else:
            return self.team2_id
