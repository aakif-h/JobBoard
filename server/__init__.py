from flask import render_template, Blueprint, jsonify
from server.Kit import *

pages = Blueprint('pages', __name__)
@pages.route('/', methods=['GET'])
@pages.route('/index.html', methods=['GET','POST'])
def pre_ship():
    try:
        return render_template('index.html')
    except:
        return jsonify(**{'message': 'Unexpected Error'}), ErrorCode_ServerError

@pages.route('/job-view.html', methods=['GET'])
def go_to_job_view():
    try:
        return render_template('job-view.html')
    except:
        return jsonify(**{'message': 'Unexpected Error'}), ErrorCode_ServerError

@pages.route('/login.html', methods=['GET'])
def go_to_login():
    try:
        return render_template('login.html')
    except:
        return jsonify(**{'message': 'Unexpected Error'}), ErrorCode_ServerError

