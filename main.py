from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
from hashlib import sha256


app = Flask(__name__)
app.secret_key = "secret"

# MongoDB connection
cl = MongoClient('mongodb://localhost:27017')
db = cl.garage_sale
db_items = db.items

# ROUTES
@app.route('/', methods=['GET', 'POST'])
def home():
    if not session:
        return redirect("/adminlogin", "You need to login first")
    return render_template('home.html')

# CONTACT
@app.route('/contact',  methods=['GET', 'POST'])
def contact():
    return 'Contact'


# WRAPPER
def requires_admin(route_func):

    def wrapper():
        admin = session.get("admin")
        if admin:
            return route_func()
        else:
            return redirect("/unauthorized")
    
    wrapper.__name__ = route_func.__name__

    return wrapper


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
            error="¡Invalid user or password!",
            username=username,
            password=password
            )


# UNAUTHORIZED
@app.route("/unauthorized")
def unauthorized():
    return "Unauthorized"


# LOGOUT      
@app.route('/logout')
@requires_admin
def logout():
    if 'admin' in session:
        session.pop('admin')

    return redirect("/adminlogin")


# UPLOAD
@app.route("/upload", methods=['GET', 'POST'])
@requires_admin
def imagine():
    if request.method == 'GET':
        return render_template('upload.html')
    
    origin_name = request.files['file'].filename
    data = request.files['file'].stream.read()
    hash_image = sha256(data).hexdigest()

    image_from_db = db_items.find_one({"sha256": hash_image})
    
    if not image_from_db:
        db_items.insert_one({
            'name': origin_name,
            'sha256': hash_image,
            'date': data
            
        })
    return render_template("upload.html", img_ids = [img['sha256'] for img in db_items])

if __name__ == "__main__":
    app.run('0.0.0.0', port=80, debug=True)
