from app.core.config import settings
from app.database.engine import DatabaseEngine

db_engine = DatabaseEngine(settings.SQLALCHEMY_DATABASE_URI)
