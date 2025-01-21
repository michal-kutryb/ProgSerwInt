"""Module containing match service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable, List

from tournament_matchmaker.core.domains.match import Match, MatchIn
from tournament_matchmaker.core.domains.tournament import Tournament


class IMatchService(ABC):
    """A class representing match repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[Match]:
        """The method getting all matches from the repository.

        Returns:
            Iterable[Match]: All matches.
        """


    @abstractmethod
    async def get_by_id(self, match_id: int) -> Match | None:
        """The method getting match by provided id.

        Args:
            match_id (int): The id of the match.

        Returns:
            Match | None: The match details.
        """

    @abstractmethod
    async def get_by_tournament_id(self, tournament_id: int) -> List[Match]:
        """The method getting match by provided tournament id.

        Args:
            tournament_id (int): The id of the tournament.

        Returns:
            List[Match]: List of the matches.
        """


    @abstractmethod
    async def add_match(self, data: MatchIn) -> Match | None:
        """The method adding new match to the data storage.

        Args:
            data (MatchIn): The details of the new match.

        Returns:
            Match | None: Full details of the newly added match.
        """

    @abstractmethod
    async def update_match(
            self,
            match_id: int,
            data: MatchIn,
    ) -> Match | None:
        """The method updating match data in the data storage.

        Args:
            match_id (int): The id of the match.
            data (MatchIn): The details of the updated match.

        Returns:
            Match | None: The updated match details.
        """

    @abstractmethod
    async def delete_match(self, match_id: int) -> bool:
        """The method updating removing match from the data storage.

        Args:
            match_id (int): The id of the match.

        Returns:
            bool: Success of the operation.
        """
