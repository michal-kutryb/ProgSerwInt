"""Module containing match repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable, List

from tournament_matchmaker.core.domains.match import MatchIn, Match
from tournament_matchmaker.core.domains.tournament import Tournament


class IMatchRepository(ABC):
    """An abstract class representing protocol of match repository."""

    @abstractmethod
    async def get_all_matches(self) -> Iterable[Any]:
        """The abstract getting all matches from the data storage.

        Returns:
            Iterable[Any]: Matches in the data storage.
        """

    @abstractmethod
    async def get_by_id(self, match_id: int) -> Any | None:
        """The abstract getting match by provided id.

        Args:
            match_id (int): The id of the match.

        Returns:
            Any | None: The match details.
        """

    @abstractmethod
    async def get_by_tournament_id(self, tournament_id: int) -> List[Match]:
        """The abstract getting match by provided tournament_id.

        Args:
            tournament_id (int): The id of the tournament.

        Returns:
            List[Match]: The list of matches
        """

    @abstractmethod
    async def add_match(self, data: MatchIn) -> Any | None:
        """The abstract adding new match to the data storage.

        Args:
            data (MatchIn): The details of the new match.

        Returns:
            Any | None: The newly added match.
        """

    @abstractmethod
    async def update_match(
            self,
            match_id: int,
            data: MatchIn,
    ) -> Any | None:
        """The abstract updating match data in the data storage.

        Args:
            match_id (int): The id of the match.
            data (MatchIn): The details of the updated match.

        Returns:
            Any | None: The updated match details.
        """

    @abstractmethod
    async def delete_match(self, match_id: int) -> bool:
        """The abstract updating removing match from the data storage.

        Args:
            match_id (int): The id of the match.

        Returns:
            bool: Success of the operation.
        """
