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


@app.route("/")
def index():
    if True:  # if user is logged in:
        return flask.redirect("/recipelist")
    else:
        return flask.redirect("/login")


@app.route("/login")
def login():
    return flask.render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    if not user_exists(""):  # email
        add_user("", "")  # email, name
    # login user
    flask.redirect("/recipe")


@app.route("/saverecipes", methods=["POST"])
# login required
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


@app.route("/saveingredients", methods=["POST"])
# login required
def saverecipes():
    error_messages = []
    del_ingredients = json.loads(flask.request.data)["delIngredients"]
    add_ingredients = json.loads(flask.request.data)["addIngredients"]

    for i in del_ingredients:
        del_ingredient("", i)
    for i in add_ingredients:
        add_ingredient(
            "",
            i,
        )

    current_ingredients = get_ingredient_ids("")  # current user email
    jsonreturn = flask.jsonify(
        {
            "newRecipeList": current_ingredients,
            "errorMessages": error_messages,
        }
    )
    return jsonreturn


@app.route("/searchrecipes", methods=["POST"])
def searchrecipes():
    query = json.loads(flask.request.data)["query"]
    result_ids = recipesSearch(query)
    recipes_info = [recipesInfo(i) for i in result_ids]
    jsonreturn = flask.jsonify({"results": recipes_info})  # data.results gives a list
    return jsonreturn


@app.route("/recipe")
# login required
def recipe():
    return flask.render_template("recipe.html")


@app.route("/recipelist")
# login required
def recipelist():
    recipe_ids = get_recipe_ids("")  # email
    ingredient_ids = get_ingredient_ids("")
    return flask.render_template("index.html", data=data)


@app.route("/grocerylist")
# login required
def recipelist():
    recipe_ids = get_recipe_ids("")  # email

    return flask.render_template("index.html", data=data)


app.run(
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", 8081)),
)
