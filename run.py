from flask import Flask
from server.Job import blueprint_Job
from server.Company import blueprint_Company
from server.User import blueprint_User

#from server.swagger import blueprint_swagger
app = Flask(__name__)

if __name__ == "__main__":
    SERVER_ROOT = "127.0.0.1"
    app.debug = True

    # Register all the routes to the app
    app.register_blueprint(blueprint_Job)
    app.register_blueprint(blueprint_Company)
    app.register_blueprint(blueprint_User)
    

    #app.register_blueprint(blueprint_swagger, url_prefix="/swagger")

    # Startup the connection to the database
    from database import init_db
    init_db()

    # Begin the actual application, serving it at this port number
    app.run(host=SERVER_ROOT, port=2446)

