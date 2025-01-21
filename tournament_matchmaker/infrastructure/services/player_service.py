"""Module containing player service implementation."""

from typing import Iterable

from tournament_matchmaker.core.domains.player import Player, PlayerIn
from tournament_matchmaker.core.repositories.i_player_repository import IPlayerRepository
from tournament_matchmaker.core.services.i_player_service import IPlayerService


class PlayerService(IPlayerService):
    """A class implementing the player service."""

    _player_repository: IPlayerRepository

    def __init__(self, player_repository: IPlayerRepository) -> None:
        """The initializer of the `player service`.

        Args:
            repository (IPlayerRepository): The reference to the repository.
        """
        self._player_repository = player_repository

    async def get_all(self) -> Iterable[Player]:
        """The method getting all players from the repository.

        Returns:
            Iterable[Player]: All players.
        """

        return await self._player_repository.get_all_players()

    async def get_by_id(self, player_id: int) -> Player | None:
        """The method getting player by provided id.

        Args:
            player_id (int): The id of the player.

        Returns:
            Player | None: The player details.
        """

        return await self._player_repository.get_by_id(player_id)

    async def get_all_by_team_id(self, team_id: int) -> Iterable[Player]:
        """The method getting player by provided id.

        Args:
            player_id (int): The id of the player.

        Returns:
            Player | None: The player details.
        """

        return await self._player_repository.get_all_by_team_id(team_id)

    async def add_player(self, data: PlayerIn) -> Player | None:
        """The method adding new player to the data storage.

        Args:
            data (PlayerIn): The details of the new player.

        Returns:
            Player | None: Full details of the newly added player.
        """

        return await self._player_repository.add_player(data)

    async def update_player(
            self,
            player_id: int,
            data: PlayerIn,
    ) -> Player | None:
        """The method updating player data in the data storage.

        Args:
            player_id (int): The id of the player.
            data (PlayerIn): The details of the updated player.

        Returns:
            Player | None: The updated player details.
        """

        return await self._player_repository.update_player(
            player_id=player_id,
            data=data,
        )

    async def delete_player(self, player_id: int) -> bool:
        """The method updating removing player from the data storage.

        Args:
            player_id (int): The id of the player.

        Returns:
            bool: Success of the operation.
        """

        return await self._player_repository.delete_player(player_id)
