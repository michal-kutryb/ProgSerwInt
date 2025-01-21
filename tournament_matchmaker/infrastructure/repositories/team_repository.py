"""Module containing team repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from tournament_matchmaker.core.repositories.i_team_repository import ITeamRepository
from tournament_matchmaker.core.domains.team import Team, TeamIn
from tournament_matchmaker.db import (
    team_table,
    database,
)

class TeamRepository(ITeamRepository):
    """A class representing continent DB repository."""

    async def get_all_teams(self) -> Iterable[Any]:
        """The method getting all teams from the data storage.

        Returns:
            Iterable[Any]: Teams in the data storage.
        """

        query = (
            select(team_table)
            .order_by(team_table.c.name.asc())
        )
        teams = await database.fetch_all(query)

        return [Team.from_record(team) for team in teams]

    async def get_by_id(self, team_id: int) -> Any | None:
        """The method getting team by provided id.

        Args:
            team_id (int): The id of the team.

        Returns:
            Any | None: The team details.
        """

        team = await self._get_by_id(team_id)

        return Team.from_record(team) if team else None

    async def add_team(self, data: TeamIn) -> Any | None:
        """The method adding new team to the data storage.

        Args:
            data (TeamIn): The details of the new team.

        Returns:
            Team: Full details of the newly added team.

        Returns:
            Any | None: The newly added team.
        """

        query = team_table.insert().values(**data.model_dump())
        new_team_id = await database.execute(query)
        new_team = await self._get_by_id(new_team_id)

        return Team(**dict(new_team)) if new_team else None

    async def update_team(
            self,
            team_id: int,
            data: TeamIn,
    ) -> Any | None:
        """The method updating team data in the data storage.

        Args:
            team_id (int): The id of the team.
            data (TeamIn): The details of the updated team.

        Returns:
            Any | None: The updated team details.
        """

        if self._get_by_id(team_id):
            query = (
                team_table.update()
                .where(team_table.c.id == team_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            team = await self._get_by_id(team_id)

            return Team(**dict(team)) if team else None

        return None

    async def delete_team(self, team_id: int) -> bool:
        """The method updating removing team from the data storage.

        Args:
            team_id (int): The id of the team.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(team_id):
            query = team_table \
                .delete() \
                .where(team_table.c.id == team_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, team_id: int) -> Record | None:
        """A private method getting team from the DB based on its ID.

        Args:
            team_id (int): The ID of the team.

        Returns:
            Any | None: Team record if exists.
        """

        query = (
            team_table.select()
            .where(team_table.c.id == team_id)
            .order_by(team_table.c.name.asc())
        )

        return await database.fetch_one(query)
