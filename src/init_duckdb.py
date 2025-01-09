"""
This module initializes a DuckDB database with tables for storing anime-related data.

Process:
- Connects to a DuckDB database file located at 'src/anilist.duckdb'.
- Executes SQL statements to create or replace the tables.
- Commits the changes and closes the connection to the database.

Tables created:
- Status: Stores statistics about anime user statuses.
- User: Stores user information.
- WebAsset: Stores web assets related to anime.
- Studio: Stores information about studios associated with anime.
- Tag: Stores tags associated with anime.
- Genre: Stores genres associated with anime.
- Anime: Stores detailed information about anime.
- Review: Stores reviews of anime.

Usage:
    # From the project root directory
    $ python src/init_duckdb.py

Notes:
    - To if you want to customize the data retrieved,
      do so by editing the src/utils/api_query.graphql and the duckdb schema in this script.

    - If you must change the schema, I recommend exploring the documentation
      and GraphQL API to understand the data structure.
        - https://docs.anilist.co/
        - https://studio.apollographql.com/sandbox/explorer?endpoint=https://graphql.anilist.co

    - Run experiments using a Jupyter Notebook to test your changes;

    - When you do, the data will be heavily nested, so you will need
      functions like Polar's df.explode([<column names>]) or df.unnest([<column names>]).

    - Foreign keys are not recommended as the GraphQL API is inherently node based
      and not relational. The primary keys are to enforce uniqueness.
"""

import duckdb

# Connect to the DuckDB database; if it doesn't exist, it will be created
conn = duckdb.connect(r"src/anilist.duckdb")

STATS_TABLE = """
CREATE OR REPLACE TABLE Status (
    AnimeID INTEGER,
    Season VARCHAR(6),
    SeasonYear INTEGER,
    AmountOfUsers INTEGER,
    UserStatus TEXT,

    PRIMARY KEY (AnimeID, Season, SeasonYear, UserStatus)
);
"""

USERS_TABLE = """
CREATE OR REPLACE TABLE User (
    UserID INTEGER,
    Username TEXT,
    DonatorTier TEXT,
    DonatorBadge TEXT,
    UserCreatedAt DATE,
    LargeAvatar TEXT,
    MediumAvatar TEXT,

    PRIMARY KEY (UserID)
);
"""

WEB_ASSETS_TABLE = """
CREATE OR REPLACE TABLE WebAsset (
    AnimeID INTEGER,
    Season VARCHAR(6),
    SeasonYear INTEGER,
    Banner TEXT,
    MediumCover TEXT,
    LargeCover TEXT,
    ExtraLargeCover TEXT,
    Color TEXT,
    SiteURL TEXT,
    Trailer TEXT,

    PRIMARY KEY (AnimeID, Season, SeasonYear)
);
"""

STUDIOS_TABLE = """
CREATE OR REPLACE TABLE Studio (
    AnimeID INTEGER,
    Season VARCHAR(6),
    SeasonYear INTEGER,
    StudioID INTEGER,
    StudioName TEXT,

    PRIMARY KEY (StudioID, AnimeID, Season, SeasonYear)
);
"""

TAGS_TABLE = """
CREATE OR REPLACE TABLE Tag (
    TagID INTEGER,
    IsAdult BOOLEAN,
    Category TEXT,
    Description TEXT,
    AnimeID INTEGER,
    Season VARCHAR(6),
    SeasonYear INTEGER,

    PRIMARY KEY (TagID)
);
"""
GENRES_TABLE = """
CREATE OR REPLACE TABLE Genre (
    Genre TEXT,
    AnimeID INTEGER,
    Season VARCHAR(6),
    SeasonYear INTEGER,

    PRIMARY KEY (Genre, AnimeID, Season, SeasonYear)
);
"""

ANIME_TABLE = """
CREATE OR REPLACE TABLE Anime (
    AnimeID INTEGER,
    Season VARCHAR(6),
    SeasonYear INTEGER,
    EnglishTitle TEXT,
    NativeTitle TEXT,
    RomajiTitle TEXT,
    Format TEXT,
    MeanScore INTEGER,
    Popularity INTEGER,
    Episodes INTEGER,
    Favourites INTEGER,
    Duration INTEGER,
    StartDate DATE,
    EndDate DATE,

    PRIMARY KEY (AnimeID, Season, SeasonYear),
    CHECK (season IN ('FALL', 'WINTER', 'SPRING', 'SUMMER'))
);
"""

REVIEW_TABLE = """
CREATE OR REPLACE TABLE Review (
    ReviewID INTEGER,
    Rating INTEGER,
    RatingAmount INTEGER,
    Body TEXT,
    Summary TEXT,
    ReviewCreatedAt DATE,
    ReviewUpdatedAt DATE,
    AnimeID INTEGER,
    Season VARCHAR(6),
    SeasonYear INTEGER,
    UserID INTEGER,

    PRIMARY KEY (ReviewID)
  );
"""

# Execute the SQL statements
conn.execute(STATS_TABLE)
conn.execute(USERS_TABLE)
conn.execute(WEB_ASSETS_TABLE)
conn.execute(STUDIOS_TABLE)
conn.execute(TAGS_TABLE)
conn.execute(GENRES_TABLE)
conn.execute(ANIME_TABLE)
conn.execute(REVIEW_TABLE)

conn.commit()
conn.close()
