"""Module containing tournament repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from tournament_matchmaker.core.repositories.i_tournament_repository import ITournamentRepository
from tournament_matchmaker.core.domains.tournament import Tournament, TournamentIn
from tournament_matchmaker.db import (
    tournament_table,
    database,
)

class TournamentRepository(ITournamentRepository):
    """A class representing continent DB repository."""

    async def get_all_tournaments(self) -> Iterable[Any]:
        """The method getting all tournaments from the data storage.

        Returns:
            Iterable[Any]: Tournaments in the data storage.
        """

        query = (
            select(tournament_table)
            .order_by(tournament_table.c.name.asc())
        )
        tournaments = await database.fetch_all(query)

        return [Tournament.from_record(tournament) for tournament in tournaments]

    async def get_by_id(self, tournament_id: int) -> Any | None:
        """The method getting tournament by provided id.

        Args:
            tournament_id (int): The id of the tournament.

        Returns:
            Any | None: The tournament details.
        """

        tournament = await self._get_by_id(tournament_id)

        return Tournament.from_record(tournament) if tournament else None

    async def add_tournament(self, data: TournamentIn) -> Any | None:
        """The method adding new tournament to the data storage.

        Args:
            data (TournamentIn): The details of the new tournament.

        Returns:
            Tournament: Full details of the newly added tournament.

        Returns:
            Any | None: The newly added tournament.
        """

        query = tournament_table.insert().values(**data.model_dump())
        new_tournament_id = await database.execute(query)
        new_tournament = await self._get_by_id(new_tournament_id)

        return Tournament(**dict(new_tournament)) if new_tournament else None

    async def update_tournament(
            self,
            tournament_id: int,
            data: TournamentIn,
    ) -> Any | None:
        """The method updating tournament data in the data storage.

        Args:
            tournament_id (int): The id of the tournament.
            data (TournamentIn): The details of the updated tournament.

        Returns:
            Any | None: The updated tournament details.
        """

        if self._get_by_id(tournament_id):
            query = (
                tournament_table.update()
                .where(tournament_table.c.id == tournament_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            tournament = await self._get_by_id(tournament_id)

            return Tournament(**dict(tournament)) if tournament else None

        return None

    async def delete_tournament(self, tournament_id: int) -> bool:
        """The method updating removing tournament from the data storage.

        Args:
            tournament_id (int): The id of the tournament.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(tournament_id):
            query = tournament_table \
                .delete() \
                .where(tournament_table.c.id == tournament_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, tournament_id: int) -> Record | None:
        """A private method getting tournament from the DB based on its ID.

        Args:
            tournament_id (int): The ID of the tournament.

        Returns:
            Any | None: Tournament record if exists.
        """

        query = (
            tournament_table.select()
            .where(tournament_table.c.id == tournament_id)
            .order_by(tournament_table.c.name.asc())
        )

        return await database.fetch_one(query)
    