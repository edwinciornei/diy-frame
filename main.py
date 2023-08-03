from flask import Flask, render_template, request, redirect, session, send_file
from pymongo import MongoClient
from hashlib import sha256
import io


app = Flask(__name__)
app.secret_key = "secret"

# MongoDB connection
cl = MongoClient('mongodb://localhost:27017')
db = cl.garage_sale
db_items = db.items


# ROUTES
@app.route('/', methods=['GET', 'POST'])
def home():
    images_list = list(db_items.find())
    return render_template("home.html", images=images_list)


# CONTACT
@app.route('/contact',  methods=['GET', 'POST'])
def contact():
    subject = request.args.get('subject', '')
    price = request.args.get('price', '')
    return render_template('contact.html', subject=subject, price=price)


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
        return redirect("/adminlogin")

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


@app.route("/home/<hash_image>", methods=["GET"])
def only_image(hash_image):
    image_from_db = db_items.find_one({"sha256": hash_image})

    if image_from_db:
        return send_file(io.BytesIO(image_from_db['image_data']), 'image/jpg')
    if not image_from_db:
        return "Not found", 404


# UPLOAD
@app.route("/upload", methods=['GET', 'POST'])
@requires_admin
def galery():
    if request.method == 'GET':
        return render_template('upload.html')

    origin_name = request.files['file'].filename
    data = request.files['file'].stream.read()
    hash_image = sha256(data).hexdigest()
    description = request.form['description']
    price = request.form['price']

    image_from_db = db_items.find_one({"sha256": hash_image})

    if not image_from_db:
        db_items.insert_one({
            'name': origin_name,
            'sha256': hash_image,
            'image_data': data,
            'description': description,
            'price': price,
        })

    images_list = [doc for doc in db_items.find()]
    return render_template("home.html",
                           img_ids=[img['sha256'] for img in images_list])


if __name__ == "__main__":
    app.run('0.0.0.0', port=80, debug=True)
