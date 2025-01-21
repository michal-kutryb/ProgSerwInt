"""A module providing database access."""

import asyncio

import databases
import sqlalchemy
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from asyncpg.exceptions import (    # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)

from tournament_matchmaker.config import config

metadata = sqlalchemy.MetaData()

player_table = sqlalchemy.Table(
    "player",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("rank", sqlalchemy.String),
    sqlalchemy.Column("team_id", sqlalchemy.ForeignKey("team.id"), nullable = True),
)

match_table = sqlalchemy.Table(
    "match",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("tournament_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("tournament.id"), nullable = False),
    sqlalchemy.Column("team1_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("team.id"), nullable = False),
    sqlalchemy.Column("team2_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("team.id"), nullable = False),
    sqlalchemy.Column("team1_score", sqlalchemy.Integer),
    sqlalchemy.Column("team2_score", sqlalchemy.Integer),
    sqlalchemy.Column("match_date", sqlalchemy.Date),
)

tournament_table = sqlalchemy.Table(
    "tournament",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("date", sqlalchemy.Date),
    sqlalchemy.Column("max_teams_count", sqlalchemy.Integer),
    sqlalchemy.Column("preffered_rank", sqlalchemy.String),
)

team_table = sqlalchemy.Table(
    "team",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
)

tournament_team_table = sqlalchemy.Table(
    "tournament_team",
    metadata,
    sqlalchemy.Column("tournament_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("tournament.id"), nullable = False),
    sqlalchemy.Column("team_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("team.id"), nullable = False),
)


db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
)

engine = create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

database = databases.Database(
    db_uri,
    force_rollback=True,
)


async def init_db(retries: int = 5, delay: int = 5) -> None:
    """Function initializing the DB.

    Args:
        retries (int, optional): Number of retries of connect to DB.
            Defaults to 5.
        delay (int, optional): Delay of connect do DB. Defaults to 2.
    """
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
            return
        except (
                OperationalError,
                DatabaseError,
                CannotConnectNowError,
                ConnectionDoesNotExistError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")
