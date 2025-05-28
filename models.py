from datetime import datetime

from sqlalchemy import String, Integer, Float, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship

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

    comments = relationship("Comment", back_populates="song", cascade="all, delete")




class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey("songs.id"))
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    likes = Column(Integer, default=0)

    song = relationship("Song", back_populates="comments")



