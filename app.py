import flask
from flask_login import (
    LoginManager,
    login_required,
    current_user,
    login_user,
    logout_user,
)
from flask import Flask, redirect, request, url_for
from oauthlib.oauth2 import WebApplicationClient
import requests
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

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

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

client = WebApplicationClient(GOOGLE_CLIENT_ID)


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


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@login_manager.unauthorized_handler
def unauthorized_callback():
    flask.flash("You must be logged in to view that page.")
    return flask.redirect("/login")


@app.route("/")
def main():
    if current_user.is_authenticated:
        return flask.redirect("/grocerylist")
    return flask.render_template("login.html")


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

    # @app.route("/loginpost", methods=["POST"])  # login POST
    # def loginpost():
    entered_email = flask.request.form["email"]
    entered_name = flask.request.form["name"]
    if not user_info_correct(entered_email, entered_name):
        flask.flash("Incorrect username or password.")
        return flask.redirect("/login")
    login_user(get_user(entered_email))
    return flask.redirect("/")


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
        if not user_exists(users_email):
            db.session.add(set_user(users_email, users_name))
            db.session.commit()
        login_user(get_user(users_email))
    return flask.redirect("/")

    # @app.route("/signup")
    # def signup():
    return flask.render_template("signup.html")

    # @app.route("/signuppost", methods=["POST"])
    # def signuppost():
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


@app.route("/addingredients", methods=["POST"])
@login_required
def addingredient():
    ingredient_names = flask.request.form["ingredients"]
    for ingredient in ingredient_names:
        if get_ingredient(current_user.email, ingredient) is None:
            db.session.add(set_ingredient(current_user.email, ingredient))
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
    ssl_context="adhoc",
)
