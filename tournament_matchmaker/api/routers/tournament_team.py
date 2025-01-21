"""A module containing tournament_team endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from tournament_matchmaker.container import Container
from tournament_matchmaker.core.domains.tournament_team import TournamentTeam, TournamentTeamIn
from tournament_matchmaker.core.services.i_team_service import ITeamService
from tournament_matchmaker.core.services.i_tournament_team_service import ITournamentTeamService
from tournament_matchmaker.core.services.i_tournament_service import ITournamentService

router = APIRouter()


@router.post("/create", response_model=TournamentTeam, status_code=201)
@inject
async def create_tournament_team(
        tournament_team: TournamentTeamIn,
        tournament_team_service: ITournamentTeamService = Depends(Provide[Container.tournament_team_service]),
        tournament_service: ITournamentService = Depends(Provide[Container.tournament_service]),
        team_service: ITeamService = Depends(Provide[Container.team_service]),
) -> dict:
    """An endpoint for adding new tournament_team.

    Args:
        tournament_team (TournamentTeamIn): The tournament_team data.
        tournament_team_service (ITournamentTeamService, optional): The injected tournament_team service dependency.
        tournament_service (ITournamentService, optional): The injected tournament service dependency.
        team_service (ITeamService, optional): The injected team service dependency.

    Returns:
        dict: The new tournament_team attributes.

    Raises:
        HTTPException: 409 if the Tournament is full.
        HTTPException: 404 if the Tournament is not found.
        HTTPException: 404 if the Team is not found.
    """

    tournament = await tournament_service.get_by_id(tournament_team.tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")

    if not await team_service.get_by_id(tournament_team.team_id):
        raise HTTPException(status_code=404, detail="Team not found")

    teams = await tournament_team_service.get_all_by_tournament_id(tournament.id)

    if len(teams) >= tournament.max_teams_count:
        raise HTTPException(status_code=409, detail="Tournament is full")

    new_tournament_team = await tournament_team_service.add_tournament_team(tournament_team)


    return new_tournament_team.model_dump() if new_tournament_team else { }


@router.get("/all", response_model=Iterable[TournamentTeam], status_code=200)
@inject
async def get_all_tournament_teams(
        service: ITournamentTeamService = Depends(Provide[Container.tournament_team_service]),
) -> Iterable:
    """An endpoint for getting all tournament_teams.

    Args:
        service (ITournamentTeamService, optional): The injected service dependency.

    Returns:
        Iterable: The tournament_team attributes collection.
    """

    tournament_teams = await service.get_all()

    return tournament_teams


@router.get("/{tournament_id}/{team_id}",response_model=TournamentTeam,status_code=200,)
@inject
async def get_tournament_team_by_tournament_id_team_id(
        tournament_id: int,
        team_id: int,
        service: ITournamentTeamService = Depends(Provide[Container.tournament_team_service]),
) -> dict | None:
    """An endpoint for getting tournament_team by tournament_id and team_id.

    Args:
        tournament_id (int): The tournament_id of the tournament_team.
        team_id (int): The team_id of the tournament_team.
        service (ITournamentTeamService, optional): The injected service dependency.

    Returns:
        dict | None: The tournament_team details.
    """

    if tournament_team := await service.get_by_tournament_id_team_id(tournament_id, team_id):
        return tournament_team.model_dump()

    raise HTTPException(status_code=404, detail="TournamentTeam not found")

@router.get("/all/team_id/{team_id}",response_model=Iterable[TournamentTeam],status_code=200,)
@inject
async def get_all_tournament_teams_by_team_id(
        team_id: int,
        service: ITournamentTeamService = Depends(Provide[Container.tournament_team_service]),
) -> Iterable[TournamentTeam]:
    """An endpoint for getting all tournament_team by team_id.

    Args:
        team_id (int): The id of the team.
        service (ITournamentTeamService, optional): The injected service dependency.

    Returns:
        Iterable: The tournament_team attributes collection.
    """

    tournament_teams = await service.get_all_by_team_id(team_id)

    return tournament_teams

@router.get("/all/tournament_id/{tournament_id}",response_model=Iterable[TournamentTeam],status_code=200,)
@inject
async def get_all_tournament_teams_by_tournament_id(
        tournament_id: int,
        service: ITournamentTeamService = Depends(Provide[Container.tournament_team_service]),
) -> Iterable[TournamentTeam]:
    """An endpoint for getting all tournament_team by tournament_id.

    Args:
        tournament_id (int): The id of the team.
        service (ITournamentTeamService, optional): The injected service dependency.

    Returns:
        Iterable: The tournament_team attributes collection.
    """

    tournament_teams = await service.get_all_by_tournament_id(tournament_id)

    return tournament_teams

@router.put("/{tournament_id}/{team_id}", response_model=TournamentTeam, status_code=201)
@inject
async def update_tournament_team(
        tournament_id: int,
        team_id: int,
        updated_tournament_team: TournamentTeamIn,
        tournament_team_service: ITournamentTeamService = Depends(Provide[Container.tournament_team_service]),
        tournament_service: ITournamentService = Depends(Provide[Container.tournament_service]),
        team_service: ITeamService = Depends(Provide[Container.team_service]),
) -> dict:
    """
    Update a tournament_team.

    Args:
        tournament_id (int): The ID of the tournament.
        team_id (int): The ID of the team.
        updated_tournament_team (TournamentTeamIn): The updated data for the tournament_team.
        tournament_team_service (ITournamentTeamService): The service for updating tournament_team.
        tournament_service (ITournamentService): The service for updating tournament.
        team_service (ITeamService): The service for updating team.

    Raises:
        HTTPException: 404 if the tournament_team does not exist.

    Returns:
        dict: The updated tournament_team details.
    """



    if await tournament_team_service.get_by_tournament_id_team_id(tournament_id=tournament_id, team_id=team_id):
        if not await tournament_service.get_by_id(updated_tournament_team.tournament_id):
            raise HTTPException(status_code=404, detail="Tournament not found")

        if not await team_service.get_by_id(updated_tournament_team.team_id):
            raise HTTPException(status_code=404, detail="Team not found")
        await tournament_team_service.update_tournament_team(
            tournament_id=tournament_id,
            team_id=team_id,
            data=updated_tournament_team,
        )
        return {**updated_tournament_team.model_dump()}

    raise HTTPException(status_code=404, detail="Tournament_Team not found")

@router.delete("/{tournament_id}/{team_id}", status_code=204)
@inject
async def delete_tournament_team(
        tournament_id: int,
        team_id: int,
        service: ITournamentTeamService = Depends(Provide[Container.tournament_team_service]),
) -> None:
    """An endpoint for deleting tournament_teams.

    Args:
        tournament_id (int): The tournament_id of the tournament_team.
        team_id (int): The tournament_id of the tournament_team.
        service (ITournamentTeamService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if tournament_team does not exist.
    """

    if await service.get_by_tournament_id_team_id(tournament_id=tournament_id, team_id=team_id):
        await service.delete_tournament_team(tournament_id, team_id)

        return

    raise HTTPException(status_code=404, detail="TournamentTeam not found")
