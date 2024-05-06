from gevent import monkey
import gevent, eventlet
monkey.patch_all()
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from markupsafe import escape
import hashlib
import random
import os
from flask_socketio import SocketIO, emit
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, timedelta
#import jsonify



app = Flask(__name__)
#THIS IS THE CONNECTION STRING NEEDED TO CONNECT TO THE DATABASE
#app.config['MONGO_URI'] = 'mongodb+srv://farhanmukit0:LnBsfo2rFTk0OSFF@cluster0.otbjk4d.mongodb.net/recipeapp'
app.config['MONGO_URI'] = 'mongodb+srv://farhanmukit0:LnBsfo2rFTk0OSFF@cluster0.otbjk4d.mongodb.net/recipeapp?tls=true&tlsAllowInvalidCertificates=true'


#PASS
app.config['SECRET_KEY'] = 'LnBsfo2rFTk0OSFF'
app.config['UPLOAD_FOLDER'] = 'static/media'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'wav'}

limiter = Limiter(app, key_func=get_remote_address, default_limits=["50 per 10 seconds"])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

socketio = SocketIO(app, logger=True, async_mode = 'gevent')

@app.errorhandler(429)
def lim(e):
    return "Wait to Send More Requests", 429

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
#client = PyMongo.MongoClient("mongodb+srv://farhanmukit0:LnBsfo2rFTk0OSFF@cluster0.otbjk4d.mongodb.net/")
#mongo.db.create_collection('users')

class User(UserMixin):
    def __init__(self, username, password_hash=None, auth_token_hash=None, _id=None):
        self.username = username
        self.password_hash = password_hash
        self.auth_token_hash = auth_token_hash
        self._id = _id
        

    def get_id(self):
        return str(self._id)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def set_auth_token(self, token):
        self.auth_token_hash = bcrypt.generate_password_hash(token).decode('utf-8')

    def check_auth_token(self, token):
        return bcrypt.check_password_hash(self.auth_token_hash, token)

@login_manager.user_loader
def load_user(user_id):
    u = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not u:
        return None
    return User(username=u['username'], password_hash=u['password_hash'], auth_token_hash=u['auth_token_hash'], _id=u['_id'])

@limiter.limit("50 per 10 seconds")
@app.route('/usercreate', methods=['GET', 'POST'])
def home():
    flash("page loaded")

    if request.method == 'POST':
        users_collection = mongo.db.users
        if 'register' in request.form:
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            if password != confirm_password:
                flash('Passwords do not match.')
                return redirect(url_for('home'))

            existing_user = users_collection.find_one({'username': username})
            if existing_user:
                flash('Username already taken.')
                return redirect(url_for('home'))

            new_user = User(username=username)
            new_user.set_password(password)

            users_collection.insert_one({
                'username': new_user.username,
                'password_hash': new_user.password_hash
            })

            flash('Account created, please login.')
            return redirect(url_for('home'))

        elif 'login' in request.form:
            # Login logic
            username = request.form.get('username')
            password = request.form.get('password')

            user_doc = users_collection.find_one({'username': username})
            if user_doc:
                user = User(username=user_doc['username'], password_hash=user_doc['password_hash'], _id=user_doc['_id'])
                if user.check_password(password):
                    auth_token = bcrypt.generate_password_hash(user.username).decode('utf-8')
                    user.set_auth_token(auth_token)

                    users_collection.update_one({'_id': user._id}, {'$set': {'auth_token_hash': user.auth_token_hash}})

                    login_user(user)

                    resp = make_response(redirect(url_for('home')))
                    resp.set_cookie('auth_token', auth_token, httponly=True, max_age=3600)
                    print('passok')
                    return resp
            flash('Invalid credentials.')
            return redirect(url_for('home'))

    return render_template('index.html', user=current_user)

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('auth_token', '', expires=0, path='/')



    return resp


