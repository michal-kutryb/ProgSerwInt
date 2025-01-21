"""Module containing match service implementation."""

from typing import Iterable, List

from tournament_matchmaker.core.domains.match import Match, MatchIn
from tournament_matchmaker.core.domains.tournament import Tournament
from tournament_matchmaker.core.repositories.i_match_repository import IMatchRepository
from tournament_matchmaker.core.services.i_match_service import IMatchService


class MatchService(IMatchService):
    """A class implementing the match service."""

    _match_repository: IMatchRepository

    def __init__(self, match_repository: IMatchRepository) -> None:
        """The initializer of the `match service`.

        Args:
            repository (IMatchRepository): The reference to the repository.
        """
        self._match_repository = match_repository

    async def get_all(self) -> Iterable[Match]:
        """The method getting all matches from the repository.

        Returns:
            Iterable[Match]: All matches.
        """

        return await self._match_repository.get_all_matches()

    async def get_by_id(self, match_id: int) -> Match | None:
        """The method getting match by provided id.

        Args:
            match_id (int): The id of the match.

        Returns:
            Match | None: The match details.
        """

        return await self._match_repository.get_by_id(match_id)

    async def get_by_tournament_id(self, tournament_id: int) -> List[Match]:
        """The abstract getting match by provided tournament_id.

        Args:
            tournament_id (int): The id of the tournament.

        Returns:
            List[Match]: The list of matches
        """
        return await self._match_repository.get_by_tournament_id(tournament_id)


    async def add_match(self, data: MatchIn) -> Match | None:
        """The method adding new match to the data storage.

        Args:
            data (MatchIn): The details of the new match.

        Returns:
            Match | None: Full details of the newly added match.
        """

        return await self._match_repository.add_match(data)

    async def update_match(
            self,
            match_id: int,
            data: MatchIn,
    ) -> Match | None:
        """The method updating match data in the data storage.

        Args:
            match_id (int): The id of the match.
            data (MatchIn): The details of the updated match.

        Returns:
            Match | None: The updated match details.
        """

        return await self._match_repository.update_match(
            match_id=match_id,
            data=data,
        )

    async def delete_match(self, match_id: int) -> bool:
        """The method updating removing match from the data storage.

        Args:
            match_id (int): The id of the match.

        Returns:
            bool: Success of the operation.
        """

        return await self._match_repository.delete_match(match_id)
