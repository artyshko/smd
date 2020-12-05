# REQUIRED FIELDS

__flask_app__ = "my"
__menu_seq__ = "2"
__menu_name__ = "My"
__menu_icon__ = ""
__menu__route = "/"
__visible__ = "1"

###
from flask import Flask
app = Flask(__name__)

@app.route("/my/<artist>")
def my():
    return "Hello World!!!!)!"
