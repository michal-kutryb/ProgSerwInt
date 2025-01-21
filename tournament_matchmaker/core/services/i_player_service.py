"""Module containing player service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from tournament_matchmaker.core.domains.player import Player, PlayerIn


class IPlayerService(ABC):
    """A class representing player repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[Player]:
        """The method getting all players from the repository.

        Returns:
            Iterable[Player]: All players.
        """


    @abstractmethod
    async def get_by_id(self, player_id: int) -> Player | None:
        """The method getting player by provided id.

        Args:
            player_id (int): The id of the player.

        Returns:
            Player | None: The player details.
        """

    @abstractmethod
    async def get_all_by_team_id(self, team_id: int) -> Iterable[Player]:
        """The method getting player by provided team_id.

        Args:
            team_id (int): The id of the team.

        Returns:
            Iterable[Player]: All players assigned to the chosen team  .
        """


    @abstractmethod
    async def add_player(self, data: PlayerIn) -> Player | None:
        """The method adding new player to the data storage.

        Args:
            data (PlayerIn): The details of the new player.

        Returns:
            Player | None: Full details of the newly added player.
        """

    @abstractmethod
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

    @abstractmethod
    async def delete_player(self, player_id: int) -> bool:
        """The method updating removing player from the data storage.

        Args:
            player_id (int): The id of the player.

        Returns:
            bool: Success of the operation.
        """
