import flask
from flask_login import (
    LoginManager,
    login_required,
    current_user,
    login_user,
    logout_user,
)
from dotenv import find_dotenv, load_dotenv
import os
from models import db
import json
from db_functions import (
    get_name,
    user_exists,
    get_user,
    set_user,
    get_ingredient,
    get_ingredient_quantity,
    get_ingredient_units,
    get_recipe,
    get_recipe_ids,
    get_ingredient_names,
    user_info_correct,
    find_load_user,
    get_ingredients,
    set_ingredient,
    set_recipe,
    user_has_ingredients,
    user_has_recipes,
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
app.secret_key = os.getenv("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
with app.app_context():
    db.create_all()


@bp.route("/recipelist")
@login_required
def recipelist():
    user_recipes = get_recipe_ids(current_user.email)
    DATA = {
        "name": current_user.name,
        "recipes": [
            {"title": recipesInfo(i)["title"], "id": recipesInfo(i)["id"]}
            for i in user_recipes
        ],
    }
    data = json.dumps(DATA)
    return flask.render_template("index.html", data=data)


app.register_blueprint(bp)


@login_manager.user_loader
def load_user(user_id):
    return find_load_user(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    flask.flash("You must be logged in to view that page.")
    return flask.redirect("/login")


@app.route("/")
def main():
    if current_user.is_authenticated:
        return flask.redirect("/grocerylist")
    else:
        return flask.redirect("/login")


@app.route("/login")
def login():
    return flask.render_template("login.html")


@app.route("/loginpost", methods=["POST"])  # login POST
def loginpost():
    entered_email = flask.request.form["email"]
    entered_name = flask.request.form["name"]
    if not user_info_correct(entered_email, entered_name):
        flask.flash("Incorrect username or password.")
        return flask.redirect("/login")
    login_user(get_user(entered_email))
    return flask.redirect("/")


@app.route("/signup")
def signup():
    return flask.render_template("signup.html")


@app.route("/signuppost", methods=["POST"])
def signuppost():
    entered_email = flask.request.form["email"]
    entered_name = flask.request.form["name"]
    if user_exists(entered_email):
        flask.flash("That username is taken. Sorry!")
        return flask.redirect("/signup")
    db.session.add(set_user(entered_email, entered_name))
    db.session.commit()
    login_user(get_user(entered_email))
    return flask.redirect("/")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return flask.redirect("/")


@app.route("/saverecipes", methods=["POST"])
@login_required
def saverecipes():
    error_messages = []
    del_recipes = json.loads(flask.request.data)["delRecipes"]
    add_recipes = json.loads(flask.request.data)["addRecipes"]

    for recipe in add_recipes:
        db.session.add(set_recipe(current_user.email, recipe))
    for recipe in del_recipes:
        db.session.delete(get_recipe(current_user.email, recipe))
    db.session.commit()

    current_recipes = [
        {"title": recipesInfo(i)["title"], "id": recipesInfo(i)["id"]}
        for i in get_recipe_ids(current_user.email)
    ]

    jsonreturn = flask.jsonify(
        {
            "newRecipeList": current_recipes,
            "errorMessages": error_messages,
        }
    )
    return jsonreturn


@app.route("/delingredient", methods=["POST"])
@login_required
def delingredient():
    ingredient_name = flask.request.form["ingredient_name"]
    if get_ingredient(current_user.email, ingredient_name) is not None:
        db.session.delete(get_ingredient(current_user.email, ingredient_name))
        db.session.commit()
        flask.flash("Ingredient removed.")
    else:
        flask.flash("Failed to delete ingredient.")
    return flask.redirect("/grocerylist")


@app.route("/addingredient", methods=["POST"])
@login_required
def addingredient():
    ingredient_name = flask.request.form["ingredient_name"]
    if get_ingredient(current_user.email, ingredient_name) is None:
        db.session.add(set_ingredient(current_user.email, ingredient_name))
        db.session.commit()


@app.route("/searchrecipes", methods=["POST"])
@login_required
def searchrecipes():
    query = json.loads(flask.request.data)["query"]
    result_ids = recipesSearch(query)
    recipes_info = [
        {"title": recipesInfo(i)["title"], "id": recipesInfo(i)["id"]}
        for i in result_ids
    ]
    jsonreturn = flask.jsonify(
        {"results": recipes_info}
    )  # data.results gives a list of info dicts
    return jsonreturn


@app.route("/recipe")
@login_required
def recipe():
    recipe_id = flask.request.args["recipeid"]
    data = recipesInfo(recipe_id)
    return flask.render_template("recipe.html", data=data)


@app.route("/grocerylist")
@login_required
def grocerylist():
    if user_has_ingredients(current_user.email):
        ingredients_info = get_ingredients(current_user.email)
        ingredients = {
            "names": [i["name"] for i in ingredients_info],
            "quantities": [i["quantity"] for i in ingredients_info],
            "units": [i["units"] for i in ingredients_info],
        }
    else:
        ingredients = {
            "names": ["Add ingredients from the recipe page!"],
            "quantities": ["--"],
            "units": ["--"],
        }
    return flask.render_template(
        "groceryList.html",
        ingredients=ingredients,
        len=len(ingredients["names"]),
    )


app.run(
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", 8081)),
)
