# pass in a recipe ID
# returns a list of the recipy name and summary(with html)

import requests
import os
import json
from dotenv import find_dotenv, load_dotenv
from requests.models import Response

def recipesInfo(recipe):
    load_dotenv(find_dotenv())

    BASE_URL = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{recipe}/information"
    
    headers = {
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': os.getenv("x-rapidapi-key")
    }

    res2 = requests.request("GET", url=BASE_URL, headers=headers)
    res2_json = res2.json()

    recipe_info_list = []

    recipe_info_list.append(res2_json["title"])
    recipe_info_list.append(res2_json["summary"])

    # res_json_fmtd = json.dumps(res2_json, indent=2)

    # print(res_json_fmtd)
    return recipe_info_list

recipesInfo(104446)