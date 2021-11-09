from models import User, SavedRecipe, SavedIngredient, db


def db_init(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


def add_user(email, name):
    user_exists = User.query.filter_by(email=email) != None
    if not user_exists:
        new_user = User(email=email, name=name)
        db.session.add(new_user)
        db.session.commit()


def del_user(email):
    this_user = User.query.filter_by(email=email).first()
    if this_user is not None:
        db.session.delete(this_user)
        db.session.commit()


def user_exists(email):
    this_user = User.query.filter_by(email=email).first()
    return this_user != None


def add_recipe(email, recipe_id):
    user_has_recipe = (
        SavedRecipe.query.filter_by(email=email, recipe_id=recipe_id).first() != None
    )
    if not user_has_recipe:
        new_recipe = SavedRecipe(email=email, recipe_id=recipe_id)
        db.session.add(new_recipe)
        db.session.commit()


def del_recipe(email, recipe_id):
    this_recipe = SavedRecipe.query.filter_by(email=email, recipe_id=recipe_id).first()
    if this_recipe is not None:
        db.session.delete(this_recipe)
        db.session.commit()


def add_ingredient(email, ingredient_name, quantity, units):
    if type(quantity) is not int:
        quantity = int(quantity)
    this_ingredient = SavedIngredient.query.filter_by(
        email=email, ingredient_name=ingredient_name
    ).first()
    if this_ingredient is None:
        new_ingredient = SavedIngredient(
            email=email,
            ingredient_name=ingredient_name,
            quantity=quantity,
            units=units,
        )
        db.session.add(new_ingredient)
        db.session.commit()


def del_ingredient(email, ingredient_name):
    this_ingredient = SavedIngredient.query.filter_by(
        email=email, ingredient_name=ingredient_name
    ).first()
    if this_ingredient is not None:
        db.session.delete(this_ingredient)
        db.session.commit()


def update_ingredient_quantity_and_units(email, ingredient_name, quantity, units):
    if type(quantity) is not int:
        quantity = int(quantity)
    this_ingredient = SavedIngredient.query.filter_by(
        email=email, ingredient_name=ingredient_name
    ).first()
    if this_ingredient is not None:
        this_ingredient.quantity = quantity
        this_ingredient.units = units


def get_ingredient_quantity(email, ingredient_name):
    this_ingredient = SavedIngredient.query.filter_by(
        email=email, ingredient_name=ingredient_name
    ).first()
    if this_ingredient is None:
        return None
    return this_ingredient.quantity


def get_ingredient_units(email, ingredient_name):
    this_ingredient = SavedIngredient.query.filter_by(
        email=email, ingredient_name=ingredient_name
    ).first()
    if this_ingredient is None:
        return None
    return this_ingredient.units


def get_name(email):
    this_user = User.query.filter_by(email=email).first()
    if this_user is None:
        return None
    return this_user.name


def get_recipe_ids(email):
    recipes = SavedRecipe.query.filter_by(email=email)
    recipe_list = [i.recipe_id for i in recipes]
    return recipe_list


def get_ingredient_names(email):
    ingredients = SavedIngredient.query.filter_by(email=email)
    ingredient_list = [i.ingredient_name for i in ingredients]
    return ingredient_list
