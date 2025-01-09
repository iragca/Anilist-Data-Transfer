"""This module provides utility functions for preprocessing anime and review data
into Polars DataFrames.

Functions:
    anime(table: pl.DataFrame) -> pl.DataFrame:
        Preprocess the given anime table to a Polars DataFrame by unnesting
        nested columns and converting date columns.

    reviews(table: pl.DataFrame) -> pl.DataFrame:
        Preprocess the given reviews table to a Polars DataFrame by unnesting
        nested columns and converting date columns.
"""

import polars as pl
from polars.exceptions import ColumnNotFoundError, SchemaError


def anime(table: pl.DataFrame) -> pl.DataFrame:
    """Preprocess the given table to a Polars DataFrame.

    Nested columns are unnested and the date is converted to a Polars Date.
    Args:
        table (pl.DataFrame): The table containing the data to preprocess.

    Returns:
        polars.DataFrame: The preprocessed Polars DataFrame.
    """
    try:
        return (
            table.select(
                [
                    "id",
                    "season",
                    "seasonYear",
                    "title",
                    "format",
                    "meanScore",
                    "popularity",
                    "episodes",
                    "favourites",
                    "duration",
                    "startDate",
                    "endDate",
                ]
            )
            .unnest(["title", "startDate"])
            .with_columns(
                [
                    (
                        pl.col("year").cast(pl.Utf8)
                        + "-"
                        + pl.col("month").cast(pl.Utf8)
                        + "-"
                        + pl.col("day").cast(pl.Utf8)
                    )
                    .str.strptime(pl.Date, "%Y-%m-%d")
                    .alias("StartDate")
                ]
            )
            .drop(["day", "month", "year"])
            .unnest(["endDate"])
            .with_columns(
                [
                    (
                        pl.col("year").cast(pl.Utf8)
                        + "-"
                        + pl.col("month").cast(pl.Utf8)
                        + "-"
                        + pl.col("day").cast(pl.Utf8)
                    )
                    .str.strptime(pl.Date, "%Y-%m-%d")
                    .alias("EndDate")
                ]
            )
            .drop(["day", "month", "year"])
            .rename(
                {
                    "id": "AnimeID",
                    "english": "EnglishTitle",
                    "native": "NativeTitle",
                    "romaji": "RomajiTitle",
                    "season": "Season",
                    "seasonYear": "SeasonYear",
                    "format": "Format",
                    "meanScore": "MeanScore",
                    "popularity": "Popularity",
                    "episodes": "Episodes",
                    "duration": "Duration",
                    "favourites": "Favourites",
                    "StartDate": "StartDate",
                    "EndDate": "EndDate",
                }
            )
        )
    except SchemaError:
        return 501
    except Exception as e:
        print(f"Error preprocessing ANIME: {e}")
        return None


def reviews(table: pl.DataFrame) -> pl.DataFrame:
    """Preprocess the given table to a Polars DataFrame.

    Nested columns are unnested and the date is converted to a Polars Date.
    Args:
        table (pl.DataFrame): The table containing the data to preprocess.

    Returns:
        polars.DataFrame: The preprocessed Polars DataFrame.
    """

    try:
        return (
            table.select(["reviews"])
            .unnest("reviews")
            .explode("nodes")
            .unnest("nodes")
            .rename(
                {
                    "id": "ReviewID",
                }
            )
            .with_columns(
                [
                    pl.from_epoch("createdAt").alias("ReviewCreatedAt"),
                    pl.from_epoch("updatedAt").alias("ReviewUpdatedAt"),
                ]
            )
            .drop(["createdAt", "updatedAt"])
            .unnest("media")
            .rename({"id": "AnimeID"})
            .unnest(["user"])
            .rename(
                {
                    "id": "UserID",
                    "rating": "Rating",
                    "ratingAmount": "RatingAmount",
                    "body": "Body",
                    "summary": "Summary",
                    "season": "Season",
                    "seasonYear": "SeasonYear",
                }
            )
            .drop(["avatar", "name", "donatorTier", "createdAt", "donatorBadge"])
            .select(
                [
                    "ReviewID",
                    "Rating",
                    "RatingAmount",
                    "Body",
                    "Summary",
                    "ReviewCreatedAt",
                    "ReviewUpdatedAt",
                    "AnimeID",
                    "Season",
                    "SeasonYear",
                    "UserID",
                ]
            )
        )
    except SchemaError:
        return 501
    except ColumnNotFoundError:
        return None
    except Exception as e:
        print(f"Error preprocessing REVIEWS: {e}")
        return None


