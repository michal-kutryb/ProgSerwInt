"""A module containing player endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from tournament_matchmaker.container import Container
from tournament_matchmaker.core.domains.player import Player, PlayerIn
from tournament_matchmaker.core.services.i_player_service import IPlayerService
from tournament_matchmaker.core.services.i_team_service import ITeamService

router = APIRouter()


@router.post("/create", response_model=Player, status_code=201)
@inject
async def create_player(
        player: PlayerIn,
        player_service: IPlayerService = Depends(Provide[Container.player_service]),
        team_service: ITeamService = Depends(Provide[Container.team_service]),
) -> dict:
    """An endpoint for adding new player.

    Args:
        player (PlayerIn): The player data.
        player_service (IPlayerService, optional): The injected player service dependency.
        team_service (ITeamService, optional): The injected team service dependency.

    Note:
        if team_id is equal to 0, it saves as null

    Returns:
        dict: The new player attributes.

    Raises:
        HTTPException: 404 if team does not exist.
    """
    if not await team_service.get_by_id(player.team_id):
        if player.team_id == 0:
            player.team_id = None
        else:
            raise HTTPException(status_code=404, detail="Given team not found")


    new_player = await player_service.add_player(player)

    return new_player.model_dump() if new_player else {}


@router.get("/all", response_model=Iterable[Player], status_code=200)
@inject
async def get_all_players(
        service: IPlayerService = Depends(Provide[Container.player_service]),
) -> Iterable:
    """An endpoint for getting all players.

    Args:
        service (IPlayerService, optional): The injected service dependency.

    Returns:
        Iterable: The player attributes collection.
    """

    players = await service.get_all()

    return players


@router.get("/{player_id}",response_model=Player,status_code=200,)
@inject
async def get_player_by_id(
        player_id: int,
        service: IPlayerService = Depends(Provide[Container.player_service]),
) -> dict | None:
    """An endpoint for getting player by id.

    Args:
        player_id (int): The id of the player.
        service (IPlayerService, optional): The injected service dependency.

    Returns:
        dict | None: The player details.

    Raises:
        HTTPException: 404 if player does not exist.

    """

    if player := await service.get_by_id(player_id):
        return player.model_dump()

    raise HTTPException(status_code=404, detail="Player not found")


@router.get("/all/{team_id}",response_model=Iterable[Player],status_code=200,)
@inject
async def get_all_player_by_team_id(
        team_id: int,
        service: IPlayerService = Depends(Provide[Container.player_service]),
) -> Iterable[Player]:
    """An endpoint for getting all player assigned to team by team id.

    Args:
        team_id (int): The id of the team.
        service (IPlayerService, optional): The injected service dependency.

    Returns:
        Iterable: The player attributes collection.
    """

    players = await service.get_all_by_team_id(team_id)

    return players


@router.put("/{player_id}", response_model=Player, status_code=201)
@inject
async def update_player(
        player_id: int,
        updated_player: PlayerIn,
        player_service: IPlayerService = Depends(Provide[Container.player_service]),
        team_service: ITeamService = Depends(Provide[Container.team_service]),
) -> dict:
    """An endpoint for updating player data.

    Args:
        player_id (int): The id of the player.
        updated_player (PlayerIn): The updated player details.
        player_service (IPlayerService, optional): The injected player service dependency.
        team_service (ITeamService, optional): The injected team service dependency.


    Raises:
        HTTPException: 404 if player does not exist.
        HTTPException: 404 if team does not exist.

    Returns:
        dict: The updated player details.
    """

    if await player_service.get_by_id(player_id=player_id):
        if not await team_service.get_by_id(updated_player.team_id):
            raise HTTPException(status_code=404, detail="Given Team not found")
        await player_service.update_player(
            player_id=player_id,
            data=updated_player,
        )
        return {**updated_player.model_dump(), "id": player_id}

    raise HTTPException(status_code=404, detail="Player not found")


@router.delete("/{player_id}", status_code=204)
@inject
async def delete_player(
        player_id: int,
        service: IPlayerService = Depends(Provide[Container.player_service]),
) -> None:
    """An endpoint for deleting players.

    Args:
        player_id (int): The id of the player.
        service (IPlayerService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if player does not exist.
    """

    if await service.get_by_id(player_id=player_id):
        await service.delete_player(player_id)

        return

    raise HTTPException(status_code=404, detail="Player not found")
