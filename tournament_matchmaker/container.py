"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from tournament_matchmaker.infrastructure.repositories.team_repository import TeamRepository
from tournament_matchmaker.infrastructure.services.team_service import TeamService

from tournament_matchmaker.infrastructure.repositories.player_repository import PlayerRepository
from tournament_matchmaker.infrastructure.services.player_service import PlayerService

from tournament_matchmaker.infrastructure.repositories.tournament_repository import TournamentRepository
from tournament_matchmaker.infrastructure.services.tournament_service import TournamentService

from tournament_matchmaker.infrastructure.repositories.match_repository import MatchRepository
from tournament_matchmaker.infrastructure.services.match_service import MatchService

from tournament_matchmaker.infrastructure.repositories.tournament_team_repository import TournamentTeamRepository
from tournament_matchmaker.infrastructure.services.tournament_team_service import TournamentTeamService

class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    team_repository = Singleton(TeamRepository)
    player_repository = Singleton(PlayerRepository)
    tournament_repository = Singleton(TournamentRepository)
    match_repository = Singleton(MatchRepository)
    tournament_team_repository = Singleton(TournamentTeamRepository)

    team_service = Factory(
        TeamService,
        team_repository=team_repository,
    )

    player_service = Factory(
        PlayerService,
        player_repository=player_repository,
    )

    tournament_team_service = Factory(
        TournamentTeamService,
        tournament_team_repository=tournament_team_repository,
    )

    tournament_service = Factory(
        TournamentService,
        tournament_repository=tournament_repository,
    )

    match_service = Factory(
        MatchService,
        match_repository=match_repository,
    )