@app.route('/recipe', methods=['GET', 'POST'])
@login_required
def recipepage():
    recipes_collection = mongo.db.recipes
    comments_collection = mongo.db.comments

    if request.method == 'POST':
         
        if 'addcomment' in request.form:
            comments_collection.insert_one({
                'content': request.form.get('comment'),
                'user': current_user.username,
                'recipeid': ObjectId(request.form.get('recipe_id'))
            })
            return redirect(url_for('recipepage'))
        elif 'addrecipe' in request.form:
            if 'mediafile' in request.files:
                mediafile = request.files['mediafile']
                # If the user does not select a file, the browser submits an
                # empty file without a filename.
                if mediafile.filename == '':
                    flash('No selected file', 'warning')
                    return redirect(request.url)
                if mediafile and allowed_file(mediafile.filename):
                    filename = mediafile.filename
                    mime_type = mediafile.mimetype
                    if mime_type.startswith('image/'):
                        filetype = 'image'
                    elif mime_type.startswith('video/'):
                        filetype = 'video'
                    elif mime_type.startswith('audio/'):
                        filetype = 'audio'
                    else:
                        flash('Invalid file type', 'danger')
                        return redirect(request.url)

                    # Generate a unique filename
                    filename = f"{filetype}_{random.randint(0, 999999)}.{filename.rsplit('.', 1)[1].lower()}"

                    # Save file
                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                    mediafile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    
                    # Add media HTML to the recipe
                    media_html = ''
                    if filetype == 'image':
                        media_html = f'<img src="/{app.config["UPLOAD_FOLDER"]}/{filename}?{{ cache_bust }}" alt="Uploaded image" width="100" height="100">'
                    elif filetype == 'video':
                        media_html = f'<video width="320" height="240" controls><source src="/{app.config["UPLOAD_FOLDER"]}/{filename}?{{ cache_bust }}" type="{mime_type}"></video>'
                    elif filetype == 'audio':
                        media_html = f'<audio controls><source src="/{app.config["UPLOAD_FOLDER"]}/{filename}?{{ cache_bust }}" type="{mime_type}"></audio>'


                    # Save recipe with media content
                    new_recipe = {
                        'recipename': request.form.get('recipename'),
                        'ingredients': request.form.get('recipeingredients'),
                        'description': request.form.get('recipedescription'),
                        'username': current_user.username,
                        'media' : media_html,
                        'filetype' : filetype
                    }
                recipes_collection.insert_one(new_recipe)
                flash('Recipe with media uploaded successfully!', 'success')
                return redirect(url_for('recipepage'))

   
        
    all_recipes = list(recipes_collection.find())
    for recipe in all_recipes:
        recipe['comments'] = list(comments_collection.find({'recipeid': ObjectId(recipe['_id'])}))
    cache_bust = random.randint(0,9999)
    

    return render_template("recipe.html", recipes=all_recipes, user=current_user, cache_bust=cache_bust)

def verify_token(auth_token):
    user = User.query.filter_by(auth_token=auth_token).first()
    if user:
        return user
    else:
        return None


@app.before_request
def before_request_func():
    if request.endpoint in ['home', 'static', None] or 'usercreate' in request.path:
        return

    if current_user.is_authenticated:
        auth_token = request.cookies.get('auth_token')
        if auth_token:
            if not current_user.check_auth_token(auth_token):
                flash("Session invalid or expired. Please log in again.", "warning")
                return logout()
        else:
            flash("Please log in to continue.", "info")
            return redirect(url_for('home'))


@app.after_request
def set_response_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.route('/')
def homepage():
    return render_template("landing.html")

@app.route('/health')
def healthCheck():
    return 'OK', 200


@app.route('/meltingpot')
@login_required
def live_chat():
    return render_template('meltingpot.html')

@limiter.limit("50 per 10 seconds")
@app.route('/landing')
def landing_page():
    return render_template('landing.html', user=current_user)

@socketio.on('message')
def handleMessage(msg):
    if current_user.is_authenticated:
        msg = f"{current_user.username}: {msg}"
    emit('message', msg, broadcast = True)

##################################################



# ingredients = [
#     "Spaghetti", "Eggs", "Guanciale", "Pecorino Cheese", "Black Pepper", 
#     "Chicken", "Bacon", "Parmesan", "Cream", "Onions", "Garlic", 
#     "Mushrooms", "Parsley", "Tomato Sauce", "Bread", "Beef", "Pork", "Carrots"
# ]

# mongo.db.ingredients.insert_one({"all_ingredients": ingredients})


