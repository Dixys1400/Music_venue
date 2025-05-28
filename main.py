from fastapi import FastAPI
from database import Base, engine, SessionLocal
from routers import music, comments_routes






app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(music.router, prefix="/music", tags=["Playlist"])
app.include_router(comments_routes.router, prefix="/comments", tags=["Comments"])




