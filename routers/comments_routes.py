from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db



router = APIRouter(prefix="/comment", tags=["Comments"])


@router.post("/comment", response_model=schemas.CommentOut)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    db_comment = models.Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment



@router.get("/comments_by_id", response_model=List[schemas.CommentOut])
def get_comments_by_id(song_id: int, db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter(models.Comment.song_id == song_id).all()
    if not comments:
        raise HTTPException(status_code=404, detail="Комментариев не найдено")
    return comments



@router.delete("/delete_comment")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Комментариев не найдено")

    db.delete(comment)
    db.commit()
    return {"message": "Комментарий удален"}



@router.post("/comment_like", response_model=schemas.CommentOut)
def comment_like(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")

    comment.likes += 1
    db.commit()
    db.refresh(comment)
    return comment


@router.get("/songs/top-comment_by_likes", response_model=schemas.CommentOut)
def get_top_comment(song_id: int, db: Session = Depends(get_db)):
    top_comment = (
        db.query(models.Comment)
        .filter(models.Comment.song_id == song_id)
        .order_by(models.Comment.likes.desc())
        .first()
    )

    if not top_comment:
        raise HTTPException(status_code=404, detail="Комментария не найдено")
    return top_comment

