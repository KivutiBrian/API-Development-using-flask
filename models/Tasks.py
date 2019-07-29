from app import db, ma
from datetime import datetime

class TasksModel(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False, unique=False)
    description = db.Column(db.String(), nullable=False, unique=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_started = db.Column(db.DateTime)
    date_completed = db.Column(db.DateTime)
    date_cancelled = db.Column(db.DateTime)
    status = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # creating a new record
    # instance method: accesses only that instance of the class
    def insert_record(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    # fetch all records
    @classmethod
    def fetch_all(cls):
        return cls.query.all()


    # update record by id
    # class instance accesses all the instances of that class
    @classmethod
    def update_by_id(cls,id, title=None, description=None, status=None):

        # 0 = todo , 1 = ongoing, 2 = completed, 3 = cancelled

        record = cls.query.filter_by(id=id).first()
        current_status = record.status

        if record:
            if title:
                record.title = title
            if description:
                record.description = description
            if status:
                if status == current_status:
                    pass
                else:
                    if status == 0: #todo state
                        record.status = status  
                        record.date_started = record.date_completed = record.date_cancelled = None
                    elif status == 1: #ongoing
                        record.date_started = datetime.now()
                        record.status = status
                        record.date_completed = record.date_cancelled = None
                    elif status == 2: #completed
                        record.date_completed = datetime.now()
                        record.status = status
                        record.date_cancelled = None
                    elif status ==3: #cancelled
                        record.date_cancelled = datetime.now()
                        record.status = status
                        record.date_completed = None
                    else:
                        pass
            db.session.commit()
        return cls.query.filter_by(id=id).first()

    # deleting a record by id
    @classmethod
    def delete_by_id(cls,id):
        record = cls.query.filter_by(id=id)
        if record.first():
            record.delete()
            db.session.commit()
            return True
        return False

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'date_created', 'date_started', 'date_completed', 'date_cancelled','status')

