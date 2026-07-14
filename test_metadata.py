from app.database.base import Base
from app.models import *

print("Tables:", list(Base.metadata.tables.keys()))