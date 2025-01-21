"""A module containing team endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from tournament_matchmaker.container import Container
from tournament_matchmaker.core.domains.team import Team, TeamIn
from tournament_matchmaker.core.services.i_team_service import ITeamService

router = APIRouter()


@router.post("/create", response_model=Team, status_code=201)
@inject
async def create_team(
        team: TeamIn,
        service: ITeamService = Depends(Provide[Container.team_service]),
) -> dict:
    """An endpoint for adding new team.

    Args:
        team (TeamIn): The team data.
        service (ITeamService, optional): The injected service dependency.

    Returns:
        dict: The new team attributes.
    """

    new_team = await service.add_team(team)

    return new_team.model_dump() if new_team else {}


@router.get("/all", response_model=Iterable[Team], status_code=200)
@inject
async def get_all_teams(
        service: ITeamService = Depends(Provide[Container.team_service]),
) -> Iterable:
    """An endpoint for getting all teams.

    Args:
        service (ITeamService, optional): The injected service dependency.

    Returns:
        Iterable[Team]: The team attributes collection.
    """

    teams = await service.get_all()

    return teams


@router.get("/{team_id}",response_model=Team,status_code=200,)
@inject
async def get_team_by_id(
        team_id: int,
        service: ITeamService = Depends(Provide[Container.team_service]),
) -> dict | None:
    """An endpoint for getting team by id.

    Args:
        team_id (int): The id of the team.
        service (ITeamService, optional): The injected service dependency.

    Returns:
        dict | None: The team details.
    """

    if team := await service.get_by_id(team_id):
        return team.model_dump()

    raise HTTPException(status_code=404, detail="Team not found")


@router.put("/{team_id}", response_model=Team, status_code=201)
@inject
async def update_team(
        team_id: int,
        updated_team: TeamIn,
        service: ITeamService = Depends(Provide[Container.team_service]),
) -> dict:
    """An endpoint for updating team data.

    Args:
        team_id (int): The id of the team.
        updated_team (TeamIn): The updated team details.
        service (ITeamService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if team does not exist.

    Returns:
        dict: The updated team details.
    """

    if await service.get_by_id(team_id=team_id):
        await service.update_team(
            team_id=team_id,
            data=updated_team,
        )
        return {**updated_team.model_dump(), "id": team_id}

    raise HTTPException(status_code=404, detail="Team not found")


@router.delete("/{team_id}", status_code=204)
@inject
async def delete_team(
        team_id: int,
        service: ITeamService = Depends(Provide[Container.team_service]),
) -> None:
    """An endpoint for deleting teams.

    Args:
        team_id (int): The id of the team.
        service (ITeamService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if team does not exist.
    """

    if await service.get_by_id(team_id=team_id):
        await service.delete_team(team_id)

        return

    raise HTTPException(status_code=404, detail="Team not found")
