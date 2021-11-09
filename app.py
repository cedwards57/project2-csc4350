import flask
from flask_login.utils import login_required
from dotenv import find_dotenv, load_dotenv
import os
import json
from db_functions import (
    db_init,
    add_user,
    del_user,
    get_name,
    user_exists,
    add_recipe,
    del_recipe,
    add_ingredient,
    del_ingredient,
    update_ingredient_quantity_and_units,
    get_ingredient_quantity,
    get_ingredient_units,
    get_recipe_ids,
    get_ingredient_ids,
)
from recipeInfo import recipesInfo
from recipeInstructions import instructions
from recipesSearch import recipesSearch
from recipeIngredients import recipeIngredients

load_dotenv(find_dotenv())

app = flask.Flask(__name__, static_folder="./build/static")
bp = flask.Blueprint("bp", __name__, template_folder="./build")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL_QL")

db_init(app)


@bp.route("/index")
@login_required
def index():
    # TODO: insert the data fetched by your app main page here as a JSON
    DATA = {"your": "data here"}
    data = json.dumps(DATA)
    return flask.render_template(
        "index.html",
        data=data,
    )


app.register_blueprint(bp)


@app.route("/signup")
def signup():
    ...


@app.route("/signup", methods=["POST"])
def signup_post():
    ...


@app.route("/login")
def login():
    ...


@app.route("/login", methods=["POST"])
def login_post():
    pass


@app.route("/saverecipes", methods=["POST"])
def saverecipes():
    error_messages = []
    del_recipes = json.loads(flask.request.data)["delRecipes"]
    add_recipes = json.loads(flask.request.data)["addRecipes"]

    for i in del_recipes:
        del_recipe("", i)
    for i in add_recipes:
        add_recipe("", i)

    current_recipes = get_recipe_ids("")  # current user email

    jsonreturn = flask.jsonify(
        {
            "newRecipeList": current_recipes,
            "errorMessages": error_messages,
        }
    )
    return jsonreturn


@app.route("/")
def main():
    return flask.render_template("index.html")


@app.route("/about")
def about():
    return flask.render_template("<h2>HELLO WORLD???</h2>")


app.run(
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", 8081)),
)
