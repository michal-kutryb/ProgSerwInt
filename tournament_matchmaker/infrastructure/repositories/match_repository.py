"""Module containing match repository implementation."""

from typing import Any, Iterable, List

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from tournament_matchmaker.core.domains.tournament import Tournament
from tournament_matchmaker.core.repositories.i_match_repository import IMatchRepository
from tournament_matchmaker.core.domains.match import Match, MatchIn
from tournament_matchmaker.db import (
    match_table,
    database,
)

class MatchRepository(IMatchRepository):
    """A class representing continent DB repository."""

    async def get_all_matches(self) -> Iterable[Any]:
        """The method getting all matches from the data storage.

        Returns:
            Iterable[Any]: Matches in the data storage.
        """

        query = (
            select(match_table)
        )
        matches = await database.fetch_all(query)

        return [Match.from_record(match) for match in matches]

    async def get_by_id(self, match_id: int) -> Any | None:
        """The method getting match by provided id.

        Args:
            match_id (int): The id of the match.

        Returns:
            Any | None: The match details.
        """

        match = await self._get_by_id(match_id)

        return Match.from_record(match) if match else None

    async def get_by_tournament_id(self, tournament_id: int) -> List[Match]:
        """The abstract getting match by provided tournament_id.

        Args:
            tournament_id (int): The id of the tournament.

        Returns:
            List[Match]: The list of matches
        """

        query = (
            match_table.select()
            .where(match_table.c.tournament_id == tournament_id)
        )

        matches = await database.fetch_all(query)

        return [Match.from_record(match) for match in matches]


    async def add_match(self, data: MatchIn) -> Any | None:
        """The method adding new match to the data storage.

        Args:
            data (MatchIn): The details of the new match.

        Returns:
            Match: Full details of the newly added match.

        Returns:
            Any | None: The newly added match.
        """

        query = match_table.insert().values(**data.model_dump())
        new_match_id = await database.execute(query)
        new_match = await self._get_by_id(new_match_id)

        return Match(**dict(new_match)) if new_match else None

    async def update_match(
            self,
            match_id: int,
            data: MatchIn,
    ) -> Any | None:
        """The method updating match data in the data storage.

        Args:
            match_id (int): The id of the match.
            data (MatchIn): The details of the updated match.

        Returns:
            Any | None: The updated match details.
        """

        if await self._get_by_id(match_id):
            query = (
                match_table.update()
                .where(match_table.c.id == match_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            match = await self._get_by_id(match_id)

            return Match(**dict(match)) if match else None

        return None

    async def delete_match(self, match_id: int) -> bool:
        """The method updating removing match from the data storage.

        Args:
            match_id (int): The id of the match.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(match_id):
            query = match_table \
                .delete() \
                .where(match_table.c.id == match_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, match_id: int) -> Record | None:
        """A private method getting match from the DB based on its ID.

        Args:
            match_id (int): The ID of the match.

        Returns:
            Any | None: Match record if exists.
        """

        query = (
            match_table.select()
            .where(match_table.c.id == match_id)
        )

        return await database.fetch_one(query)
