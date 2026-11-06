from flask import Flask 
app = Flask(__name__)


# Define a route for the home page ("/")
@app.route("/")
def index():
    """Returns a simple Hello, World! string."""
    
    return "Hello, World!"


# Define a dynamic route that accepts a name in the URL
@app.route("/greet/<name>")
def greet(name):
    """Returns a personalized greeting."""
    
    return f"Hello, {name}!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)