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
    is_disliked,
    user_exists,
    get_user,
    set_user,
    get_ingredient,
    get_recipes,
    get_recipe_ids,
    user_info_correct,
    find_load_user,
    get_ingredients,
    set_ingredient,
    set_recipe,
    user_has_ingredients,
    user_has_recipe,
    set_like,
    get_like,
    set_dislike,
    get_likes_list,
    get_dislikes_list,
    is_liked,
    is_disliked,
)
from recipeInfo import recipesInfo
from recipeInstructions import instructions
from recipesSearch import recipesSearch
from recipeIngredients import recipeIngredients
from combineQuantities import add_quantities

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
        "name": current_user.email,
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
    flask.session.pop("_flashes", None)
    return flask.render_template("landingPage.html")


@app.route("/redirect")
def redirect():
    flask.session.pop("_flashes", None)
    if current_user.is_authenticated:
        return flask.redirect("/grocerylist")
    else:
        return flask.redirect("/login")


@app.route("/login")
def login():
    if current_user.is_authenticated:
        return flask.redirect("/grocerylist")
    return flask.render_template("login.html")


@app.route("/loginpost", methods=["POST"])  # login POST
def loginpost():
    flask.session.pop("_flashes", None)
    entered_email = flask.request.form["email"]
    entered_password = flask.request.form["password"]
    if not user_info_correct(entered_email, entered_password):
        flask.flash("Incorrect email or password.")
        return flask.redirect("/login")
    login_user(get_user(entered_email))
    return flask.redirect("/redirect")


@app.route("/signup")
def signup():
    if current_user.is_authenticated:
        return flask.redirect("/grocerylist")
    return flask.render_template("signup.html")


@app.route("/signuppost", methods=["POST"])
def signuppost():
    flask.session.pop("_flashes", None)
    entered_email = flask.request.form["email"]
    entered_password = flask.request.form["password"]
    if user_exists(entered_email):
        flask.flash("That email already has an account! Did you mean to log in?")
        return flask.redirect("/signup")
    db.session.add(set_user(entered_email, entered_password))
    db.session.commit()
    login_user(get_user(entered_email))
    return flask.redirect("/")


@app.route("/logout")
@login_required
def logout():
    flask.session.pop("_flashes", None)
    logout_user()
    flask.flash("Logged out successfully.")
    return flask.redirect("/")


@app.route("/saverecipes", methods=["POST"])
@login_required
def saverecipes():
    flask.session.pop("_flashes", None)
    recipe_list = set(
        [str(i["id"]) for i in json.loads(flask.request.data)["recipeList"]]
    )
    user_recipes = get_recipes(current_user.email)

    for recipe in recipe_list:
        if not user_has_recipe(current_user.email, recipe):
            db.session.add(set_recipe(current_user.email, recipe))
            db.session.commit()
    for recipe in user_recipes:
        if recipe.recipe_id not in recipe_list:
            db.session.delete(recipe)
            db.session.commit()
    current_ids = get_recipe_ids(current_user.email)
    current_recipes = []
    for id in current_ids:
        this_recipe_info = recipesInfo(id)
        append_recipe = {
            "title": this_recipe_info["title"],
            "id": this_recipe_info["id"],
        }
        current_recipes.append(append_recipe)

    jsonreturn = flask.jsonify({"newRecipeList": current_recipes})
    return jsonreturn


@app.route("/delingredient", methods=["POST"])
@login_required
def delingredient():
    flask.session.pop("_flashes", None)
    ingredient_name = flask.request.form["ingredient_name"]
    this_ingredient = get_ingredient(current_user.email, ingredient_name)

    if this_ingredient is not None:
        db.session.delete(this_ingredient)
        db.session.commit()
        flask.flash("Ingredient removed.")
    else:
        flask.flash("Failed to delete ingredient.")
    return flask.redirect("/grocerylist")


@app.route("/addingredients", methods=["POST"])
@login_required
def addingredient():
    flask.session.pop("_flashes", None)
    add_indexes = [int(i) for i in flask.request.form.getlist("checks")]
    ingredients = flask.request.form.getlist("ingredient")
    quantities = flask.request.form.getlist("quantity")
    units = flask.request.form.getlist("units")
    recipe_id = flask.request.form["recipe_id"]

    for i in add_indexes:
        ingredient_in_db = get_ingredient(current_user.email, ingredients[i])

        if ingredient_in_db is not None:
            new_quantity = add_quantities(
                ingredient_in_db.quantity,
                ingredient_in_db.units,
                float(quantities[i]),
                units[i],
            )
            ingredient_in_db.quantity = new_quantity["amount"]
            ingredient_in_db.units = new_quantity["units"]
            db.session.commit()

        if ingredient_in_db is None:
            new_ingredient = set_ingredient(
                current_user.email, ingredients[i], quantities[i], units[i]
            )
            db.session.add(new_ingredient)
            db.session.commit()

    return flask.redirect(f"/recipe?recipeid={recipe_id}")


