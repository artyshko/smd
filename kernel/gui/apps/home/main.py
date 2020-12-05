# REQUIRED FIELDS

__flask_app__ = "home"
__menu_seq__ = "1"
__menu_name__ = "Home"
__menu_icon__ = ""
__menu__route = "/"
__visible__ = "1"

###

from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!"


