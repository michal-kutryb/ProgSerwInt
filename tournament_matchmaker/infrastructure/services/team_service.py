"""Module containing team service implementation."""

from typing import Iterable

from tournament_matchmaker.core.domains.team import Team, TeamIn
from tournament_matchmaker.core.repositories.i_team_repository import ITeamRepository
from tournament_matchmaker.core.services.i_team_service import ITeamService


class TeamService(ITeamService):
    """A class implementing the team service."""

    _team_repository: ITeamRepository

    def __init__(self, team_repository: ITeamRepository) -> None:
        """The initializer of the `team service`.

        Args:
            repository (ITeamRepository): The reference to the repository.
        """
        self._team_repository = team_repository

    async def get_all(self) -> Iterable[Team]:
        """The method getting all teams from the repository.

        Returns:
            Iterable[Team]: All teams.
        """

        return await self._team_repository.get_all_teams()

    async def get_by_id(self, team_id: int) -> Team | None:
        """The method getting team by provided id.

        Args:
            team_id (int): The id of the team.

        Returns:
            Team | None: The team details.
        """

        return await self._team_repository.get_by_id(team_id)

    async def add_team(self, data: TeamIn) -> Team | None:
        """The method adding new team to the data storage.

        Args:
            data (TeamIn): The details of the new team.

        Returns:
            Team | None: Full details of the newly added team.
        """

        return await self._team_repository.add_team(data)

    async def update_team(
            self,
            team_id: int,
            data: TeamIn,
    ) -> Team | None:
        """The method updating team data in the data storage.

        Args:
            team_id (int): The id of the team.
            data (TeamIn): The details of the updated team.

        Returns:
            Team | None: The updated team details.
        """

        return await self._team_repository.update_team(
            team_id=team_id,
            data=data,
        )

    async def delete_team(self, team_id: int) -> bool:
        """The method updating removing team from the data storage.

        Args:
            team_id (int): The id of the team.

        Returns:
            bool: Success of the operation.
        """

        return await self._team_repository.delete_team(team_id)
