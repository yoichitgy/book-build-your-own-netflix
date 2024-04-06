import logging
import os
import sys
import time

import pandas as pd
import requests
from tqdm import tqdm

# Logger configuration
logging.basicConfig(
    format="[%(asctime)s][%(levelname)s] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def add_url(imdbId: str) -> str:
    return f"https://www.imdb.com/title/tt{imdbId}/"


def add_rating(df: pd.DataFrame) -> pd.DataFrame:
    ratings_df = pd.read_csv("data/ratings.csv")
    ratings_df["movieId"] = ratings_df["movieId"].astype(str)
    ratings_df = (
        ratings_df.groupby("movieId")
        .agg(
            rating_count=("rating", "count"),
            rating_ave=("rating", "mean"),
        )
        .reset_index()
    )
    return pd.merge(df, ratings_df, on="movieId")


def add_poster(df: pd.DataFrame) -> pd.DataFrame:
    # Get API key form .env
    api_key = os.getenv("TMDB_API_KEY")
    if api_key is None:
        logger.error("TMDB API key is not set.")
        sys.exit(1)

    for i, row in tqdm(df.iterrows(), total=df.shape[0]):
        tmdb_id = row["tmdbId"]
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"Failed to get poster for {tmdb_id}.")
            df.at[i, "poster_path"] = (
                "https://image.tmdb.org/t/p/original/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg"
            )
            continue

        try:
            path = response.json()["poster_path"]
            df.at[i, "poster_path"] = f"https://image.tmdb.org/t/p/original{path}"
            time.sleep(0.1)
        except (TypeError, KeyError) as e:
            logger.error(f"Failed to read poster for {tmdb_id}: {e}")
            df.at[i, "poster_path"] = (
                "https://image.tmdb.org/t/p/original/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg"
            )
    return df


if __name__ == "__main__":
    movies_df = pd.read_csv("data/movies.csv")
    movies_df["movieId"] = movies_df["movieId"].astype(str)
    links_df = pd.read_csv("data/links.csv", dtype=str)
    merged_df = pd.merge(movies_df, links_df, on="movieId", how="left")
    merged_df["url"] = merged_df["imdbId"].apply(add_url)
    result_df = add_rating(merged_df)
    result_df["poster_path"] = None
    result_df = add_poster(result_df)
    result_df.to_csv("data/movies_final.csv", index=None)
    print(result_df)