@app.route("/searchrecipes", methods=["POST"])
@login_required
def searchrecipes():
    flask.session.pop("_flashes", None)
    query = json.loads(flask.request.data)["query"]
    result_ids = recipesSearch(query)
    recipes_info = []
    for id in result_ids:
        recipe_info = recipesInfo(id)
        this_recipe = {"title": recipe_info["title"], "id": recipe_info["id"]}
        recipes_info.append(this_recipe)

    jsonreturn = flask.jsonify(
        {"results": recipes_info}
    )  # data.results gives a list of info dicts
    return jsonreturn


@app.route("/recipe")
@login_required
def recipe():
    recipe_id = flask.request.args["recipeid"]

    recipy_info = recipesInfo(recipe_id)
    recipe_ing = recipeIngredients(recipe_id)

    data = {
        "title": recipy_info["title"],
        "summary": recipy_info["summary"],
        "imageURL": recipy_info["imageURL"],
        "ingredients": recipe_ing,
        "len": len(recipe_ing),
        "recipe_id": recipe_id,
        "is_liked": is_liked(current_user.email, recipe_id),
        "is_disliked": is_disliked(current_user.email, recipe_id),
    }

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


@app.route("/savelikes", methods=["POST"])
@login_required
def savelikes():
    flask.session.pop("_flashes", None)
    likes_list = json.loads(flask.request.data)["likes"]  # expects a list of recipe IDs
    dislikes_list = json.loads(flask.request.data)[
        "dislikes"
    ]  # likes & UNlikes go in same list. dislikes go with un-dislikes.
    for i in dislikes_list:
        if is_disliked(current_user.email, i):
            like_entry = get_like(current_user.email, i)
            db.session.delete(like_entry)
            db.session.commit()
        elif is_liked(current_user.email, i):
            like_entry = get_like(current_user.email, i)
            like_entry.like_value = -1
            db.session.commit()
        else:
            like_entry = set_dislike(current_user.email, i)
            db.session.add(like_entry)
            db.session.commit()

    for i in likes_list:
        if is_liked(current_user.email, i):
            like_entry = get_like(current_user.email, i)
            db.session.delete(like_entry)
            db.session.commit()
        elif is_disliked(current_user.email, i):
            like_entry = get_like(current_user.email, i)
            like_entry.like_value = 1
            db.session.commit()
        else:
            like_entry = set_like(current_user.email, i)
            db.session.add(like_entry)
            db.session.commit()

    new_likes = get_likes_list(current_user.email)
    new_dislikes = get_dislikes_list(current_user.email)

    jsonreturn = flask.jsonify(
        {
            "likes": new_likes,
            "dislikes": new_dislikes,
        }
    )
    return jsonreturn


@app.route("/likerecipe", methods=["POST"])
@login_required
def likerecipe():
    flask.session.pop("_flashes", None)
    recipe_id = flask.request.form["recipe_id"]
    if is_liked(current_user.email, recipe_id):
        like_entry = get_like(current_user.email, recipe_id)
        db.session.delete(like_entry)
        db.session.commit()
    elif is_disliked(current_user.email, recipe_id):
        like_entry = get_like(current_user.email, recipe_id)
        like_entry.like_value = 1
        db.session.commit()
    else:
        like_entry = set_like(current_user.email, recipe_id)
        db.session.add(like_entry)
        db.session.commit()

    return flask.redirect(f"/recipe?recipeid={recipe_id}")


@app.route("/dislikerecipe", methods=["POST"])
@login_required
def dislikerecipe():
    flask.session.pop("_flashes", None)
    recipe_id = flask.request.form["recipe_id"]
    if is_disliked(current_user.email, recipe_id):
        like_entry = get_like(current_user.email, recipe_id)
        db.session.delete(like_entry)
        db.session.commit()
    elif is_liked(current_user.email, recipe_id):
        like_entry = get_like(current_user.email, recipe_id)
        like_entry.like_value = -1
        db.session.commit()
    else:
        like_entry = set_dislike(current_user.email, recipe_id)
        db.session.add(like_entry)
        db.session.commit()

    return flask.redirect(f"/recipe?recipeid={recipe_id}")


app.run(
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", 8081)),
)
