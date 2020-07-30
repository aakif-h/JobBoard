from flask import Flask, jsonify, request, Blueprint
from database.Job import *
from server.Kit import *
from config import tokenCheck

blueprint_Job = Blueprint('blueprint_Job', __name__)

@blueprint_Job.route("/createJob", methods = ['POST'])
def createJobRoute():
    data = request.get_json()

    
    if not checkParam(data, 'appToken') or not tokenCheck(data['appToken']):
        return jsonify(**{'message':'Unsupported App'}), ErrorCode_BadParams


    # the id parameter does not need checking on object creation
    params_on_create = Job.params
    try:
        params_on_create.remove('id')
    except ValueError:
        pass
    if not checkParams(data, *params_on_create):
        return jsonify(**{'message':'Bad Params'}), ErrorCode_BadParams

    new_Job = createJob(
        data['title'],
        data['user_id'],
        data['company_id'],
        data['job_link'],
        data['number_applicants'],
        data['description'],)
    if new_Job is None:
        return jsonify(**{'message':'Bad Params'}), ErrorCode_ServerError
    return jsonify(**dict(new_Job)), ErrorCode_Success


@blueprint_Job.route("/readJob", methods = ['POST'])
def readJobRoute():
    data = request.get_json()

    
    if not checkParam(data, 'appToken') or not tokenCheck(data['appToken']):
        return jsonify(**{'message':'Unsupported App'}), ErrorCode_BadParams

    
    if not checkParam(data, 'filters'):
        return jsonify(**{'message':'Bad Params'}), ErrorCode_BadParams

    retrieved_Job_list = readJob(**data)
    if retrieved_Job_list is None:
        return jsonify(**{'Job':''}), ErrorCode_Success
    
    Job_json_list = []
    try:
        for Job in retrieved_Job_list:
            Job_json_list.append(dict(Job))
        return jsonify(**{'Job':Job_json_list}), ErrorCode_Success
    except Exception as e:
        if e.__class__.__name__ in ('ValueError', 'TypeError'):
            return jsonify(**{'Job':dict(retrieved_Job_list)}), ErrorCode_Success
        else:
            print("An exception has occurred!\n{}".format(str(e)))
            return jsonify(**{'message': '{}'.format(str(e))}), ErrorCode_ServerError


@blueprint_Job.route("/updateJob", methods = ['POST'])
def updateJobRoute():
    data = request.get_json()

    
    if not checkParam(data, 'appToken') or not tokenCheck(data['appToken']):
        return jsonify(**{'message':'Unsupported App'}), ErrorCode_BadParams


    if not checkParam(data, 'id'):
        return jsonify(**{'message':'Bad Params'}), ErrorCode_BadParams

    if not (updateJob(int(data['id']), **data)):
        return jsonify(**{'message':'Bad object id'}), ErrorCode_NotFound
    return jsonify(**{}), ErrorCode_Success


@blueprint_Job.route("/deleteJob", methods = ['POST'])
def deleteJobRoute():
    data = request.get_json()

    
    if not checkParam(data, 'appToken') or not tokenCheck(data['appToken']):
        return jsonify(**{'message':'Unsupported App'}), ErrorCode_BadParams


    if not checkParam(data, 'id'):
        return jsonify(**{'message':'Bad Params'}), ErrorCode_BadParams

    if not (deleteJob(int(data['id']))):
        return jsonify(**{'message':'Bad object id'}), ErrorCode_NotFound
    return jsonify(**{}), ErrorCode_Success


if __name__ == "__main__":
    SERVER_ROOT = "127.0.0.1"
    app = Flask(__name__)
    app.debug = True
    app.register_blueprint(blueprint_Job)
    app.run(port=2446)

