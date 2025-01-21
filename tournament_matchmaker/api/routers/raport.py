from tournament_matchmaker.api.routers import tournament as tournament_router
from tournament_matchmaker.core.services.i_tournament_service import ITournamentService
from tournament_matchmaker.core.services.i_player_service import IPlayerService
from tournament_matchmaker.core.services.i_team_service import ITeamService
from tournament_matchmaker.core.services.i_match_service import IMatchService
from tournament_matchmaker.core.services.i_tournament_team_service import ITournamentTeamService


from dependency_injector.wiring import inject, Provide

from fastapi import APIRouter, Depends, HTTPException

from tournament_matchmaker.container import Container

router = APIRouter()

@router.get(path="/summary", response_model=dict, status_code=200)
@inject
async def generate_summary(
        tournament_service: ITournamentService = Depends(Provide[Container.tournament_service]),
        player_service: IPlayerService = Depends(Provide[Container.player_service]),
        team_service: ITeamService = Depends(Provide[Container.team_service]),
        match_service: IMatchService = Depends(Provide[Container.match_service])
) -> dict:
    """An endpoint for generating report.

    Returns:
        dict: The summary of the whole system.
    """
    return {
        "total_tournaments": len(await tournament_service.get_all()),
        "total_players": len(await player_service.get_all()),
        "total_teams": len(await team_service.get_all()),
        "total_matches": len(await match_service.get_all()),
    }

@router.get(path="/summary/{tournament_id}", response_model=dict, status_code=200)
@inject
async def generate_tournament_summary(
        tournament_id: int,
        tournament_service: ITournamentService = Depends(Provide[Container.tournament_service]),
        tournament_team_service: ITournamentTeamService = Depends(Provide[Container.tournament_team_service])
) -> dict:
    """An endpoint for generating tournament summary.

    Args:
        tournament_id (int): The id of the tournament.

        tournament_service (ITournamentService): The injected tournament service dependency.
        tournament_team_service (ITournamentTeamService): The injected tournament_team service dependency.

    Raises:
        HTTPException: 404 if team does not exist.

    Returns:
        dict: The summary of the selected tournament
    """
    tournament = await tournament_service.get_by_id(tournament_id)

    if tournament:
        return {
            "tournament_name": tournament.name,
            "number_of_participating_teams": len(await tournament_team_service.get_all_by_tournament_id(tournament_id)),
            "winner_team": await tournament_router.get_winner(tournament_id)
        }

    raise HTTPException(status_code=404, detail="Tournament not found")
