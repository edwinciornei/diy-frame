from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient


app = Flask(__name__)
app.secret_key = "mysecretkey"

# MongoDB connection
cl = MongoClient('mongodb://localhost:27017')
db = cl.garage_sale
items_collection = db.items

# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    if not session.get('username'):
        return redirect("/adminlogin", "You need to login first")
    return render_template('index.html')

@app.route("/adminlogin", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("/admin_login/login.html")
    
    username = request.form.get("username")
    password = request.form.get("password")
    
    if username == 'admin' and password == 'admin':
        session["username"] = username
        session["admin"] = "true"
        return redirect("/")

    else:
        return render_template(
            "/admin_login/login.html", 
            eroare="¡Invalid user or password!",
            username=username,
            password=password
            )

if __name__ == "__main__":
    app.run('0.0.0.0', port=80, debug=True)
