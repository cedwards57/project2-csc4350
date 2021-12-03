import unittest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from recipeInfo import recipesInfo
from recipeIngredients import recipeIngredients

INPUT = "INPUT"
EXPECTED_OUTPUT = "EXPECTED_OUTPUT"

class GetRecipeDataTest(unittest.TestCase):
    def setUp(self):

        self.success_test_params = [
            {
                INPUT: '',
                EXPECTED_OUTPUT: {'title':'','id':'', 'imageURL':'', 'summary':''}
            },
            {
                INPUT: '104446',
                EXPECTED_OUTPUT: {'title': 'Moroccan Chicken', 'id': 104446, 'imageURL': 'https://spoonacular.com/recipeImages/104446-556x370.jpg', 'summary': 'Need a <b>gluten free main course</b>? Moroccan Chicken could be an awesome recipe to try. This recipe serves 4 and costs $2.16 per serving. One serving contains <b>747 calories</b>, <b>47g of protein</b>, and <b>42g of fat</b>. Not a lot of people made this recipe, and 1 would say it hit the spot. Head to the store and pick up saffron thread, chicken pieces, juice of lemon, and a few other things to make it today. To use up the saffron you could follow this main course with the <a href="https://spoonacular.com/recipes/creamy-saffron-yogurt-213954">Creamy saffron yogurt</a> as a dessert. From preparation to the plate, this recipe takes around <b>1 hour and 15 minutes</b>. All things considered, we decided this recipe <b>deserves a spoonacular score of 74%</b>. This score is solid. Try <a href="https://spoonacular.com/recipes/moroccan-chicken-100422">Moroccan Chicken</a>, <a href="https://spoonacular.com/recipes/moroccan-chicken-543637">Moroccan Chicken</a>, and <a href="https://spoonacular.com/recipes/moroccan-chicken-74397">Moroccan Chicken</a> for similar recipes.'}
            },
            {
                INPUT:'11111',
                EXPECTED_OUTPUT: {'title': '', 'id': '', 'imageURL': '', 'summary': ''}
            },
        ]
        self.success_test_params_ing = [
            {
                INPUT: '',
                EXPECTED_OUTPUT: []
            },
            {
                INPUT: '104446',
                EXPECTED_OUTPUT: [{'name': 'canned tomatoes', 'recipe_id': 104446, 'quantity': 14.109, 'units': 'oz'}, {'name': 'chicken pieces', 'recipe_id': 104446, 'quantity': 1.874, 'units': 'lb'}, {'name': 'chicken stock', 'recipe_id': 104446, 'quantity': 1.0, 'units': 'cup'}, {'name': 'cinnamon stick', 'recipe_id': 104446, 'quantity': 1.0, 'units': ''}, {'name': 'honey', 'recipe_id': 104446, 'quantity': 1.0, 'units': 'Tbsp'}, {'name': 'lemon (juice)', 'recipe_id': 104446, 'quantity': 1.0, 'units': ''}, {'name': 'olive oil', 'recipe_id': 104446, 'quantity': 2.0, 'units': 'Tbsps'}, {'name': 'onions', 'recipe_id': 104446, 'quantity': 2.0, 'units': ''}, {'name': 'prunes', 'recipe_id': 104446, 'quantity': 12.0, 'units': ''}, {'name': 'pumpkin', 'recipe_id': 104446, 'quantity': 1.102, 'units': 'lb'}, {'name': 'ras el hanout spice mix', 'recipe_id': 104446, 'quantity': 1.5, 'units': 'Tbsps'}, {'name': 'saffron', 'recipe_id': 104446, 'quantity': 0.25, 'units': 'tsps'}, {'name': 'salt and pepper', 'recipe_id': 104446, 'quantity': 4.0, 'units': 'servings'}, {'name': 'yoghurt', 'recipe_id': 104446, 'quantity': 4.0, 'units': 'servings'}]
            },
            {
                INPUT:'111111',
                EXPECTED_OUTPUT: [{'name': 'black pepper', 'recipe_id': 111111, 'quantity': 0.25, 'units': 'tsps'}, {'name': 'frozen broccoli', 'recipe_id': 111111, 'quantity': 2.0, 'units': 'cups'}, {'name': 'boneless chicken meat', 'recipe_id': 111111, 'quantity': 1.0, 'units': 'lb'}, {'name': 'canned cream of mushroom soup', 'recipe_id': 111111, 'quantity': 10.0, 'units': 'ounce'}, {'name': 'minute rice', 'recipe_id': 111111, 'quantity': 2.0, 'units': 'cups'}, {'name': 'canned mushroom', 'recipe_id': 111111, 'quantity': 4.0, 'units': 'ounce'}, {'name': 'paprika', 'recipe_id': 111111, 'quantity': 0.25, 'units': 'tsps'}, {'name': 'water', 'recipe_id': 111111, 'quantity': 1.5, 'units': 'cups'}]
            },
            {
                INPUT:'11111',
                EXPECTED_OUTPUT: []
            },
        ]

    def test_recipeInfo(self):
        for test in self.success_test_params:
            self.assertEqual(recipesInfo(test[INPUT]), test[EXPECTED_OUTPUT])

    def test_recipeIngredients(self):
        for test in self.success_test_params_ing:
            self.assertEqual(recipesInfo(test[INPUT]), test[EXPECTED_OUTPUT])

    