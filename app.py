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
    get_ingredient_names,
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


@bp.route("/recipelist")
def recipelist():
    DATA = {"name": "", "recipes": get_recipe_ids("")}  # name, email
    data = json.dumps(DATA)
    return flask.render_template("index.html", data=data)


app.register_blueprint(bp)


@app.route("/")
def index():
    if True:  # if user is logged in:
        return flask.redirect("/grocerylist")
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
def saveingredients():
    error_messages = []
    del_ingredients = json.loads(flask.request.data)["delIngredients"]
    add_ingredients = json.loads(flask.request.data)["addIngredients"]

    for i in del_ingredients:
        del_ingredient("", i["name"])
    for i in add_ingredients:
        add_ingredient("", i["name"], i["quantity"], i["units"])

    current_ingredients = get_ingredient_names("")  # current user email
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
    jsonreturn = flask.jsonify(
        {"results": recipes_info}
    )  # data.results gives a list of info dicts
    return jsonreturn


@app.route("/recipe")
def recipe():
    recipe_id = flask.request.form["recipeid"]  # whatever the field name is
    data = recipesInfo(recipe_id)
    return flask.render_template("recipe.html")


@app.route("/grocerylist")
# login required
def grocerylist():
    recipe_ids = get_recipe_ids("")  # email
    DATA = {"": ""}
    data = json.dumps(DATA)
    return flask.render_template("index.html", data=data)


app.run(
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", 8081)),
)
