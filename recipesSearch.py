# pass the search query as a string
# return a list of 10 result meal IDs

import requests
import os
import json
from dotenv import find_dotenv, load_dotenv
from requests.models import Response


def recipesSearch(items):
    load_dotenv(find_dotenv())

    BASE_URL = (
        "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search"
    )

    headers = {
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("x-rapidapi-key"),
    }

    queryString = {"query": items, "number": "10", "type": "main course"}

    res1 = requests.request("GET", url=BASE_URL, headers=headers, params=queryString)
    res1_json = res1.json()

    searchResultIDs = []

    for meals in res1_json["results"]:
        searchResultIDs.append(meals["id"])

    # # if you would like to see the output json for the query that is run then uncomment the next line and past the result into testResult, over the existing text.
    # json_formatted_str = json.dumps(res1_json, indent=2)
    # print(searchResultID)

    return searchResultIDs
    
# uncomment next two lines to test the function
# things = "chicken"
# recipesSearch(things)
