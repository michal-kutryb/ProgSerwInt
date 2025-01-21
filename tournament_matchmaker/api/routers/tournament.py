"""A module containing tournament endpoints."""
from datetime import datetime
from itertools import combinations

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from tournament_matchmaker.container import Container
from tournament_matchmaker.core.domains.match import MatchIn
from tournament_matchmaker.core.domains.team import Team
from tournament_matchmaker.core.domains.tournament import Tournament, TournamentIn
from tournament_matchmaker.core.services.i_match_service import IMatchService
from tournament_matchmaker.core.services.i_tournament_service import ITournamentService
from tournament_matchmaker.core.services.i_tournament_team_service import ITournamentTeamService
from tournament_matchmaker.core.services.i_team_service import ITeamService

router = APIRouter()


@router.post("/create", response_model=Tournament, status_code=201)
@inject
async def create_tournament(
        tournament: TournamentIn,
        service: ITournamentService = Depends(Provide[Container.tournament_service]),
) -> dict:
    """An endpoint for adding new tournament.

    Args:
        tournament (TournamentIn): The tournament data.
        service (ITournamentService, optional): The injected service dependency.

    Returns:
        dict: The new tournament attributes.
    """

    new_tournament = await service.add_tournament(tournament)

    return new_tournament.model_dump() if new_tournament else {}


@router.get("/all", response_model=Iterable[Tournament], status_code=200)
@inject
async def get_all_tournaments(
        service: ITournamentService = Depends(Provide[Container.tournament_service]),
) -> Iterable:
    """An endpoint for getting all tournaments.

    Args:
        service (ITournamentService, optional): The injected service dependency.

    Returns:
        Iterable: The tournament attributes collection.
    """

    tournaments = await service.get_all()

    return tournaments


@router.get("/{tournament_id}",response_model=Tournament,status_code=200,)
@inject
async def get_tournament_by_id(
        tournament_id: int,
        service: ITournamentService = Depends(Provide[Container.tournament_service]),
) -> dict | None:
    """An endpoint for getting tournament by id.

    Args:
        tournament_id (int): The id of the tournament.
        service (ITournamentService, optional): The injected service dependency.

    Returns:
        dict | None: The tournament details.

    Raises:
        HTTPException: 404 if tournament does not exist.

    """

    if tournament := await service.get_by_id(tournament_id):
        return tournament

    raise HTTPException(status_code=404, detail="Tournament not found")


@router.put("/{tournament_id}", response_model=Tournament, status_code=201)
@inject
async def update_tournament(
        tournament_id: int,
        updated_tournament: TournamentIn,
        service: ITournamentService = Depends(Provide[Container.tournament_service]),
) -> dict:
    """An endpoint for updating tournament data.

    Args:
        tournament_id (int): The id of the tournament.
        updated_tournament (TournamentIn): The updated tournament details.
        service (ITournamentService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if tournament does not exist.

    Returns:
        dict: The updated tournament details.
    """

    if await service.get_by_id(tournament_id=tournament_id):
        await service.update_tournament(
            tournament_id=tournament_id,
            data=updated_tournament,
        )
        return {**updated_tournament.model_dump(), "id": tournament_id}

    raise HTTPException(status_code=404, detail="Tournament not found")


@router.delete("/{tournament_id}", status_code=204)
@inject
async def delete_tournament(
        tournament_id: int,
        service: ITournamentService = Depends(Provide[Container.tournament_service]),
) -> None:
    """An endpoint for deleting tournaments.

    Args:
        tournament_id (int): The id of the tournament.
        service (ITournamentService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if tournament does not exist.
    """

    if await service.get_by_id(tournament_id=tournament_id):
        await service.delete_tournament(tournament_id)

        return

    raise HTTPException(status_code=404, detail="Tournament not found")

@router.post("/end_recruiting/{tournament_id}", status_code=204)
@inject
async def end_recruiting(
        tournament_id: int,
        tournament_service: ITournamentService = Depends(Provide[Container.tournament_service]),
        tournament_team_service: ITournamentTeamService = Depends(Provide[Container.tournament_team_service]),
        match_service: IMatchService = Depends(Provide[Container.match_service]),
) -> None:
    """An endpoint for ending recruitment for the tournament.

    Args:
        tournament_id (int): The id of the tournament.
        tournament_service (ITournamentService): The injected tournament service dependency.
        tournament_team_service (ITournamentTeamService): The injected tournament team service dependency.
        match_service (IMatchService): The injected match service dependency.

    """
    tournament = await tournament_service.get_by_id(tournament_id)
    tournament_teams = await tournament_team_service.get_all_by_tournament_id(tournament.id)
    team_ids = [
        team.team_id for team in tournament_teams
    ]

    unique_combinations = combinations(team_ids, 2)

    for combination in unique_combinations:
        await match_service.add_match(MatchIn(
            tournament_id=tournament.id,
            team1_id=combination[0],
            team2_id=combination[1],
            team1_score=0,
            team2_score=0,
            match_date=tournament.date,
        ))

@router.get("/get_winner/{tournament_id}", response_model=Team | dict, status_code=200)
@inject
async def get_winner(
        tournament_id: int,
        team_service: ITeamService = Depends(Provide[Container.team_service]),
        match_service: IMatchService = Depends(Provide[Container.match_service]),
        tournament_service: ITournamentService = Depends(Provide[Container.tournament_service]),

) -> Team | dict:
    """An endpoint for getting winner of the selected tournament by team_id.

    Args:
        tournament_id (int): The id of the tournament.
        team_service (ITeamService): The injected team service dependency.
        match_service (IMatchService): The injected match service dependency.
        tournament_service (ITournamentService): The injected tournament service dependency.

    Returns:
        Team: Object team with data about winner team.

    Raises:
        HTTPException: 404 if tournament does not exist.
    """

    if not await tournament_service.get_by_id(tournament_id):
        raise HTTPException(status_code=404, detail="Tournament not found")

    matches = await match_service.get_by_tournament_id(tournament_id)

    if len(matches) == 0:
        return {}

    winners = {}

    for match in matches:
        winner_id = match.get_winner_team_id()

        if winner_id not in winners:
            winners[winner_id] = 0
        else:
            winners[winner_id] += 1

    total_winner_id = max(winners, key=winners.get)

    team = await team_service.get_by_id(total_winner_id)

    return team if team else {}

