import logging

from fastapi import FastAPI, Query
from recommender import item_based_recommendation, user_based_recommendation
from resolver import random_genres_items, random_items

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
    result = random_items()
    return {"result": result}


@app.get("/genres/{genre}")
async def genre_movies(genre: str):
    result = random_genres_items(genre)
    return {"result": result}


@app.get("/user-based/")
async def user_based(params: list[str] | None = Query(None)):
    input_ratings = {int(x.split(":")[0]): float(x.split(":")[1]) for x in params}
    result = user_based_recommendation(input_ratings)
    return {"result": result}


@app.get("/item-based/{item_id}")
async def item_based(item_id: str):
    result = item_based_recommendation(item_id)
    return {"result": result}
