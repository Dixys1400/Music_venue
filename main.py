from fastapi import FastAPI
from database import Base, engine, SessionLocal
from routers import music


app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(music.router, prefix="/Music venue", tags=["Playlist"])




