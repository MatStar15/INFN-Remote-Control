from flask import Blueprint, render_template
from src.manager import *
import machineScripts

main = Blueprint("main", __name__)


@main.route('/synch')
def hello():
    return render_template('synch.html', **status)
    
@main.route('/')
def home():
    return render_template('index.html')
    
@main.route('/test')
def test():
    machineScripts.CustomSystem()
    return render_template('index.html')
