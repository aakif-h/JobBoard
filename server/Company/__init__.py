from flask import Flask, jsonify, request, Blueprint
from database.Company import *
from server.Kit import *
from config import tokenCheck

blueprint_Company = Blueprint('blueprint_Company', __name__)

@blueprint_Company.route("/createCompany", methods = ['POST'])
def createCompanyRoute():
    data = request.get_json()

    
    if not checkParam(data, 'appToken') or not tokenCheck(data['appToken']):
        return jsonify(**{'message':'Unsupported App'}), ErrorCode_BadParams


    # the id parameter does not need checking on object creation
    params_on_create = Company.params
    try:
        params_on_create.remove('id')
    except ValueError:
        pass
    if not checkParams(data, *params_on_create):
        return jsonify(**{'message':'Bad Params'}), ErrorCode_BadParams

    new_Company = createCompany(
        data['name'],
        data['user_id'],
        data['num_employees'],
        data['description'],)
    if new_Company is None:
        return jsonify(**{'message':'Bad Params'}), ErrorCode_ServerError
    return jsonify(**dict(new_Company)), ErrorCode_Success


@blueprint_Company.route("/readCompany", methods = ['POST'])
def readCompanyRoute():
    data = request.get_json()

    
    if not checkParam(data, 'appToken') or not tokenCheck(data['appToken']):
        return jsonify(**{'message':'Unsupported App'}), ErrorCode_BadParams

    
    if not checkParam(data, 'filters'):
        return jsonify(**{'message':'Bad Params'}), ErrorCode_BadParams

    retrieved_Company_list = readCompany(**data)
    if retrieved_Company_list is None:
        return jsonify(**{'Company':''}), ErrorCode_Success
    
    Company_json_list = []
    try:
        for Company in retrieved_Company_list:
            Company_json_list.append(dict(Company))
        return jsonify(**{'Company':Company_json_list}), ErrorCode_Success
    except Exception as e:
        if e.__class__.__name__ in ('ValueError', 'TypeError'):
            return jsonify(**{'Company':dict(retrieved_Company_list)}), ErrorCode_Success
        else:
            print("An exception has occurred!\n{}".format(str(e)))
            return jsonify(**{'message': '{}'.format(str(e))}), ErrorCode_ServerError


@blueprint_Company.route("/updateCompany", methods = ['POST'])
def updateCompanyRoute():
    data = request.get_json()

    
    if not checkParam(data, 'appToken') or not tokenCheck(data['appToken']):
        return jsonify(**{'message':'Unsupported App'}), ErrorCode_BadParams


    if not checkParam(data, 'id'):
        return jsonify(**{'message':'Bad Params'}), ErrorCode_BadParams

    if not (updateCompany(int(data['id']), **data)):
        return jsonify(**{'message':'Bad object id'}), ErrorCode_NotFound
    return jsonify(**{}), ErrorCode_Success


@blueprint_Company.route("/deleteCompany", methods = ['POST'])
def deleteCompanyRoute():
    data = request.get_json()

    
    if not checkParam(data, 'appToken') or not tokenCheck(data['appToken']):
        return jsonify(**{'message':'Unsupported App'}), ErrorCode_BadParams


    if not checkParam(data, 'id'):
        return jsonify(**{'message':'Bad Params'}), ErrorCode_BadParams

    if not (deleteCompany(int(data['id']))):
        return jsonify(**{'message':'Bad object id'}), ErrorCode_NotFound
    return jsonify(**{}), ErrorCode_Success


if __name__ == "__main__":
    SERVER_ROOT = "127.0.0.1"
    app = Flask(__name__)
    app.debug = True
    app.register_blueprint(blueprint_Company)
    app.run(port=2446)

