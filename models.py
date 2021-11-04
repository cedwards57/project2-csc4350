from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserLogin(db.Model, UserMixin):
    username = db.Column(db.String(30), primary_key="True")

    def __repr__(self):
        return "<UserLogin %r %r>" % (self.username)

    def get_id(self):
        return self.username


class SavedRecipe(db.Model):
    username = db.Column(db.String(30), primary_key="True")
    recipe_id = db.Column(db.String(80), primary_key="True")

    def __repr__(self):
        return "<SavedRecipe %r %r>" % (self.username, self.recipe_id)

    def get_artist_id(self):
        return self.recipe_id


class SavedIngredient(db.Model):
    username = db.Column(db.String(30), primary_key="True")
    ingredient_id = db.Column(db.String(80), primary_key="True")

    def __repr__(self):
        return "<SavedIngredient %r %r>" % (self.username, self.ingredient_id)

    def get_artist_id(self):
        return self.ingredient_id
