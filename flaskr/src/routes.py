from flask import Blueprint, render_template
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
    return render_template('index.html')
