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


