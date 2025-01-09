"""
This module contains utility functions for fetching data from a specified URL
based on provided query parameters, including year and season. It handles rate
limiting and retries if necessary.

Functions:
    fetch_from(url: str, query: str, year: int, season: str) -> None:
        Fetches data from a given URL based on the provided query, year, and season.
"""

import time

import polars as pl
import requests
from tqdm import tqdm


def api_call(
    url: str,
    query: str,
    year: int,
    season: str,
    page: int,
):
    """Fetch data from a given URL with specified query parameters.

    Args:
        url (str): The URL to fetch data from.
        query (str): The query string to be included in the request.
        year (int): The year parameter for the query.
        season (str): The season parameter for the query (e.g., 'spring', 'summer', 'fall', 'winter').
        page (int): The page number for paginated results.

    Returns:
        dict: The JSON response from the server as a dictionary.
    """

    variables = {
        "page": page,
        "perPage": 50,  # hard limit of 50 anime entries per page
        "seasonYear": year,
        "season": season,
        "sort": "ID",
        "type": "ANIME",
    }
    try:
        response = requests.post(
            url, json={"query": query, "variables": variables}, timeout=10
        )
        return response

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

    except Exception as e:
        print(
            (f"Status Code: {response}. " f"{type(e).__name__}: {e}"),
            response.json(),
        )
        return None


def fetch_from(
    url: str,
    query: str,
    year: int,
    season: str,
) -> pl.DataFrame:
    """Fetches data from a given URL based on the provided query, year, and season.

    Args:
        url (str): The URL to send the POST request to.
        query (str): _description_
        year (int): _description_
        season (str): _description_

    Returns:
        pl.DataFrame: the aggregated data from the API response.
    """

    data = []
    current_page = 1
    no_more_pages = False
    while not no_more_pages:
        try:  # Try and retrieve data
            response = api_call(url, query, year, season, current_page)

            headers = dict(response.headers)
            rate_limit_remaining = int(headers["X-RateLimit-Remaining"])
            rate_limit_limit = int(headers["X-RateLimit-Limit"])

            ## Rate limiting and retrying
            if response.status_code == 429 or rate_limit_remaining < 20:
                tqdm.write(
                    (
                        f"Rate limit exceeded ({rate_limit_remaining}/{rate_limit_remaining}). "
                        f"Stopping at page {current_page}."
                        "\nTrying again in 300 seconds."
                    )
                )

                time.sleep(1)
                break

        except Exception as e:
            print(f"Failed to retrieve data: {e}")
            break
        else:
            response_data = response.json()

        media = response_data["data"]["Page"]["media"]

        if len(media) == 0:
            return (rate_limit_remaining, rate_limit_limit)

        data.append(pl.DataFrame(media))

        # Stop if there are no more pages
        if not response_data["data"]["Page"]["pageInfo"]["hasNextPage"]:
            no_more_pages = True
            break

        # Continue looping for pages
        current_page += 1

    try:
        aggregated_data = pl.concat(data)
    except Exception as e:
        print(f"Failed to aggregate data: {type(e).__name__}: {e}")
    else:
        # Write a summary of the data retrieval
        tqdm.write(
            f"🟩 Maximum pages retrieved ({current_page}). "
            f"Retrieved {len(aggregated_data)} anime entries. "
            f"Requests remaining: {rate_limit_remaining}/{rate_limit_limit}"
        )

        return aggregated_data
