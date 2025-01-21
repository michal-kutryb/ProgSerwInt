"""Module containing tournament_team service implementation."""

from typing import Iterable

from tournament_matchmaker.core.domains.tournament_team import TournamentTeam, TournamentTeamIn
from tournament_matchmaker.core.repositories.i_tournament_team_repository import ITournamentTeamRepository
from tournament_matchmaker.core.services.i_tournament_team_service import ITournamentTeamService


class TournamentTeamService(ITournamentTeamService):
    """A class implementing the tournament_team service."""

    _tournament_team_repository: ITournamentTeamRepository

    def __init__(self, tournament_team_repository: ITournamentTeamRepository) -> None:
        """The initializer of the `tournament_team service`.

        Args:
            repository (ITournamentTeamRepository): The reference to the repository.
        """
        self._tournament_team_repository = tournament_team_repository

    async def get_all(self) -> Iterable[TournamentTeam]:
        """The method getting all tournament_teams from the repository.

        Returns:
            Iterable[TournamentTeam]: All tournament_teams.
        """

        return await self._tournament_team_repository.get_all_tournament_teams()

    async def get_by_tournament_id_team_id(self, tournament_id: int, team_id: int) -> TournamentTeam | None:
        """The method getting tournament_team by provided tournament_id and team_id.

        Args:
            tournament_id (int): The tournament_id of the tournament.
            team_id (int): The tournament_id of the team.

        Returns:
            TournamentTeam | None: The tournament_team details.
        """

        return await self._tournament_team_repository.get_by_tournament_id_team_id(tournament_id, team_id)

    async def get_all_by_tournament_id(self, tournament_id: int) -> Iterable[TournamentTeam]:
        """The method getting tournament_team by provided tournament_id.

        Args:
            tournament_id (int): The tournament_id of the tournament_team.

        Returns:
            TournamentTeam | None: The tournament_team details.
        """

        return await self._tournament_team_repository.get_all_by_tournament_id(tournament_id)

    async def get_all_by_team_id(self, team_id: int) -> Iterable[TournamentTeam]:
        """The method getting tournament_team by provided team_id.

        Args:
            team_id (int): The team_id of the tournament_team.

        Returns:
            TournamentTeam | None: The tournament_team details.
        """

        return await self._tournament_team_repository.get_all_by_team_id(team_id)

    async def add_tournament_team(self, data: TournamentTeamIn) -> TournamentTeam | None:
        """The method adding new tournament_team to the data storage.

        Args:
            data (TournamentTeamIn): The details of the new tournament_team.

        Returns:
            TournamentTeam | None: Full details of the newly added tournament_team.
        """

        return await self._tournament_team_repository.add_tournament_team(data)

    async def update_tournament_team(self, tournament_id: int, team_id: int, data: TournamentTeamIn) -> TournamentTeam | None:

        """
        Update an existing tournament_team in the data storage.

        Args:
            tournament_id (int): The tournament_id of the tournament_team.
            team_id (int): The team_id of the tournament_team.
            data (TeamTournamentIn): The details of the updated team_tournament.

        Returns:
            Any | None: The updated tournament_team details.
        """

        return await self._tournament_team_repository.update_tournament_team(
            tournament_id=tournament_id,
            team_id=team_id,
            data=data,
        )

    async def delete_tournament_team(self, tournament_id: int, team_id: int) -> bool:
        """The method updating removing tournament_team from the data storage.

        Args:
            tournament_id (int): The tournament_id of the tournament_team.
            team_id (int): The team_id of the tournament_team.

        Returns:
            bool: Success of the operation.
        """

        return await self._tournament_team_repository.delete_tournament_team(tournament_id, team_id)
