"""Module containing tournament repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from tournament_matchmaker.core.domains.tournament import TournamentIn


class ITournamentRepository(ABC):
    """An abstract class representing protocol of tournament repository."""

    @abstractmethod
    async def get_all_tournaments(self) -> Iterable[Any]:
        """The abstract getting all tournaments from the data storage.

        Returns:
            Iterable[Any]: Tournaments in the data storage.
        """

    @abstractmethod
    async def get_by_id(self, tournament_id: int) -> Any | None:
        """The abstract getting tournament by provided id.

        Args:
            tournament_id (int): The id of the tournament.

        Returns:
            Any | None: The tournament details.
        """

    @abstractmethod
    async def add_tournament(self, data: TournamentIn) -> Any | None:
        """The abstract adding new tournament to the data storage.

        Args:
            data (TournamentIn): The details of the new tournament.

        Returns:
            Any | None: The newly added tournament.
        """

    @abstractmethod
    async def update_tournament(
            self,
            tournament_id: int,
            data: TournamentIn,
    ) -> Any | None:
        """The abstract updating tournament data in the data storage.

        Args:
            tournament_id (int): The id of the tournament.
            data (TournamentIn): The details of the updated tournament.

        Returns:
            Any | None: The updated tournament details.
        """

    @abstractmethod
    async def delete_tournament(self, tournament_id: int) -> bool:
        """The abstract updating removing tournament from the data storage.

        Args:
            tournament_id (int): The id of the tournament.

        Returns:
            bool: Success of the operation.
        """
        