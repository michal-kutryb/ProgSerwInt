"""Module containing tournament_team repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from tournament_matchmaker.core.domains.tournament_team import TournamentTeamIn


class ITournamentTeamRepository(ABC):
    """An abstract class representing protocol of tournament_team repository."""

    @abstractmethod
    async def get_all_tournament_teams(self) -> Iterable[Any]:
        """The abstract getting all tournament_teams from the data storage.

        Returns:
            Iterable[Any]: TournamentTeams in the data storage.
        """

    @abstractmethod
    async def get_by_tournament_id_team_id(self, tournament_id:int, team_id: int) -> Any | None:
        """The abstract getting tournament_team by provided combination of tournament id and team id.

        Args:
            tournament_id (int): The id of the tournament.
            team_id (int): The id of the team.

        Returns:
            Any | None: The tournament_team details.
        """

    @abstractmethod
    async def get_all_by_tournament_id(self, tournament_id: int) -> Iterable[Any]:
        """The abstract getting all tournament_teams by provided tournament id.

        Args:
            tournament_id (int): Tournament id of the tournament_team.

        Returns:
            Iterable[Any]: TournamentTeams in the data storage.
        """

    @abstractmethod
    async def get_all_by_team_id(self, team_id: int) -> Iterable[Any]:
        """The abstract getting all tournament_teams by provided team id.

        Args:
            team_id (int): Team id of the tournament_team.

        Returns:
            Iterable[Any]: TournamentTeams in the data storage.
        """


    @abstractmethod
    async def add_tournament_team(self, data: TournamentTeamIn) -> Any | None:
        """The abstract adding new tournament_team to the data storage.

        Args:
            data (TournamentTeamIn): The details of the new tournament_team.

        Returns:
            Any | None: The newly added tournament_team.
        """

    @abstractmethod
    async def update_tournament_team(self, tournament_id: int, team_id: int, data: TournamentTeamIn) -> Any | None:
        """
        Update an existing tournament_team in the data storage.

        Args:
            tournament_id (int): The tournament_id of the tournament_team.
            team_id (int): The team_id of the tournament_team.
            data (TeamTournamentIn): The details of the updated team_tournament.

        Returns:
            Any | None: The updated tournament_team details.
        """

    @abstractmethod
    async def delete_tournament_team(self, tournament_id: int, team_id: int) -> bool:
        """The abstract updating removing tournament_team from the data storage.

        Args:
            tournament_id (int): The id of the tournament.
            team_id (int): The id of the team.

        Returns:
            bool: Success of the operation.
        """

