"""A module containing match endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from tournament_matchmaker.container import Container
from tournament_matchmaker.core.domains.match import Match, MatchIn
from tournament_matchmaker.core.services.i_match_service import IMatchService
from tournament_matchmaker.core.services.i_team_service import ITeamService
from tournament_matchmaker.core.services.i_tournament_service import ITournamentService

router = APIRouter()


@router.post("/create", response_model=Match, status_code=201)
@inject
async def create_match(
        match: MatchIn,
        match_service: IMatchService = Depends(Provide[Container.match_service]),
        tournament_service: ITournamentService = Depends(Provide[Container.tournament_service]),
        team_service: ITeamService = Depends(Provide[Container.team_service]),
) -> dict:
    """An endpoint for adding new match.

    Args:
        match (MatchIn): The match data.
        match_service (IMatchService, optional): The injected match service dependency.
        tournament_service (ITournamentService, optional): The injected tournament service dependency.
        team_service (ITeamService, optional): The injected team service dependency.

    Returns:
        dict: The new match attributes.

    Raises:
        HTTPException: 404 if tournament does not exist.
        HTTPException: 404 if team_1 does not exist.
        HTTPException: 404 if team_2 does not exist.
    """
    if not await tournament_service.get_by_id(match.tournament_id):
        raise HTTPException(status_code=404, detail="Given tournament not found")

    if not await team_service.get_by_id(match.team1_id):
        raise HTTPException(status_code=404, detail="Given team1 not found")

    if not await team_service.get_by_id(match.team2_id):
        raise HTTPException(status_code=404, detail="Given team2 not found")

    new_match = await match_service.add_match(match)

    return new_match.model_dump() if new_match else {}


@router.get("/all", response_model=Iterable[Match], status_code=200)
@inject
async def get_all_matches(
        service: IMatchService = Depends(Provide[Container.match_service]),
) -> Iterable:
    """An endpoint for getting all matches.

    Args:
        service (IMatchService, optional): The injected service dependency.

    Returns:
        Iterable: The match attributes collection.
    """

    matches = await service.get_all()

    return matches


@router.get("/{match_id}",response_model=Match,status_code=200,)
@inject
async def get_match_by_id(
        match_id: int,
        service: IMatchService = Depends(Provide[Container.match_service]),
) -> dict | None:
    """An endpoint for getting match by id.

    Args:
        match_id (int): The id of the match.
        service (IMatchService, optional): The injected service dependency.

    Returns:
        dict | None: The match details.

    Raises:
        HTTPException: 404 if match does not exist.
    """

    if match := await service.get_by_id(match_id):
        return match.model_dump()

    raise HTTPException(status_code=404, detail="Match not found")


@router.put("/{match_id}", response_model=Match, status_code=201)
@inject
async def update_match(
        match_id: int,
        updated_match: MatchIn,
        match_service: IMatchService = Depends(Provide[Container.match_service]),
        tournament_service: ITournamentService = Depends(Provide[Container.tournament_service]),
        team_service: ITeamService = Depends(Provide[Container.team_service]),
) -> dict:
    """An endpoint for updating match data.

    Args:
        match_id (int): The id of the match.
        updated_match (MatchIn): The updated match details.
        match_service (IMatchService, optional): The injected match service dependency.
        tournament_service (ITournamentService, optional): The injected tournament service dependency.
        team_service (ITeamService, optional): The injected team service dependency.

    Raises:
        HTTPException: 404 if match does not exist.
        HTTPException: 404 if tournament does not exist.
        HTTPException: 404 if team_1 does not exist.
        HTTPException: 404 if team_2 does not exist.

    Returns:
        dict: The updated match details.
    """



    if await match_service.get_by_id(match_id=match_id):
        if not await tournament_service.get_by_id(updated_match.tournament_id):
            raise HTTPException(status_code=404, detail="Given tournament not found")

        if not await team_service.get_by_id(updated_match.team1_id):
            raise HTTPException(status_code=404, detail="Given team1 not found")

        if not await team_service.get_by_id(updated_match.team2_id):
            raise HTTPException(status_code=404, detail="Given team2 not found")

        await match_service.update_match(
            match_id=match_id,
            data=updated_match,
        )
        return {**updated_match.model_dump(), "id": match_id}

    raise HTTPException(status_code=404, detail="Match not found")


@router.delete("/{match_id}", status_code=204)
@inject
async def delete_match(
        match_id: int,
        service: IMatchService = Depends(Provide[Container.match_service]),
) -> None:
    """An endpoint for deleting matches.

    Args:
        match_id (int): The id of the match.
        service (IMatchService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if match does not exist.
    """

    if await service.get_by_id(match_id=match_id):
        await service.delete_match(match_id)

        return

    raise HTTPException(status_code=404, detail="Match not found")
