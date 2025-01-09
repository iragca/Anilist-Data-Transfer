"""
This script retrieves anime and review data from Anilist for
the specified range of years and seasons,
processes the data, and inserts it into a DuckDB database.

Usage:
    # From the project root directory
    $ python data_transfer.py <inclusive: start_year> <exclusive: end_year> <optional: cooldown>

Arguments:
    start_year (int): The starting year for data retrieval.
    end_year (int): The ending year for data retrieval.

    Optional:
        COOLDOWN (int): The cooldown period between API requests (default: 10 seconds).
Modules:
    time: Provides various time-related functions.
    sys: Provides access to some variables used or maintained by the interpreter.
    duckdb: A fast, embeddable SQL OLAP database management system.
    tqdm: A fast, extensible progress bar for Python.
    utils.fetch_data: Custom module to fetch data from Anilist.
    utils.preprocess: Custom module to preprocess anime and review data.
Functions:
    fetch_from: Fetches data from Anilist using a GraphQL query.
    preprocess_<table>: Processes the fetched specific table data.

Notes:
    - The script must be run directly and not imported as a module.
    - The script requires a GraphQL query file located at 'src/utils/api_query.graphql'.
    - The script includes a cooldown period between API requests to avoid rate limiting. Recommended cooldown: 10 seconds.
"""

import sys
import time

import duckdb
from tqdm import tqdm

from utils import preprocess
from utils.custom_exceptions import NoAnimeEntriesFound
from utils.fetch_data import fetch_from
from utils.insert_data import insert_data

if __name__ != "__main__":
    sys.exit("This script must be run directly.")

if len(sys.argv) > 1:
    start_year = int(sys.argv[1])
    end_year = int(sys.argv[2])
    COOLDOWN = int(sys.argv[3]) if len(sys.argv) > 3 else 10
else:
    sys.exit(
        (
        "Please provide a start and end year as kwargs. "
        "python <inclusive: start_year> <exclusive: end_year> <optional: cooldown>"
        )
        )

## GraphQL query to retrieve data from Anilist
with open(r"src/utils/api_query.graphql", "r", encoding="UTF-8") as file:
    QUERY = file.read()

YEARS = range(start_year, end_year)
SEASONS = {
    "WINTER": "❄️",
    "SPRING": "🌸",
    "SUMMER": "🌞",
    "FALL": "🍂",
}

YEAR_BAR = tqdm(YEARS, position=0, leave=False, colour="#60D850")
for year in YEARS:
    YEAR_BAR.set_description(f"Fetching {year}")

    SEASON_BAR = tqdm(SEASONS, position=1, leave=False, colour="#22351F")
    for season, emoji in SEASONS.items():
        tqdm.write(f"===== {emoji}  {season} {year} =====")
        SEASON_BAR.set_description(f"Fetching {season}")

        try:
            buffer = fetch_from(
                url="https://graphql.anilist.co", query=QUERY, year=year, season=season
            )

            if type(buffer) is tuple:
                raise NoAnimeEntriesFound(
                    f"🟨 No anime entries found for {year} {season}. "
                    f"Requests remaining: {buffer[0]}/{buffer[1]}"
                )

            def handle_insert(data, table, year, season, conn):
                """Handle the insertion of data into the database.

                Args:
                    data (DataFrame): The data to be inserted.
                    data_type (str): The type of data being inserted
                                    (e.g., 'anime shows', 'reviews').
                    year (int): The year of the data.
                    season (str): The season of the data
                                (e.g., 'spring', 'summer', 'fall', 'winter').

                Returns:
                    None
                """
                try:
                    generator = (
                        data.iter_rows()
                    )  # Raises an attribute error if data == 501
                    try:
                        for row in generator:
                            insert_status = insert_data(row=row, table=table, conn=conn)
                            if insert_status == 404:
                                tqdm.write(
                                    f"🟨 {row} for {table.upper()} already exists"
                                )
                            elif insert_status == 500:
                                tqdm.write(
                                    f"🟥 Error inserting {row} for {table.upper()} for {season} {year}"
                                )
                                continue
                    except Exception as e:
                        tqdm.write(f"🟥 Error inserting data: {type(e).__name__}: {e}")

                except AttributeError:
                    tqdm.write(f"🟨 No data found for {table.upper()}")
                except Exception as e:
                    tqdm.write(f"🟥 Error: {type(e).__name__}: {e}")

            try:
                tqdm.write("🟦 Inserting data...")
                conn = duckdb.connect("src/anilist.duckdb")
                handle_insert(preprocess.anime(buffer), "Anime", year, season, conn)
                handle_insert(preprocess.genres(buffer), "Genre", year, season, conn)
                handle_insert(preprocess.reviews(buffer), "Review", year, season, conn)
                handle_insert(preprocess.status(buffer), "Status", year, season, conn)
                handle_insert(preprocess.studios(buffer), "Studio", year, season, conn)
                handle_insert(preprocess.tags(buffer), "Tag", year, season, conn)
                handle_insert(preprocess.users(buffer), "User", year, season, conn)
                handle_insert(
                    preprocess.web_assets(buffer), "WebAsset", year, season, conn
                )
            except KeyboardInterrupt:
                conn.close()
                tqdm.write("x--- Closing connection ---x")
                raise KeyboardInterrupt
            except Exception as e:
                conn.close()
                tqdm.write(f"🟥 Caught an error: {type(e).__name__}: {e}")
            else:
                conn.commit()
                conn.close()
                tqdm.write(f"🟩 All data inserted for {season} {year}!")

            SEASON_BAR.update(1)

            try:
                # TODO: Refactor the cooldown as a function
                COOLDOWN_BAR = tqdm(
                    range(0, COOLDOWN), position=2, leave=False, desc="Cooldown"
                )
                for i in range(0, COOLDOWN):
                    COOLDOWN_BAR.set_description(f"⏱ Cooldown: {COOLDOWN-i} sec(s)")
                    time.sleep(1)
                    COOLDOWN_BAR.update(1)

            except KeyboardInterrupt:
                raise KeyboardInterrupt

        except KeyboardInterrupt:
            print("\n" * 2)
            sys.exit("👋 Script terminated.")

        except NoAnimeEntriesFound as e:
            tqdm.write(f"{e}")
            SEASON_BAR.update(1)
            COOLDOWN_BAR = tqdm(
                range(0, COOLDOWN), position=2, leave=False, desc="Cooldown"
            )
            for i in range(0, COOLDOWN):
                COOLDOWN_BAR.set_description(f"⏱ Cooldown: {COOLDOWN-i} sec(s)")
                time.sleep(1)
                COOLDOWN_BAR.update(1)

    YEAR_BAR.update(1)
