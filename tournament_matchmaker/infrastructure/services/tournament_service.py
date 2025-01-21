"""Module containing tournament service implementation."""

from typing import Iterable

from tournament_matchmaker.core.domains.tournament import Tournament, TournamentIn
from tournament_matchmaker.core.repositories.i_team_repository import ITeamRepository
from tournament_matchmaker.core.repositories.i_tournament_repository import ITournamentRepository
from tournament_matchmaker.core.repositories.i_tournament_team_repository import ITournamentTeamRepository
from tournament_matchmaker.core.services.i_team_service import ITeamService
from tournament_matchmaker.core.services.i_tournament_service import ITournamentService
from tournament_matchmaker.core.services.i_tournament_team_service import ITournamentTeamService


class TournamentService(ITournamentService):
    """A class implementing the tournament service."""

    _tournament_repository: ITournamentRepository

    def __init__(
            self,
            tournament_repository: ITournamentRepository,
    ) -> None:
        """The initializer of the `tournament service`.

        Args:
            repository (ITournamentRepository): The reference to the repository.
        """
        self._tournament_repository = tournament_repository

    async def get_all(self) -> Iterable[Tournament]:
        """The method getting all tournaments from the repository.

        Returns:
            Iterable[Tournament]: All tournaments.
        """

        return await self._tournament_repository.get_all_tournaments()

    async def get_by_id(self, tournament_id: int) -> Tournament | None:
        """The method getting tournament by provided id.

        Args:
            tournament_id (int): The id of the tournament.

        Returns:
            Tournament | None: The tournament details.
        """

        return await self._tournament_repository.get_by_id(tournament_id)

    async def add_tournament(self, data: TournamentIn) -> Tournament | None:
        """The method adding new tournament to the data storage.

        Args:
            data (TournamentIn): The details of the new tournament.

        Returns:
            Tournament | None: Full details of the newly added tournament.
        """

        return await self._tournament_repository.add_tournament(data)

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

        return await self._tournament_repository.update_tournament(
            tournament_id=tournament_id,
            data=data,
        )

    async def delete_tournament(self, tournament_id: int) -> bool:
        """The method updating removing tournament from the data storage.

        Args:
            tournament_id (int): The id of the tournament.

        Returns:
            bool: Success of the operation.
        """

        return await self._tournament_repository.delete_tournament(tournament_id)
