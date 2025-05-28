from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SongBase(BaseModel):
    id: int
    nickname:  str
    song: str
    desc: Optional[str] = None
    auditions: int
    country: str
    likes:  int



class SongCreate(SongBase):
    pass


class SongOut(SongBase):
    id: int

    class Config:
        orm_mode = True






class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    song_id: int

class CommentOut(CommentBase):
    id: int
    song_id: int
    created_at: datetime
    likes: int

    class Config:
        orm_mode = True






class FavoriteBase(BaseModel):
    song_id: int

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteOut(FavoriteBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