# dishes = [
#     {
#         "name": "Spaghetti Carbonara",
#         "ingredients": ["Spaghetti", "Eggs", "Guanciale", "Pecorino Cheese", "Black Pepper"]
#     },
#     {
#         "name": "Margherita Pizza",
#         "ingredients": ["Pizza Dough", "Tomato Sauce", "Mozzarella Cheese", "Basil"]
#     }
# ]

# mongo.db.dishes.insert_many(dishes)

# new_ingredients = [
#     "Tomatoes", "Cucumber", "Spinach", "Rice", "Beans",
#     "Beef", "Pork", "Carrots", "Vinegar", "Soy Sauce",
#     "Chicken Broth", "Sour Cream", "Chives", "Tortillas", "Fish"
# ]

# new_dishes = [
#     {
#         "name": "Beef Taco",
#         "ingredients": ["Beef", "Cheese", "Tomatoes", "Tortillas", "Sour Cream"]
#     },
#     {
#         "name": "Vegetable Stir Fry",
#         "ingredients": ["Rice", "Carrots", "Beans", "Soy Sauce", "Chicken Broth"]
#     },
#     {
#         "name": "Chicken Salad",
#         "ingredients": ["Chicken", "Lettuce", "Tomatoes", "Cucumber", "Vinegar"]
#     }
# ]


# mongo.db.ingredients.update_one({}, { '$addToSet': { 'all_ingredients': { '$each': new_ingredients } }})

# mongo.db.dishes.insert_many(new_dishes)


@app.route('/scramble')
def game():
    return render_template('scramble.html')

@app.route('/scramble/start')
def start_game():
    dishes = list(mongo.db.dishes.find())
    if not dishes:
        return jsonify({'error': 'No dishes available'}), 404

    selected_dish = random.choice(dishes)
    correct_ingredients = selected_dish['ingredients']
    all_ingredients = mongo.db.ingredients.find_one()['all_ingredients']
    incorrect_ingredients = [ing for ing in all_ingredients if ing not in correct_ingredients]
    random.shuffle(incorrect_ingredients)
    selected_ingredients = correct_ingredients + incorrect_ingredients[:10]
    random.shuffle(selected_ingredients)

    game_id = mongo.db.games.insert_one({
        'dish_id': selected_dish['_id'],
        'dish_name': selected_dish['name'],
        'correct_ingredients': correct_ingredients,
        'selected_ingredients': selected_ingredients,
        'guessed_ingredients': [],
        'hints': [],
        'attempts': 0
    }).inserted_id
    return jsonify(game_id=str(game_id), dish_name=selected_dish['name'], ingredients=selected_ingredients)

@app.route('/scramble/guess', methods=['POST'])
def guess_ingredients():
    game_id = request.json['game_id']
    guessed_ingredient = request.json['guessed_ingredient']
    game = mongo.db.games.find_one({'_id': ObjectId(game_id)})

    if not game:
        return jsonify({'error': 'Game not found'}), 404

    # Retrieve or initialize guessed ingredients
    guessed_ingredients = set(game.get('guessed_ingredients', []))
    guessed_ingredients.add(guessed_ingredient)

    # Update guessed ingredients in database
    mongo.db.games.update_one({'_id': ObjectId(game_id)}, {'$set': {'guessed_ingredients': list(guessed_ingredients)}})

    correct_ingredients = set(game['correct_ingredients'])
    hits = guessed_ingredients.intersection(correct_ingredients)

    # Check if all correct ingredients have been guessed
    if guessed_ingredients >= correct_ingredients:
        mongo.db.games.update_one({'_id': ObjectId(game_id)}, {'$set': {'completed': True}})
        return jsonify({'win': True, 'attempts': game['attempts'] + 1})

    # Provide hint if not all ingredients are guessed correctly
    hint = random.choice(list(correct_ingredients - hits)) if correct_ingredients != hits else None
    return jsonify({
        'correct': guessed_ingredient in correct_ingredients,
        'hits': list(hits),
        'hint': hint,
        'attempts': game['attempts'] + 1
    })


@app.route('/leaderboard')
def leaderboard():
    leaders = mongo.db.leaderboard.find().sort('attempts')
    return render_template('leaderboard.html', leaders=leaders)


if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app, debug=True)
