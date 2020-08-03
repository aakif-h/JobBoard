from flask import render_template, Blueprint, jsonify
from server.Kit import *

pages = Blueprint('pages', __name__)
@pages.route('/', methods=['GET'])
def pre_ship():
    try:
        return render_template('index.html')
    except:
        return jsonify(**{'message': 'Unexpected Error'}), ErrorCode_ServerError