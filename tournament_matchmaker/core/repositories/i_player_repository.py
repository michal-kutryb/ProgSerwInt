"""Module containing player repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from tournament_matchmaker.core.domains.player import PlayerIn


class IPlayerRepository(ABC):
    """An abstract class representing protocol of player repository."""

    @abstractmethod
    async def get_all_players(self) -> Iterable[Any]:
        """The abstract getting all players from the data storage.

        Returns:
            Iterable[Any]: Players in the data storage.
        """

    @abstractmethod
    async def get_by_id(self, player_id: int) -> Any | None:
        """The abstract getting player by provided id.

        Args:
            player_id (int): The id of the player.

        Returns:
            Any | None: The player details.
        """

    @abstractmethod
    async def get_all_by_team_id(self, team_id: int) -> Iterable[Any]:
        """The abstract getting player by provided team_id.

        Args:
            team_id (int): The id of the player.

        Returns:
            Iterable[Any]: Players in the data storage assigned to selected team.
        """

    @abstractmethod
    async def add_player(self, data: PlayerIn) -> Any | None:
        """The abstract adding new player to the data storage.

        Args:
            data (PlayerIn): The details of the new player.

        Returns:
            Any | None: The newly added player.
        """

    @abstractmethod
    async def update_player(
            self,
            player_id: int,
            data: PlayerIn,
    ) -> Any | None:
        """The abstract updating player data in the data storage.

        Args:
            player_id (int): The id of the player.
            data (PlayerIn): The details of the updated player.

        Returns:
            Any | None: The updated player details.
        """

    @abstractmethod
    async def delete_player(self, player_id: int) -> bool:
        """The abstract updating removing player from the data storage.

        Args:
            player_id (int): The id of the player.

        Returns:
            bool: Success of the operation.
        """
