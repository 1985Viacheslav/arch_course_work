from datetime import datetime
from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP, Date

from database.postgres_db import Base


class User(Base):
    __tablename__ = 'user'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(length=200), nullable=False)
    last_name: str = Column(String(length=200), nullable=False)
    username: str = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    registered_at: Date = Column(TIMESTAMP, default=datetime.utcnow)




