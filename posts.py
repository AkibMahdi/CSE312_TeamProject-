from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient 
import html

app = Flask(__name__)
mongo_client = MongoClient("mongo")
db = mongo_client["Pending..."]
recipe_collection = db["recipes"]
chat_collection = db["chat"]
account_collection = db["accounts"]


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user, password = account_collection
        ruser = user.finds_one({'name': request.form['username']})

        if not ruser:
            user.insert_one({'name': request.form['username'], 'password': request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('home'))
        else:
            return 'Username exists already'
        
    return render_template('register.html')
        

@app.route('/login',  methods=['GET', 'POST'])
def login():
    if request.methd == 'POST':
        user, password = account_collection
        ruser = user.finds_one({'name': request.form['username']})

        if ruser:
            if ruser['password'] == request.form['password']:
                session['usename'] == request.form['username']
                return redirect(url_for('home'))
        else:
            return 'Incorrect username and/or password. Try again'
    return render_template('login.html')

@app.route('/recipe', methods=['GET', 'POST'])
def recipes():
    
    return render_template('recipe.html')
            


