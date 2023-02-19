from flask import Flask
from launchServer import server

app = Flask(__name__)


@app.route("/")
def hello_world():
    server()
    return "<p>Hello, World!</p>"
