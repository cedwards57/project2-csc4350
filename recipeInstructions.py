# pass in a recipe ID
# returns
import requests
import os
import json
from dotenv import find_dotenv, load_dotenv
from requests.models import Response


def instructions(recipe):
    load_dotenv(find_dotenv())

    BASE_URL = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{recipe}/analyzedInstructions"

    querystring = {"stepBreakdown": "true"}

    headers = {
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("x-rapidapi-key"),
    }

    res = requests.request("GET", url=BASE_URL, headers=headers, params=querystring)
    res_json = res.json()

    ingredients = []

    for ing in res_json["ingredients"]:
        ingredients.append(
            {
                "name": ing["name"],
                "quantity": ing["amount"]["us"]["value"],
                "units": ing["amount"]["us"]["unit"],
            }
        )

    # if you would like to see the output json for the query that is run then uncomment the next line and past the result into testResult, over the existing text.
    # json_formatted_str = json.dumps(res_json, indent=2)
    # print(json_formatted_str)

    return ingredients