def web_assets(table):
    try:
        return (
            table.select(
                [
                    "id",
                    "season",
                    "seasonYear",
                    "bannerImage",
                    "coverImage",
                    "siteUrl",
                    "trailer",
                ]
            )
            .unnest(["coverImage"])
            .rename(
                {
                    "id": "AnimeID",
                    "season": "Season",
                    "seasonYear": "SeasonYear",
                    "bannerImage": "Banner",
                    "medium": "MediumCover",
                    "large": "LargeCover",
                    "extraLarge": "ExtraLargeCover",
                    "color": "Color",
                    "siteUrl": "SiteURL",
                    "trailer": "Trailer",
                }
            )
        )
    except SchemaError:
        return 501
    except Exception as e:
        print(f"Error preprocessing WEB ASSETS: {e}")
        return None


def studios(table):
    try:
        return (
            table.select(["studios"])
            .unnest("studios")
            .explode("nodes")
            .unnest("nodes")
            .rename({"id": "StudioID", "name": "StudioName"})
            .unnest("media")
            .explode("nodes")
            .unnest("nodes")
            .rename(
                {
                    "id": "AnimeID",
                    "season": "Season",
                    "seasonYear": "SeasonYear",
                }
            )
            .select(["AnimeID", "Season", "SeasonYear", "StudioID", "StudioName"])
        )
    except SchemaError:
        return 501
    except Exception as e:
        print(f"Error preprocessing STUDIOS: {e}")
        return None


def genres(table):
    try:
        return (
            table.select(
                [
                    "genres",
                    "id",
                    "season",
                    "seasonYear",
                ]
            )
            .explode("genres")
            .rename(
                {
                    "id": "AnimeID",
                    "season": "Season",
                    "seasonYear": "SeasonYear",
                    "genres": "Genre",
                }
            )
        )
    except SchemaError:
        return 501
    except Exception as e:
        print(f"Error preprocessing GENRES: {e}")
        return None


def tags(table):
    try:
        return (
            table.select(["tags", "id", "season", "seasonYear"])
            .rename({"id": "AnimeID"})
            .explode("tags")
            .unnest("tags")
            .rename(
                {
                    "id": "TagID",
                    "isAdult": "IsAdult",
                    "category": "Category",
                    "description": "Description",
                    "season": "Season",
                    "seasonYear": "SeasonYear",
                }
            )
        )
    except SchemaError:
        return 501
    except Exception as e:
        print(f"Error preprocessing TAGS: {e}")
        return None


def users(table):
    try:
        return (
            table.select(["reviews"])
            .unnest("reviews")
            .explode("nodes")
            .unnest("nodes")
            .drop(
                [
                    "media",
                    "id",
                    "rating",
                    "ratingAmount",
                    "body",
                    "summary",
                    "createdAt",
                    "updatedAt",
                ]
            )
            .unnest("user")
            .unnest("avatar")
            .with_columns([pl.from_epoch("createdAt").alias("UserCreatedAt")])
            .rename(
                {
                    "id": "UserID",
                    "name": "Username",
                    "donatorTier": "DonatorTier",
                    "donatorBadge": "DonatorBadge",
                    "large": "LargeAvatar",
                    "medium": "MediumAvatar",
                }
            )
            .select(
                [
                    "UserID",
                    "Username",
                    "DonatorTier",
                    "DonatorBadge",
                    "UserCreatedAt",
                    "LargeAvatar",
                    "MediumAvatar",
                ]
            )
        )
    except SchemaError:
        return 501
    except Exception as e:
        print(f"Error preprocessing USERS: {e}")
        return None


def status(table):
    try:
        return (
            table.select(
                [
                    "id",
                    "season",
                    "seasonYear",
                    "stats",
                ]
            )
            .unnest("stats")
            .explode("statusDistribution")
            .unnest("statusDistribution")
            .rename(
                {
                    "id": "AnimeID",
                    "season": "Season",
                    "seasonYear": "SeasonYear",
                    "amount": "AmountOfUsers",
                    "status": "UserStatus",
                }
            )
        )
    except SchemaError:
        return 501
    except Exception as e:
        print(f"Error preprocessing STATS: {e}")
        return None
