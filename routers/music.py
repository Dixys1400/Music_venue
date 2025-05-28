from html.parser import HTMLParser

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import models
import schemas
from database import get_db
from models import Song



router = APIRouter()




@router.post("/song_create", response_model=schemas.SongOut)
def create_song(song: schemas.SongCreate, db: Session = Depends(get_db)):
    db_song = models.Song(**song.dict())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song




@router.get("/songs", response_model=list[schemas.SongOut])
def get_all_songs(db: Session = Depends(get_db)):
    return db.query(models.Song).all()



@router.get("/songs_by_id", response_model=schemas.SongOut)
def get_car_id(song_id: int, db: Session = Depends(get_db)):
    song_id = db.query(models.Song).filter(models.Song.id == song_id).first()
    if not song_id:
        raise HTTPException(status_code=404, detail="Трек не найден")
    return song_id



@router.get("/filter", response_model=List[schemas.SongOut])
def filter_by_auditions(
        max_auditions: Optional[float] = Query(None, description="Максимальное число"),
        min_auditions: Optional[float] = Query(None, description="Минимаотное число"),
        db: Session = Depends(get_db)
):
    query = db.query(Song)

    if max_auditions is not None:
        query = query.filter(Song.auditions <= max_auditions)
    if min_auditions is not None:
        query = query.filter(Song.auditions >= min_auditions)

    results = query.all()
    if not results:
        raise HTTPException(status_code=404, detail="Трек не найден")
    return results




@router.post("/song_like", response_model=schemas.SongOut)
def like_to_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(models.Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Трек не найден")

    song.likes += 1
    db.commit()
    db.refresh(song)
    return song


@router.get("/song_by_author", response_model=List[schemas.SongOut])
def song_by_author(
        nickname: str = Query(..., descrition="Название артиста"),
        db: Session = Depends(get_db)
):
    song = db.query(Song).filter(models.Song.nickname == nickname).all()
    if not song:
        raise HTTPException(status_code=404, detail="Трек не найден")
    return song



@router.get("/songs_by_country", response_model=List[schemas.SongOut])
def song_by_region(
        country: str = Query(..., description="Страна"),
        db: Session = Depends(get_db)
):
    song = db.query(Song).filter(models.Song.country == country).all()
    if not song:
        raise HTTPException(status_code=404, detail="Треки не найдены")
    return song






@router.delete("/delete_song")
def delete_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Трек не найден")

    db.delete(song)
    db.commit()
    return {"message": "Трек удален"}






@router.get("/top5_songs_by_likes", response_model=List[schemas.SongOut])
def get_top5_songs_by_likes(db: Session = Depends(get_db)):
    top_songs = db.query(models.Song).order_by(models.Song.likes.desc()).limit(5).all()
    if not top_songs:
        raise HTTPException(status_code=404, detail="Треки не найдены")
    return top_songs


@router.get("/top5_songs_by_auditions", response_model=List[schemas.SongOut])
def get_top5_songs_by_auditions(db: Session = Depends(get_db)):
    top_songs_au = db.query(models.Song).order_by(models.Song.auditions.desc()).limit(5).all()
    if not top_songs_au:
        raise HTTPException(status_code=404, detail="Треки не найдены")
    return top_songs_au



