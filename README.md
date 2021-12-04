## Heroku Link: Sprint 2
[http://hungrylists.herokuapp.com/](http://hungrylists.herokuapp.com/)

## Sprint 1 Link
[http://project2-csc4350.herokuapp.com/](http://project2-csc4350.herokuapp.com/)
<br><br>

# Use This App (Documentation)
Welcome! Hungrylists can be accessed from [this website](http://hungrylists.herokuapp.com/).

## Startup
The base page `/` will show a landing page, with links to `Login` and `Sign up`.

Clicking links to either `login` or `signup` while already logged in will redirect the user to their `/grocerylist` page. Otherwise, they'll go to the link clicked.

From the `/login` page, the user can enter existing credentials to log in, or click the link to go to the `/signup` page.
* Entering a username that does not exist, or an existing username with an incorrect password, will display the error "Incorrect username or password."

From the `/signup` page, a user may create a new account.
* Passwords are encrypted before being stored in the database. Both encryption and decryption (for password checks in `/login`) are done server-side.
* Entering a username that already exists will flash the error "That email is taken. Sorry!"

Attempting to access a login-only page (`/grocerylist`, `/recipelist`, `/recipe`) while not logged in will redirect the user to the landing page and display the error "You must be logged in to view that page."

## `/grocerylist`
This page will display ingredients that you have chosen to save from recipes. By default, the list will be empty, and prompt you to check out recipes. After you add ingredients, you can delete them individually from this page.

## `/recipelist`
You can view your saved recipes here. You can also enter a type of ingredient (e.g. try "egg" or "potato"!) and click "Search" to find the top 10 recipes that feature that ingredient.

You may add and remove recipes from your saved list (remember to click "Save Changes" afterwards, and give it a few seconds), or click "More Details" to check out the recipe's summary and ingredients.

## `/recipe`
You can only access this page by clicking a specific "More Details" link, as the URL will contain encoding to specify a particular recipe.

This page contains an image and summary of the particular recipe, as well as a list of ingredients. At the bottom of the page, you can choose ingredients your kitchen is missing, and add them to your grocery list (which will add the amount needed for this particular recipe).

You can click buttons to Like or Dislike a recipe (the corresponding button will be highlighted anytime you visit the page for a recipe you've already liked or disliked, so you can quickly tell your opinion on recipes you've seen before). You can also save or un-save the recipe from this page.


<br><br>
# Implement and develop from this app

## Requirements
1. `npm install`
2. `pip install -r requirements.txt`



## Run Application Locally
1. In your project directory, run command: `npm run build`. This will update anything related to your `App.js` file (i.e. `public/index.html`, any CSS you're pulling in, etc), so be sure to do this anytime you change any components related to the React page!
2. In your project directory, run command: `python3 app.py`
3. Preview web page in browser at 'localhost:8081/'

## Set up Heroku
> (remember that all commands starting with `heroku` must have `-a <APPNAME>` added to the end, though the `heroku create` command can be left without if you want an automatically-generated name.)
1. Create a Heroku app: `heroku create --buildpack heroku/python`
2. Add nodejs buildpack: `heroku buildpacks:add --index 1 heroku/nodejs`
3. Add database: `heroku addons:create heroku-postgresql`
4. On your [Heroku app dashboard](https://dashboard.heroku.com/apps), under "Settings" -> "Reveal Config Vars", create a new variable called `DATABASE_URL_QL` and copy the value from `DATABASE_URL` into it. In the new variable name, change `postgres://` to `postgresql://`.

## Configure Other Heroku Variables
1. Go to your [Heroku app dashboard](https://dashboard.heroku.com/apps) and navigate to your app. Under the "Settings" tab, click "Reveal Config Vars".
2. Generate a long, random `bytes` or `str` variable. One way to do this is running on the command line: `python3 -c "import secrets; print(secrets.token_hex())"`. Save the output as a Config Variable called `SECRET_KEY`.
3. Go to [Spoonacular](https://spoonacular.com/food-api) and register to get an API key appropriate to the level of use you expect for your app. Save the key as a Config Variable called `SPOON_API_KEY`.
4. Go to [Rapid API](https://rapidapi.com/) and register to get an API key. Save the key as a Config Variable called `x-rapidapi-key`.
5. Run `python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"` and save the output as a Config Variable called `PASSWORD_KEY`.

## Configure variables for local development
If you want to develop locally, create a file in your repository called `.env`. Copy each Config Variable into that file in the following format:

> `export VARIABLE_NAME="VARIABLE_CONTENT"`

This file is included in the `.gitignore` so that they do not get committed. Be sure you do not save/commit these keys elsewhere.


## Deploy to Heroku
1. Push to Heroku: `git push heroku main`
2. You can now view your app at APP_NAME.herokuapp.com!
