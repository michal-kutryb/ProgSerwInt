from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from tournament_matchmaker.api.routers.team import router as team_router
from tournament_matchmaker.api.routers.player import router as player_router
from tournament_matchmaker.api.routers.tournament import router as tournament_router
from tournament_matchmaker.api.routers.match import router as match_router
from tournament_matchmaker.api.routers.tournament_team import router as tournament_team_router
from tournament_matchmaker.api.routers.raport import router as raport_router

from tournament_matchmaker.container import Container
from tournament_matchmaker.db import database
from tournament_matchmaker.db import init_db

container = Container()
container.wire(modules=[
    "tournament_matchmaker.api.routers.team",
    "tournament_matchmaker.api.routers.player",
    "tournament_matchmaker.api.routers.tournament",
    "tournament_matchmaker.api.routers.match",
    "tournament_matchmaker.api.routers.tournament_team",
    "tournament_matchmaker.api.routers.raport",
])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(team_router, prefix="/team")
app.include_router(player_router, prefix="/player")
app.include_router(tournament_router, prefix="/tournament")
app.include_router(match_router, prefix="/match")
app.include_router(tournament_team_router, prefix="/tournament_team")
app.include_router(raport_router, prefix="/raport")
