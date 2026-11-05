from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'
