from models import UserInfos, SavedRecipe, SaveIngredient, Likes
from encryption import encrypt_password, decrypt_password


def find_load_user(user_id):
    return UserInfos.query.get(user_id)


def user_exists(email):
    this_user = UserInfos.query.filter_by(email=email).first()
    return this_user != None


def user_info_correct(email, password):
    this_user = UserInfos.query.filter_by(email=email).first()
    if this_user != None:
        decrypted_pw = decrypt_password(this_user.password)
        return password == decrypted_pw
    return False


def get_user(email):
    return UserInfos.query.filter_by(email=email).first()


def set_user(email, password):
    encrypted_pw = encrypt_password(password)
    return UserInfos(email=email, password=encrypted_pw)


def get_ingredient_quantity(email, ingredient_name):
    this_ingredient = SaveIngredient.query.filter_by(
        email=email, ingredient_name=ingredient_name
    ).first()
    if this_ingredient is None:
        return None
    return this_ingredient.quantity


def get_ingredient_units(email, ingredient_name):
    this_ingredient = SaveIngredient.query.filter_by(
        email=email, ingredient_name=ingredient_name
    ).first()
    if this_ingredient is None:
        return None
    return this_ingredient.units


def get_ingredient(email, ingredient_name):
    return SaveIngredient.query.filter_by(
        email=email, ingredient_name=ingredient_name
    ).first()


def set_ingredient(email, ingredient_name, quantity, units):
    return SaveIngredient(
        email=email, ingredient_name=ingredient_name, quantity=quantity, units=units
    )


def set_recipe(email, recipe_id):
    return SavedRecipe(email=email, recipe_id=recipe_id)


def get_recipe_ids(email):
    recipes = SavedRecipe.query.filter_by(email=email)
    recipe_list = [i.recipe_id for i in recipes]
    return recipe_list


def get_recipe(email, recipe_id):
    return SavedRecipe.query.filter_by(email=email, recipe_id=recipe_id).first()


def get_ingredient_names(email):
    ingredients = SaveIngredient.query.filter_by(email=email)
    ingredient_list = [i.ingredient_name for i in ingredients]
    return ingredient_list


def user_has_ingredients(email):
    ingredients = SaveIngredient.query.filter_by(email=email).first()
    return ingredients is not None


def user_has_recipes(email):
    recipes = SavedRecipe.query.filter_by(email=email).first()
    return recipes is not None


def get_ingredients(email):
    ingredients = SaveIngredient.query.filter_by(email=email)
    ingredient_list = [
        {"name": i.ingredient_name, "quantity": i.quantity, "units": i.units}
        for i in ingredients
    ]
    return ingredient_list


def get_likes_list(email):
    likes = Likes.query.filter_by(email=email, like_value=1)
    likes_list = [i.recipe_id for i in likes]
    return likes_list


def get_dislikes_list(email):
    dislikes = Likes.query.filter_by(email=email, like_value=-1)
    dislikes_list = [i.recipe_id for i in dislikes]
    return dislikes_list


def get_like(email, recipe_id):
    Likes.query.filter_by(email=email, recipe_id=recipe_id).first()


def set_like(email, recipe_id):
    return Likes(email=email, recipe_id=recipe_id, like_value=1)


def set_dislike(email, recipe_id):
    return Likes(email=email, recipe_id=recipe_id, like_value=-1)


def get_like_value(email, recipe_id):
    like_entry = Likes.query.filter_by(email=email, recipe_id=recipe_id).first()
    if like_entry == None:
        return 0
    return like_entry.like_value


def is_liked(email, recipe_id):
    like_entry = Likes.query.filter_by(email=email, recipe_id=recipe_id).first()
    if like_entry == None:
        return False
    return like_entry.like_value == 1


def is_disliked(email, recipe_id):
    like_entry = Likes.query.filter_by(email=email, recipe_id=recipe_id).first()
    if like_entry == None:
        return False
    return like_entry.like_value == -1
