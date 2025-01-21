"""Module containing team repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from tournament_matchmaker.core.domains.team import TeamIn


class ITeamRepository(ABC):
    """An abstract class representing protocol of team repository."""

    @abstractmethod
    async def get_all_teams(self) -> Iterable[Any]:
        """The abstract getting all teams from the data storage.

        Returns:
            Iterable[Any]: Teams in the data storage.
        """

    @abstractmethod
    async def get_by_id(self, team_id: int) -> Any | None:
        """The abstract getting team by provided id.

        Args:
            team_id (int): The id of the team.

        Returns:
            Any | None: The team details.
        """

    @abstractmethod
    async def add_team(self, data: TeamIn) -> Any | None:
        """The abstract adding new team to the data storage.

        Args:
            data (TeamIn): The details of the new team.

        Returns:
            Any | None: The newly added team.
        """

    @abstractmethod
    async def update_team(
            self,
            team_id: int,
            data: TeamIn,
    ) -> Any | None:
        """The abstract updating team data in the data storage.

        Args:
            team_id (int): The id of the team.
            data (TeamIn): The details of the updated team.

        Returns:
            Any | None: The updated team details.
        """

    @abstractmethod
    async def delete_team(self, team_id: int) -> bool:
        """The abstract updating removing team from the data storage.

        Args:
            team_id (int): The id of the team.

        Returns:
            bool: Success of the operation.
        """
