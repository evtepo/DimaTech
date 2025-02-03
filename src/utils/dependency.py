from typing import Annotated

from db.db_connect import get_session
from fastapi import Depends
from repository.repository import BaseRepository, get_db_repository
from sqlalchemy.ext.asyncio import AsyncSession


db_dependency = Annotated[AsyncSession, Depends(get_session)]
repository_dependency = Annotated[BaseRepository, Depends(get_db_repository)]
