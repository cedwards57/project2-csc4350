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
    add_user,
    del_user,
    get_name,
    user_exists,
    get_user,
    set_user,
    add_recipe,
    del_recipe,
    add_ingredient,
    del_ingredient,
    update_ingredient_quantity_and_units,
    get_ingredient_quantity,
    get_ingredient_units,
    get_recipe_ids,
    get_ingredient_names,
    user_info_correct,
    find_load_user,
    get_ingredients,
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


@login_manager.user_loader
def load_user(user_id):
    return find_load_user(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    flask.flash("You must be logged in to view that page.")
    return flask.redirect("/login")


@bp.route("/recipelist")
@login_required
def recipelist():
    DATA = {"name": current_user.name, "recipes": get_recipe_ids(current_user.email)}
    data = json.dumps(DATA)
    return flask.render_template("index.html", data=data)


app.register_blueprint(bp)


@app.route("/")
def index():
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
    if not user_exists(entered_name) or not user_info_correct(
        entered_email, entered_name
    ):
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


@app.route("/logout")  # logout POST
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
@login_required
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
@login_required
def searchrecipes():
    query = json.loads(flask.request.data)["query"]
    result_ids = recipesSearch(query)
    recipes_info = [recipesInfo(i) for i in result_ids]
    jsonreturn = flask.jsonify(
        {"results": recipes_info}
    )  # data.results gives a list of info dicts
    return jsonreturn


@app.route("/recipe")
@login_required
def recipe():
    recipe_id = flask.request.form["recipeid"]  # whatever the field name is
    data = recipesInfo(recipe_id)
    return flask.render_template("recipe.html")


@app.route("/recipelist")
@login_required
def recipelist():
    recipe_ids = get_recipe_ids("")  # email
    ingredient_ids = get_ingredient_names("")
    return flask.render_template("index.html", data=data)


@app.route("/grocerylist")
@login_required
def grocerylist():
    person = current_user.email
    listForTable = []
    # list of ingredients in the database for the email of the user
    recipe_ids = get_ingredient_names(person)  # email

    # the for loop goes throught the list of ingredients that were returned from the db
    # and creates a combines them with their quantity and units
    for item in recipe_ids:
        temp = [item]
        temp.append(get_ingredient_quantity(person, item))
        temp.append(get_ingredient_units(person, item))
        listForTable.append(temp)

    return flask.render_template(
        "groceryList.html",
        length=len(listForTable),
        length2=len(listForTable[0]),
        listForTable=listForTable,
    )


app.run(
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", 8081)),
)
