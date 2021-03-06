import requests
import os
import json
from dotenv import find_dotenv, load_dotenv
from requests.models import Response


def add_quantities(amnt1, unt1, amnt2, unt2):

    amnt1 = float(amnt1)
    amnt2 = float(amnt2)

    if len(unt1) > len(unt2):
        if (unt1[-1:] == "s" or unt1[-2:] == "es") and (
            unt1[:-1] == unt2 or unt1[:-2] == unt2
        ):
            unt2 = unt1

    elif len(unt1) < len(unt2):
        if (unt2[-1:] == "s" or unt2[-2:] == "es") and (
            unt2[:-1] == unt1 or unt2[:-2] == unt1
        ):
            unt1 = unt2

    famnt = amnt1
    funit = unt1

    mtrc_unt = ["cups", "cup", "tbsps", "tbsp", "tsps", "tsp", "fl oz", "ml", "g"]
    mtrc_cnvrt = [1, 1, 1 / 16, 1 / 16, 1 / 48, 1 / 48, 1 / 8, 1 / 237, 1 / 227]

    if unt1 == unt2:
        famnt = amnt1 + amnt2

    elif mtrc_unt.index(unt1) < mtrc_unt.index(unt2):
        funit = unt1
        famnt = amnt1 + (amnt2 * mtrc_cnvrt[mtrc_unt.index(unt2)])

    elif mtrc_unt.index(unt1) > mtrc_unt.index(unt2):
        funit = unt2
        famnt = amnt2 + (amnt1 * mtrc_cnvrt[mtrc_unt.index(unt1)])

    return {"amount": str(famnt), "units": funit}
