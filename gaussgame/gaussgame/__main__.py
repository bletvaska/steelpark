from sqlmodel import SQLModel

from .helpers import get_db_engine
from .context import Context

# create db schema
engine = get_db_engine()
SQLModel.metadata.create_all(engine)

context = Context()
context.run()
