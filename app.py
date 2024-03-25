from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from markupsafe import escape
import hashlib


app = Flask(__name__)
#THIS IS THE CONNECTION STRING NEEDED TO CONNECT TO THE DATABASE
app.config['MONGO_URI'] = 'mongodb+srv://farhanmukit0:LnBsfo2rFTk0OSFF@cluster0.otbjk4d.mongodb.net/recipeapp'
#PASS
app.config['SECRET_KEY'] = 'LnBsfo2rFTk0OSFF'

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

@app.route('/logout')
def logout():
    logout_user()
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('auth_token', '', expires=0)



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
            recipes_collection.insert_one({
                'recipename': request.form.get('recipename'),
                'ingredients': request.form.get('recipeingredients'),
                'description': request.form.get('recipedescription'),
                'username': current_user.username
            })
            return redirect(url_for('recipepage'))
        
    all_recipes = list(recipes_collection.find())
    for recipe in all_recipes:
        recipe['comments'] = list(comments_collection.find({'recipeid': ObjectId(recipe['_id'])}))

    return render_template("recipe.html", recipes=all_recipes, user=current_user)


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

if __name__ == '__main__':
    app.run(debug=True)


