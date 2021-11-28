## Heroku Link: Sprint 2
[http://hungrylists.herokuapp.com/](http://hungrylists.herokuapp.com/)

### Sprint 1 Link
[http://project2-csc4350.herokuapp.com/](http://project2-csc4350.herokuapp.com/)
<br><br>

# Hungrylists Usage
Welcome! Hungrylists can be accessed from [this website](http://hungrylists.herokuapp.com/).

## Startup
The base page `/` will redirect the user to `/login` if they are not signed in, or `/grocerylist` if they are.

From the `/login` page, the user can enter existing credentials to log in, or click the link to go to the `/signup` page.
* Entering a username that does not exist, or an existing username with an incorrect password, will display the error "Incorrect username or password."

From the `/signup` page, a user may create a new account.
* Passwords are encrypted before being stored in the database. Both encryption and decryption (for password checks in `/login`) are done server-side.
* Entering a username that already exists will flash the error "That username is taken. Sorry!"

Attempting to access a login-only page (`/grocerylist`, `/recipelist`, `/recipe`) while not logged in will redirect the user to `/login` and display the error "You must be logged in to view that page."

## /recipelist

Upon accessing `/recipelist`, the user can see a search bar and a 



<br><br>
# Implement and develop from this app

## Requirements
1. `npm install`
2. `pip install -r requirements.txt`



## Run Application Locally
1. In your project directory, run command: `npm run build`. This will update anything related to your `App.js` file (i.e. `public/index.html`, any CSS you're pulling in, etc).
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
2. Generate a long, random `bytes` or `str` variable. You can do this by running on the command line: `python -c 'import secrets; print(secrets.token_hex())'`. Save the output as a Config Variable called `SECRET_KEY`.
3. Go to [Spoonacular](https://spoonacular.com/food-api) and register to get an API key appropriate to the level of use you expect for your app. Save the key as a Config Variable called `SPOON_API_KEY`.
4. Go to [Rapid API](https://rapidapi.com/) and register to get an API key. Save the key as a Config Variable called `x-rapidapi-key`.



## Deploy to Heroku
1. Push to Heroku: `git push heroku main`
2. You can now view your app at APP_NAME.herokuapp.com!
