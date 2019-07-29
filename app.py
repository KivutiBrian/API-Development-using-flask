from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager,create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity


from config import *

# instantiate flask
app = Flask(__name__)
# setup the development config file
app.config.from_object(DevelopmentConfig)
# instanciate db
db = SQLAlchemy(app)
# instantiate marshmallow
ma = Marshmallow(app)
# instanciate Bcrypt
bcrypt = Bcrypt(app)
# instanciate JWT
jwt = JWTManager(app)

from models.Tasks import TasksModel, TaskSchema
from models.Users import User, UserSchema

task_schema = TaskSchema(strict=True)
tasks_schema = TaskSchema(many=True, strict=True)

user_schema = UserSchema(strict=True)
users_schema = UserSchema(strict=True)


@app.before_first_request
def create_tables():
    db.create_all()

# resource not found
@app.errorhandler(404)
def resource_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify({"message":"Resource not found"}), 404

# bad request
@app.errorhandler(400)
def bad_request(e):
    # note that we set the 400 status explicitly
    return jsonify({"message":"Check your request body"}), 400

# method not allowes
@app.errorhandler(405)
def bad_request(e):
    # note that we set the 400 status explicitly
    return jsonify({"message":"Check your request body"}), 405


# internal server error
@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 404 status explicitly
    return jsonify({"message":"There was a problem with the server"}), 500

# home route
@app.route('/')
def home():
    return jsonify({"message":"You are now welcome to python"}), 200

# creating a new task
@app.route('/tasks', methods=['POST'])
@jwt_required
def createTask():
    # check if the data is json
    if request.is_json:
        data = request.get_json(force=True)
        title = data['title']
        description = data['description']
        
        # send to the DB. instance of the Task Model
        task = TasksModel(title=title,description=description,user_id=get_jwt_identity())
        # insert the the record to the DB
        record = task.insert_record()
        return  task_schema.jsonify(record), 201
    else:
        jsonify({'message':'JSON request expected'}), 400

# update an existing task
@app.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required
def updateTask(id):
    # check if the data is json
    if request.is_json:
        data = request.get_json(force=True)

        title=description=status=None

        if u'title' in data:
            title = data['title']
        if u'description' in data:
            description = data['description']
        if u'status' in data:
            status = data['status'] 
            status = int(status)
        
        update_record = TasksModel.update_by_id(id=id,title=title,description=description,status=status)
        return task_schema.jsonify(update_record), 200

    else:
        jsonify({'message':'JSON request expected'}), 400

# get all records
@app.route('/tasks', methods=['GET'])
@jwt_required
def fetch_all():
    records = TasksModel.fetch_all()    
    return tasks_schema.jsonify(records),200 

# getting a task by a particular user
@app.route('/tasks', methods=['GET'])
@jwt_required
def fetch_task():
    # getting user id
    uid = get_jwt_identity()
    user = User.fetch_by_id(id=uid)
    return tasks_schema.jsonify(user.tasks),200
s
# delete a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required
def delete_task(id):
    delete = TasksModel.delete_by_id(id=id)
    return jsonify({"message":"Task deleted successfully"}),200

# create a new user
@app.route('/users',methods=['POST'])
def add_user():
    # check if the data is json
    if request.is_json:
        data = request.get_json(force=True)
        username = data['username']
        email = data['email']
        password = data['password']

        # hashing the password
        harshed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        #check if user exist
        if User.check_username(username):
            return jsonify({'message':'Username already exists'}),409
        if User.check_email(email):
            return jsonify({'message':'Email already exists'}),409  
        
        addUser = User(username=username,email=email,password=harshed_password)

        try:
            record = addUser.insert_record()
            # creating an acess token to enable a user access a resource
            access_token = create_access_token(identity=record.id)
            # to renew an access token
            refresh_token = create_refresh_token(identity=record.id)

            return jsonify({'acess_token':access_token,"refresh_token":refresh_token}),200

            # return user_schema.jsonify(record),200
        except Exception as e:
            return jsonify({'message':'Error adding user'}),500
  
    else:
        jsonify({'message':'JSON request expected'}), 400

# special endpoint used to refresh token
@app.route('/users/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh_token():
    id = get_jwt_identity()
    access = create_access_token(identity=id)
    return jsonify({"access_token":access}),200
    

# login
@app.route('/users', methods=['PUT'])
def login_user():
    # check if the data is json
    if request.is_json:
        data = request.get_json(force=True)
        username = data['username']
        password = data['password']

        # first chech if the user exist || if true check if the password check is correct
        if User.check_username(username=username):
            if User.check_password(username,password):

                user = User.fetch_by_username(username=username)
                access = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)

                return jsonify({'acess_token':access,"refresh_token":refresh_token})
            else:
                return jsonify({'message':'Invalid password'}),401
        else:
            return jsonify({'message':'User not recognised'}),401

        
        


if __name__ == '__main__':
    app.run(debug=False)