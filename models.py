from sqlalchemy import String, Integer, Float, Column
from database import Base


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, index=True)
    song = Column(String)
    desc = Column(String, nullable=True)
    auditions = Column(Integer)
    country = Column(String)
    likes = Column(Integer, default=0)


