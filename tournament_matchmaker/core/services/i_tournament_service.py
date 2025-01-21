"""Module containing tournament service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from tournament_matchmaker.core.domains.tournament import Tournament, TournamentIn


class ITournamentService(ABC):
    """A class representing tournament repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[Tournament]:
        """The method getting all tournaments from the repository.

        Returns:
            Iterable[Tournament]: All tournaments.
        """


    @abstractmethod
    async def get_by_id(self, tournament_id: int) -> Tournament | None:
        """The method getting tournament by provided id.

        Args:
            tournament_id (int): The id of the tournament.

        Returns:
            Tournament | None: The tournament details.
        """


    @abstractmethod
    async def add_tournament(self, data: TournamentIn) -> Tournament | None:
        """The method adding new tournament to the data storage.

        Args:
            data (TournamentIn): The details of the new tournament.

        Returns:
            Tournament | None: Full details of the newly added tournament.
        """

    @abstractmethod
    async def update_tournament(
            self,
            tournament_id: int,
            data: TournamentIn,
    ) -> Tournament | None:
        """The method updating tournament data in the data storage.

        Args:
            tournament_id (int): The id of the tournament.
            data (TournamentIn): The details of the updated tournament.

        Returns:
            Tournament | None: The updated tournament details.
        """

    @abstractmethod
    async def delete_tournament(self, tournament_id: int) -> bool:
        """The method updating removing tournament from the data storage.

        Args:
            tournament_id (int): The id of the tournament.

        Returns:
            bool: Success of the operation.
        """
