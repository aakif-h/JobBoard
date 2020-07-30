from sqlalchemy import Column, Integer, String
from database import Base, db_session
from random import randint

class User(Base):

    params = [ 'user_type', 'username', 'password', 'company_id',]

    __tablename__ = "User"
    
    user_type = Column(Integer, primary_key=False, nullable=True, unique=True)
    username = Column(String, primary_key=False, nullable=True, unique=True)
    password = Column(String, primary_key=False, nullable=True, unique=True)
    company_id = Column(Integer, primary_key=False, nullable=True, unique=True)
    id = Column(Integer, primary_key=True, nullable=False, unique=True)

    def __init__(self, user_type,username,password,company_id):
        
        self.user_type = user_type
        self.username = username
        self.password = password
        self.company_id = company_id

        # set the id of the object to a random value
        # using a range unlikely to collide with other ids
        self.id = randint(0, 1000000)

    def __repr__(self):
        return '[User %r]' %self.id

    def __iter__(self):
        
        yield 'user_type', self.user_type
        yield 'username', self.username
        yield 'password', self.password
        yield 'company_id', self.company_id

    def __getitem(self, item):
        object_as_dict = dict(self)
        if item in object_as_dict:
            return object_as_dict[item]
        return None

def isValidUser(obj_id):
    try:
        return User.query.filter(User.id==obj_id).one_or_none() is not None
    except Exception:
        return False

def createUser(*args):
    if not isValidUser(args[0]):
        new_obj = User(*args)
        db_session.add(new_obj)
        db_session.commit()
        return new_obj
    return dict() # an empty dict in case you are using **{} on this function's output

def readUser(queries):
    attr = val = ""
    try:
        filter_list = []
        for attr, val in queries.items():
            filter_list.append(getattr(User, attr) == str(val))
        User_list = User.query.filter(*filter_list).all()
        return User_list if len(User_list) > 1 else User_list[0]
    except Exception as e:
        print("An exception occurred with the following details:\n{}".format(str(e)))
        print("Attribute: {}\tValue: {}\n".format(attr, val))
        return None    

def updateUser(obj_id, **kwargs):
    if not isValidUser(obj_id):
        return False

    retrieved_object = readUser({"id":obj_id})

    for key, value in kwargs.items():
        if key in User.params:
            
            if key == 'user_type':
                retrieved_object.user_type = value
            if key == 'username':
                retrieved_object.username = value
            if key == 'password':
                retrieved_object.password = value
            if key == 'company_id':
                retrieved_object.company_id = value

    db_session.commit()
    return True

def deleteUser(obj_id):
    if not isValidUser(obj_id):
        return False

    retrieved_object = readUser({"id":obj_id})

    db_session.delete(retrieved_object)
    db_session.commit()
    return True

