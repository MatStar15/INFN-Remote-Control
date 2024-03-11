from flask import Blueprint, render_template, request
from src.manager import *

main = Blueprint("main", __name__)


# @main.route('/synch')
# def hello():
#     return render_template('synch.html', **test_value)
    
@main.route('/')
def home():
    return render_template('index.html')
    
@main.route('/test')
def test():
    return render_template('test.html')

@main.route("/view_file", methods = ["GET"])
def view_file():
    requested_file = request.args.get("file_name")

    FILE_DIR = "text_data\\"
    try:
        with open(FILE_DIR + f"{requested_file}.txt", "r") as file:
            content = file.read()
    except:
        content = "No such File"
    return render_template("view_file.html", content = content) #TODO move load_file to manager.py