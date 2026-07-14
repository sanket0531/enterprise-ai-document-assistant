from sqlalchemy import create_engine, inspect

from app.core.config import settings
from app.database.base import Base
from app.models import *

print("=" * 60)
print("DATABASE URL")
print(settings.database_url)
print("=" * 60)

engine = create_engine(settings.database_url)

with engine.connect() as conn:
    db = conn.exec_driver_sql("SELECT DB_NAME()").scalar()
    print("Current Database:", db)

print("=" * 60)

print("SQLAlchemy Metadata Tables:")
print(list(Base.metadata.tables.keys()))

print("=" * 60)

inspector = inspect(engine)

print("Actual Database Tables:")
print(inspector.get_table_names())

print("=" * 60)