from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

# Create a MongoClient and connect to your MongoDB instance
client = MongoClient('mongodb://localhost:27017')

# Select the "task" database
db = client['task']

# Select the "users" collection
users_collection = db['users']

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST']) 
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the user already exists in the database
        if users_collection.find_one({'email': email}):
            return "User with this email already exists."

        # Insert the user data into the database
        users_collection.insert_one({'email': email, 'password': password})

        # Redirect to a success page or login page
        return "Registration successful! <a href='/login'>Login</a>"

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

         # Check if the user exists in the database
        user = users_collection.find_one({'email': email, 'password': password})

        if user:
            # You can set up a user session here for authentication
            # For simplicity, we'll just return a success message
            return redirect('/myvlog')
        else:
            return "Login failed. Please check your credentials."

    return render_template('login.html')

@app.route('/myvlog')
def myvlog():
    return render_template('myvlog.html')

@app.route('/mystory')
def yourstory():
    return render_template('mystory.html')

@app.route('/followme')
def followme():
    return render_template('followme.html')

if __name__ == '__main__':
    app.run(debug=True)
 