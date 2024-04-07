import pandas as pd

item_frame = "data/movies_final.csv"


def random_items() -> list[dict]:
    movies_df = pd.read_csv(item_frame)
    movies_df = movies_df.fillna("")
    return movies_df.sample(n=10).to_dict("records")


def random_genres_items(genre: str) -> list[dict]:
    movies_df = pd.read_csv(item_frame)
    filter = movies_df["genres"].str.contains(genre, case=False)
    genre_df = movies_df[filter].fillna("")
    return genre_df.sample(n=10).to_dict("records")
