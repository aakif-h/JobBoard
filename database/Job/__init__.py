from sqlalchemy import Column, Integer, String
from database import Base, db_session
from random import randint

class Job(Base):

    params = [ 'title', 'user_id', 'company_id', 'job_link', 'number_applicants', 'description',]

    __tablename__ = "Job"
    
    title = Column(String, primary_key=False, nullable=True, unique=True)
    user_id = Column(Integer, primary_key=False, nullable=True, unique=True)
    company_id = Column(Integer, primary_key=False, nullable=True, unique=True)
    job_link = Column(String, primary_key=False, nullable=True, unique=True)
    number_applicants = Column(Integer, primary_key=False, nullable=True, unique=True)
    description = Column(String, primary_key=False, nullable=True, unique=True)
    id = Column(Integer, primary_key=True, nullable=False, unique=True)

    def __init__(self, title,user_id,company_id,job_link,number_applicants,description):
        
        self.title = title
        self.user_id = user_id
        self.company_id = company_id
        self.job_link = job_link
        self.number_applicants = number_applicants
        self.description = description

        # set the id of the object to a random value
        # using a range unlikely to collide with other ids
        self.id = randint(0, 1000000)

    def __repr__(self):
        return '[Job %r]' %self.id

    def __iter__(self):
        
        yield 'title', self.title
        yield 'user_id', self.user_id
        yield 'company_id', self.company_id
        yield 'job_link', self.job_link
        yield 'number_applicants', self.number_applicants
        yield 'description', self.description

    def __getitem(self, item):
        object_as_dict = dict(self)
        if item in object_as_dict:
            return object_as_dict[item]
        return None

def isValidJob(obj_id):
    try:
        return Job.query.filter(Job.id==obj_id).one_or_none() is not None
    except Exception:
        return False

def createJob(*args):
    if not isValidJob(args[0]):
        new_obj = Job(*args)
        db_session.add(new_obj)
        db_session.commit()
        return new_obj
    return dict() # an empty dict in case you are using **{} on this function's output

def readJob(queries):
    attr = val = ""
    try:
        filter_list = []
        for attr, val in queries.items():
            filter_list.append(getattr(Job, attr) == str(val))
        Job_list = Job.query.filter(*filter_list).all()
        return Job_list if len(Job_list) > 1 else Job_list[0]
    except Exception as e:
        print("An exception occurred with the following details:\n{}".format(str(e)))
        print("Attribute: {}\tValue: {}\n".format(attr, val))
        return None    

def updateJob(obj_id, **kwargs):
    if not isValidJob(obj_id):
        return False

    retrieved_object = readJob({"id":obj_id})

    for key, value in kwargs.items():
        if key in Job.params:
            
            if key == 'title':
                retrieved_object.title = value
            if key == 'user_id':
                retrieved_object.user_id = value
            if key == 'company_id':
                retrieved_object.company_id = value
            if key == 'job_link':
                retrieved_object.job_link = value
            if key == 'number_applicants':
                retrieved_object.number_applicants = value
            if key == 'description':
                retrieved_object.description = value

    db_session.commit()
    return True

def deleteJob(obj_id):
    if not isValidJob(obj_id):
        return False

    retrieved_object = readJob({"id":obj_id})

    db_session.delete(retrieved_object)
    db_session.commit()
    return True

