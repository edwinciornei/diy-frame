from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient


app = Flask(__name__)
app.secret_key = "mysecretkey"

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['garage_sale']
items_collection = db['items']

# Database model
class Item:
    def __init__(self, items_collection):
        self.id = str(items_collection['id'])
        self.title = items_collection['title']
        self.description = items_collection['description']
        self.price = items_collection['price']
        self.sold = items_collection['sold']

# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    items = items_collection.find()
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
