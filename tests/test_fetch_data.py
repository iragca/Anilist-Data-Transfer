from utils.fetch_data import fetch_from, api_call

#TODO: Add more and finish tests
def test_api_call():

    with open(r"src/utils/api_query.graphql", "r") as file:
        graphql_query = file.read()

    result = api_call(
        url="https://graphql.anilist.co",
        query=graphql_query,
        year=2014,
        season="FALL",
        page=1,
    )
    
    assert result.status_code == 200