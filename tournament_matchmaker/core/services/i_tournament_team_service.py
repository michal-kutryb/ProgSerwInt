"""Module containing tournament_team service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from tournament_matchmaker.core.domains.tournament_team import TournamentTeam, TournamentTeamIn


class ITournamentTeamService(ABC):
    """A class representing tournament_team repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[TournamentTeam]:
        """The method getting all tournament_teams from the repository.

        Returns:
            Iterable[TournamentTeam]: All tournament_teams.
        """


    @abstractmethod
    async def get_by_tournament_id_team_id(self, tournament_id: int, team_id: int) -> TournamentTeam | None:
        """The method getting tournament_team by provided tournament id and team id.

        Args:
            tournament_id (int): The id of the tournament.
            team_id (int): The id of the team.


        Returns:
            TournamentTeam | None: The tournament_team details.
        """

    @abstractmethod
    async def get_all_by_team_id(self, team_id: int) -> Iterable[TournamentTeam]:
        """The method getting tournament_team by provided team id.

        Args:
            team_id (int): The id of the team.

        Returns:
            Iterable[TournamentTeam]: All tournament_teams assigned to the chosen team.
        """

    @abstractmethod
    async def get_all_by_tournament_id(self, tournament_id: int) -> Iterable[TournamentTeam]:
        """The method getting tournament_team by provided tournament id.

        Args:
            tournament_id (int): The id of the tournament.

        Returns:
            Iterable[TournamentTeam]: All tournament_teams assigned to the chosen tournament.
        """

    @abstractmethod
    async def add_tournament_team(self, data: TournamentTeamIn) -> TournamentTeam | None:
        """The method adding new tournament_team to the data storage.

        Args:
            data (TournamentTeamIn): The details of the new tournament_team.

        Returns:
            TournamentTeam | None: Full details of the newly added tournament_team.
        """

    @abstractmethod
    async def delete_tournament_team(self, tournament_id: int, team_id: int) -> bool:
        """The method updating removing tournament_team from the data storage.

        Args:
            tournament_id (int): The id of the tournament.
            team_id (int): The id of the tournament.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
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
