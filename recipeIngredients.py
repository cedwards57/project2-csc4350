# pass in a recipes ID to get a 2D list of ingredients

import requests
import os
import json
from dotenv import find_dotenv, load_dotenv
from requests.models import Response


def recipeIngredients(rID):
    load_dotenv(find_dotenv())

    url = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{rID}/ingredientWidget.json"

    headers = {
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("x-rapidapi-key"),
    }

    response = requests.get(url, headers=headers)
    res_json = response.json()

    ingredients = []
    
    try:

        for ing in res_json["ingredients"]:
            ingredients.append(
                {
                    "name": ing["name"],
                    "recipe_id": rID,
                    "quantity": ing["amount"]["us"]["value"],
                    "units": ing["amount"]["us"]["unit"],
                }
            )
    except res_json['status'] == 'failure':
        pass
    # # if you would like to see what the entier json returns uncomment the next two lines.
    # res_json_fmtd = json.dumps(res_json, indent=2)
    # print(ingredients)

    return ingredients


# uncomment next two lines to test the function
recipeIngredients(1003464)
