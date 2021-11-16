from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model, UserMixin):
    email = db.Column(db.String(50), primary_key="True")
    name = db.Column(db.String(50))

    def __repr__(self):
        return "<User %r %r>" % (self.email)

    def get_id(self):
        return self.email


class SavedRecipe(db.Model):
    email = db.Column(db.String(50), primary_key="True")
    recipe_id = db.Column(db.String(80), primary_key="True")

    def __repr__(self):
        return "<SavedRecipe %r %r>" % (self.email, self.recipe_id)

    def get_recipe_id(self):
        return self.recipe_id


class SavedIngredients(db.Model):
    email = db.Column(db.String(50), primary_key="True")
    ingredient_name = db.Column(db.String(80), primary_key="True")
    quantity = db.Column(db.Integer)
    units = db.Column(db.String(16))

    def __repr__(self):
        return "<SavedIngredients %r %r>" % (self.email, self.ingredient_name)

    def get_ingredient_name(self):
        return self.ingredient_name
