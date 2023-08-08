from flask import Flask, render_template, request, redirect, session, send_file
from flask_mail import Mail, Message
from pymongo import MongoClient
from hashlib import sha256
import configparser
import io
import os


config = configparser.ConfigParser()
config.read('config/config.cfg')
app = Flask(__name__)
app.secret_key = "secret"

app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'diyframe@outlook.com'
app.config['MAIL_PASSWORD'] = config['Mail']['MAIL_PASSWORD']
app.config['MAIL_DEFAULT_SENDER'] = 'diyframe@outlook.com'
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

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
    subject_param = request.args.get('subject', '')
    price = request.args.get('price', '')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message_body = request.form['subject']
        
        msg = Message("HEY THERE", recipients=[email])
        msg.body = f'From: {name} <{email}>\n{message_body}'
        
        try:
            mail.send(msg)
        except Exception as e:
            return f'Error: {e}'
        
        return "Email sent successfully"


    return render_template('contact.html', subject=subject_param, price=price)


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


# ADMIN LOGIN
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


# READ
@app.route("/home/<hash_image>", methods=['GET'])
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
