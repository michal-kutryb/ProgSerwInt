"""Module containing team service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from tournament_matchmaker.core.domains.team import Team, TeamIn


class ITeamService(ABC):
    """A class representing team repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[Team]:
        """The method getting all teams from the repository.

        Returns:
            Iterable[Team]: All teams.
        """


    @abstractmethod
    async def get_by_id(self, team_id: int) -> Team | None:
        """The method getting team by provided id.

        Args:
            team_id (int): The id of the team.

        Returns:
            Team | None: The team details.
        """


    @abstractmethod
    async def add_team(self, data: TeamIn) -> Team | None:
        """The method adding new team to the data storage.

        Args:
            data (TeamIn): The details of the new team.

        Returns:
            Team | None: Full details of the newly added team.
        """

    @abstractmethod
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

    @abstractmethod
    async def delete_team(self, team_id: int) -> bool:
        """The method updating removing team from the data storage.

        Args:
            team_id (int): The id of the team.

        Returns:
            bool: Success of the operation.
        """
