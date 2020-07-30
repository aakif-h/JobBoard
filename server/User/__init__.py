from flask import Flask, jsonify, request, Blueprint
from database.User import *
from server.Kit import *
from config import tokenCheck

blueprint_User = Blueprint('blueprint_User', __name__)

@blueprint_User.route("/createUser", methods = ['POST'])
def createUserRoute():
    data = request.get_json()

    
    if not checkParam(data, 'appToken') or not tokenCheck(data['appToken']):
        return jsonify(**{'message':'Unsupported App'}), ErrorCode_BadParams


    # the id parameter does not need checking on object creation
    params_on_create = User.params
    try:
        params_on_create.remove('id')
    except ValueError:
        pass
    if not checkParams(data, *params_on_create):
        return jsonify(**{'message':'Bad Params'}), ErrorCode_BadParams

    new_User = createUser(
        data['user_type'],
        data['username'],
        data['password'],
        data['company_id'],)
    if new_User is None:
        return jsonify(**{'message':'Bad Params'}), ErrorCode_ServerError
    return jsonify(**dict(new_User)), ErrorCode_Success


@blueprint_User.route("/readUser", methods = ['POST'])
def readUserRoute():
    data = request.get_json()

    
    if not checkParam(data, 'appToken') or not tokenCheck(data['appToken']):
        return jsonify(**{'message':'Unsupported App'}), ErrorCode_BadParams

    
    if not checkParam(data, 'filters'):
        return jsonify(**{'message':'Bad Params'}), ErrorCode_BadParams

    retrieved_User_list = readUser(**data)
    if retrieved_User_list is None:
        return jsonify(**{'User':''}), ErrorCode_Success
    
    User_json_list = []
    try:
        for User in retrieved_User_list:
            User_json_list.append(dict(User))
        return jsonify(**{'User':User_json_list}), ErrorCode_Success
    except Exception as e:
        if e.__class__.__name__ in ('ValueError', 'TypeError'):
            return jsonify(**{'User':dict(retrieved_User_list)}), ErrorCode_Success
        else:
            print("An exception has occurred!\n{}".format(str(e)))
            return jsonify(**{'message': '{}'.format(str(e))}), ErrorCode_ServerError


@blueprint_User.route("/updateUser", methods = ['POST'])
def updateUserRoute():
    data = request.get_json()

    
    if not checkParam(data, 'appToken') or not tokenCheck(data['appToken']):
        return jsonify(**{'message':'Unsupported App'}), ErrorCode_BadParams


    if not checkParam(data, 'id'):
        return jsonify(**{'message':'Bad Params'}), ErrorCode_BadParams

    if not (updateUser(int(data['id']), **data)):
        return jsonify(**{'message':'Bad object id'}), ErrorCode_NotFound
    return jsonify(**{}), ErrorCode_Success


@blueprint_User.route("/deleteUser", methods = ['POST'])
def deleteUserRoute():
    data = request.get_json()

    
    if not checkParam(data, 'appToken') or not tokenCheck(data['appToken']):
        return jsonify(**{'message':'Unsupported App'}), ErrorCode_BadParams


    if not checkParam(data, 'id'):
        return jsonify(**{'message':'Bad Params'}), ErrorCode_BadParams

    if not (deleteUser(int(data['id']))):
        return jsonify(**{'message':'Bad object id'}), ErrorCode_NotFound
    return jsonify(**{}), ErrorCode_Success


if __name__ == "__main__":
    SERVER_ROOT = "127.0.0.1"
    app = Flask(__name__)
    app.debug = True
    app.register_blueprint(blueprint_User)
    app.run(port=2446)

