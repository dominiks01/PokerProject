import os
from pymongo import MongoClient
from flask import Flask, request, send_file
from PIL import Image
import auth

from credits import cluster

app = Flask(__name__)
client = MongoClient(cluster)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/images/<path:path>')
def send_image(path):
    img_dir = './Images'
    os.listdir(img_dir)
    img_path = os.path.join(img_dir, path)
    return send_file(img_path, mimetype='image/png')


@app.route('/login')
def login():
    return "login"


@app.route('/login', methods=['POST'])
def handle_login():
    login_data = request.form
    return loginHandler.login(login_data)


@app.route('/register', methods=['POST'])
def handle_register():
    register_data = request.form
    return loginHandler.register(register_data, None)


db = client.PokerProject
loginHandler = auth.AuthHandler(db)
app.run(debug=True, port=5000, host='127.0.0.1')
