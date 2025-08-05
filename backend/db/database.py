""" module to define a session and base """
import os
from datetime import datetime
from typing import Annotated
from dotenv import load_dotenv

from sqlalchemy import func
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncAttrs
)
from sqlalchemy.orm import (
    DeclarativeBase, declared_attr, Mapped, mapped_column
)

# load environment variables
load_dotenv()

# database connection details
dbname = os.getenv("DB1_NAME")
user = os.getenv("DB1_USER")
host = os.getenv("DB1_HOST")
port = os.getenv("DB1_PORT")
password = os.getenv("DB1_PASS")
db_path = os.getenv("DB1_PATH")
db_engine = os.getenv("DB_ENGINE", "postgresql")
pg_base = "postgresql+asyncpg://"
SQLALCHEMY_DATABASE_URL = f"{pg_base}{user}:{password}@{host}:{port}/{dbname}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
# create anotations for models
int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(
    server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_false = Annotated[str, mapped_column(nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self) -> str:
        return f"{self.__name__.lower()}s"

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
