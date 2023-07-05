import flask

from flask import Blueprint


homeBlueprint = Blueprint('home', __name__)
@homeBlueprint.route('/', methods=['POST', 'GET'])
def home():
    return flask.render_template('home.html')
