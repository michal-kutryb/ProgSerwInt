"""Module containing player repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from tournament_matchmaker.core.repositories.i_player_repository import IPlayerRepository
from tournament_matchmaker.core.domains.player import Player, PlayerIn
from tournament_matchmaker.db import (
    player_table,
    database,
)

class PlayerRepository(IPlayerRepository):
    """A class representing continent DB repository."""

    async def get_all_players(self) -> Iterable[Any]:
        """The method getting all players from the data storage.

        Returns:
            Iterable[Any]: Players in the data storage.
        """

        query = (
            select(player_table)
            .order_by(player_table.c.name.asc())
        )
        players = await database.fetch_all(query)

        return [Player.from_record(player) for player in players]

    async def get_by_id(self, player_id: int) -> Any | None:
        """The method getting player by provided id.

        Args:
            player_id (int): The id of the player.

        Returns:
            Any | None: The player details.
        """

        player = await self._get_by_id(player_id)

        return Player.from_record(player) if player else None

    async def get_all_by_team_id(self, team_id: int) -> Iterable[Any]:
        """The abstract getting player by provided team_id.

        Args:
            team_id (int): The id of the player.

        Returns:
            Iterable[Any]: Players in the data storage assigned to selected team.
        """

        query = (
            player_table.select()
            .where(player_table.c.team_id == team_id)
            .order_by(player_table.c.name.asc())
        )

        players = await database.fetch_all(query)

        return [Player.from_record(player) for player in players]

    async def add_player(self, data: PlayerIn) -> Any | None:
        """The method adding new player to the data storage.

        Args:
            data (PlayerIn): The details of the new player.

        Returns:
            Player: Full details of the newly added player.

        Returns:
            Any | None: The newly added player.
        """

        query = player_table.insert().values(**data.model_dump())
        new_player_id = await database.execute(query)
        new_player = await self._get_by_id(new_player_id)

        return Player(**dict(new_player)) if new_player else None

    async def update_player(
            self,
            player_id: int,
            data: PlayerIn,
    ) -> Any | None:
        """The method updating player data in the data storage.

        Args:
            player_id (int): The id of the player.
            data (PlayerIn): The details of the updated player.

        Returns:
            Any | None: The updated player details.
        """

        if self._get_by_id(player_id):
            query = (
                player_table.update()
                .where(player_table.c.id == player_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            player = await self._get_by_id(player_id)

            return Player(**dict(player)) if player else None

        return None

    async def delete_player(self, player_id: int) -> bool:
        """The method updating removing player from the data storage.

        Args:
            player_id (int): The id of the player.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(player_id):
            query = player_table \
                .delete() \
                .where(player_table.c.id == player_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, player_id: int) -> Record | None:
        """A private method getting player from the DB based on its ID.

        Args:
            player_id (int): The ID of the player.

        Returns:
            Any | None: Player record if exists.
        """

        query = (
            player_table.select()
            .where(player_table.c.id == player_id)
            .order_by(player_table.c.name.asc())
        )

        return await database.fetch_one(query)
