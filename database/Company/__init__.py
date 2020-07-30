from sqlalchemy import Column, Integer, String
from database import Base, db_session
from random import randint

class Company(Base):

    params = [ 'name', 'user_id', 'num_employees', 'description',]

    __tablename__ = "Company"
    
    name = Column(String, primary_key=False, nullable=True, unique=True)
    user_id = Column(Integer, primary_key=False, nullable=True, unique=True)
    num_employees = Column(Integer, primary_key=False, nullable=True, unique=True)
    description = Column(String, primary_key=False, nullable=True, unique=True)
    id = Column(Integer, primary_key=True, nullable=False, unique=True)

    def __init__(self, name,user_id,num_employees,description):
        
        self.name = name
        self.user_id = user_id
        self.num_employees = num_employees
        self.description = description

        # set the id of the object to a random value
        # using a range unlikely to collide with other ids
        self.id = randint(0, 1000000)

    def __repr__(self):
        return '[Company %r]' %self.id

    def __iter__(self):
        
        yield 'name', self.name
        yield 'user_id', self.user_id
        yield 'num_employees', self.num_employees
        yield 'description', self.description

    def __getitem(self, item):
        object_as_dict = dict(self)
        if item in object_as_dict:
            return object_as_dict[item]
        return None

def isValidCompany(obj_id):
    try:
        return Company.query.filter(Company.id==obj_id).one_or_none() is not None
    except Exception:
        return False

def createCompany(*args):
    if not isValidCompany(args[0]):
        new_obj = Company(*args)
        db_session.add(new_obj)
        db_session.commit()
        return new_obj
    return dict() # an empty dict in case you are using **{} on this function's output

def readCompany(queries):
    attr = val = ""
    try:
        filter_list = []
        for attr, val in queries.items():
            filter_list.append(getattr(Company, attr) == str(val))
        Company_list = Company.query.filter(*filter_list).all()
        return Company_list if len(Company_list) > 1 else Company_list[0]
    except Exception as e:
        print("An exception occurred with the following details:\n{}".format(str(e)))
        print("Attribute: {}\tValue: {}\n".format(attr, val))
        return None

def updateCompany(obj_id, **kwargs):
    if not isValidCompany(obj_id):
        return False

    retrieved_object = readCompany({"id":obj_id})

    for key, value in kwargs.items():
        if key in Company.params:
            
            if key == 'name':
                retrieved_object.name = value
            if key == 'user_id':
                retrieved_object.user_id = value
            if key == 'num_employees':
                retrieved_object.num_employees = value
            if key == 'description':
                retrieved_object.description = value

    db_session.commit()
    return True

def deleteCompany(obj_id):
    if not isValidCompany(obj_id):
        return False

    retrieved_object = readCompany({"id":obj_id})

    db_session.delete(retrieved_object)
    db_session.commit()
    return True

