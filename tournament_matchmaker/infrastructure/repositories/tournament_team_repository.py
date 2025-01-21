"""Module containing tournament_team repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from tournament_matchmaker.core.repositories.i_tournament_team_repository import ITournamentTeamRepository
from tournament_matchmaker.core.domains.tournament_team import TournamentTeam, TournamentTeamIn
from tournament_matchmaker.db import (
    tournament_team_table,
    database,
)

class TournamentTeamRepository(ITournamentTeamRepository):
    """A class representing continent DB repository."""

    async def get_all_tournament_teams(self) -> Iterable[Any]:
        """The method getting all tournament_teams from the data storage.

        Returns:
            Iterable[Any]: TournamentTeams in the data storage.
        """

        query = (
            select(tournament_team_table)
            .order_by(tournament_team_table.c.team_id.asc())
        )
        tournament_teams = await database.fetch_all(query)

        return [TournamentTeam.from_record(tournament_team) for tournament_team in tournament_teams]

    async def get_by_tournament_id_team_id(self, tournament_id: int, team_id: int) -> Any | None:
        """The method getting tournament_team by provided id.

        Args:
            tournament_id (int): The id of the tournament.
            team_id (int): The id of the team.

        Returns:
            Any | None: The tournament_team details.
        """
        query = (
            tournament_team_table.select()
            .where(tournament_team_table.c.tournament_id == tournament_id)
            .where(tournament_team_table.c.team_id == team_id)
            .order_by(tournament_team_table.c.tournament_id.asc())
        )
        tournament_team = await database.fetch_one(query)

        return TournamentTeam.from_record(tournament_team) if tournament_team else None

    async def get_all_by_team_id(self, team_id: int) -> Iterable[Any]:
        """The method getting tournament_team by provided team_id.

        Args:
            team_id (int): The team_id of the tournament_team.

        Returns:
            Any | None: The tournament_team details.
        """

        query = (
            tournament_team_table.select()
            .where(tournament_team_table.c.team_id == team_id)
            .order_by(tournament_team_table.c.team_id.asc())
        )

        tournament_teams = await database.fetch_all(query)

        return [TournamentTeam.from_record(tournament_team) for tournament_team in tournament_teams]

    async def get_all_by_tournament_id(self, tournament_id: int) -> Iterable[Any]:
        """The method getting tournament_team by provided tournament_id.

        Args:
            tournament_id (int): The tournament_id of the tournament_team.

        Returns:
            Any | None: The tournament_team details.
        """

        query = (
            tournament_team_table.select()
            .where(tournament_team_table.c.tournament_id == tournament_id)
            .order_by(tournament_team_table.c.tournament_id.asc())
        )

        tournament_teams = await database.fetch_all(query)

        return [TournamentTeam.from_record(tournament_team) for tournament_team in tournament_teams]

    async def add_tournament_team(self, data: TournamentTeamIn) -> Any | None:
        """The method adding new tournament_team to the data storage.

        Args:
            data (TournamentTeamIn): The details of the new tournament_team.

        Returns:
            TournamentTeam: Full details of the newly added tournament_team.

        Returns:
            Any | None: The newly added tournament_team.
        """

        query = tournament_team_table.insert().values(**data.model_dump())
        await database.execute(query)
        new_tournament_team = await self.get_by_tournament_id_team_id(data.tournament_id, data.team_id)

        return TournamentTeam(**dict(new_tournament_team)) if new_tournament_team else None

    async def update_tournament_team(self, tournament_id: int, team_id: int, data: TournamentTeamIn,
    ) -> Any | None:
        """
        Update an existing tournament_team in the data storage.

        Args:
            tournament_id (int): The tournament_id of the tournament_team.
            team_id (int): The team_id of the tournament_team.
            data (TeamTournamentIn): The details of the updated team_tournament.

        Returns:
            Any | None: The updated tournament_team details.
        """

        if await self.get_by_tournament_id_team_id(tournament_id, team_id):
            query = (
                tournament_team_table.update()
                .where(tournament_team_table.c.tournament_id == tournament_id)
                .where(tournament_team_table.c.team_id == team_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            tournament_team = await self.get_by_tournament_id_team_id(tournament_id, team_id)

            return TournamentTeam(**dict(tournament_team)) if tournament_team else None

        return None

    async def delete_tournament_team(self, tournament_id: int, team_id: int) -> bool:
        """The method updating removing tournament_team from the data storage.

        Args:
            tournament_id (int): The id of the tournament.
            team_id (int): The id of the team.

        Returns:
            bool: Success of the operation.
        """
        query1 = (
            tournament_team_table.select()
            .where(tournament_team_table.c.tournament_id == tournament_id)
            .where(tournament_team_table.c.team_id == team_id)
            .order_by(tournament_team_table.c.tournament_id.asc())
        )
        tournament_team = await database.fetch_one(query1)

        if tournament_team:
            query2 = tournament_team_table \
                .delete() \
                .where(tournament_team_table.c.team_id == tournament_id)\
                .where(tournament_team_table.c.team_id == team_id)

            await database.execute(query2)

            return True

        return False
