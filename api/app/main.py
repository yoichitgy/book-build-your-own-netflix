import logging
from fastapi import FastAPI, Query

# Logger configuration
logging.basicConfig(
    format="[%(asctime)s][%(levelname)s] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/all/")
async def all_movies():
    return {"message": "All movies"}


@app.get("/genres/{genre}")
async def genre_movies(genre: str):
    return {"message": f"genre: {genre}"}


@app.get("/user-based/")
async def user_based(params: list[str] | None = Query(None)):
    return {"message": f"User based"}


@app.get("/item-based/{item_id}")
async def item_based(item_id: str):
    return {"message": f"item based: {item_id}"}
