from app import db,ma,bcrypt

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String())
    tasks = db.relationship('TasksModel', backref='user')

    # add record
    def insert_record(self):
        db.session.add(self)
        db.session.commit()
        return self

    # fetch by username
    @classmethod
    def fetch_by_username(cls,username):
        return cls.query.filter_by(username=username).first()

    # fetch by email
    @classmethod
    def fetch_by_email(cls,email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def fetch_by_id(cls,id):
        return cls.query.filter_by(id=id).first()
        
    # update
    @classmethod
    def update_by_id(cls,id, username=None, email=None):
        record = cls.query.filter_by(id=id).first()
        if record:
            if username:
                record.username = username
            if email:
                record.email = email
            db.session.commit()
        return cls.query.filter_by(id=id).first()

    # delete record
    @classmethod
    def delete_by_id(cls,id):
        record = cls.query.filter_by(id=id)
        if record.first():
            record.delete()
            db.session.commit()
            return True
        else:
            return False

    # check if a username exist
    @classmethod
    def check_username(cls,username):
        record = User.query.filter_by(username=username)
        if record.first():
            return True
        else:
            return False

    # check if an email exist
    @classmethod
    def check_email(cls,email):
        record = User.query.filter_by(email=email)
        if record.first():
            return True
        else:
            return False

    # checking if the password entered and the password in the database match
    @classmethod
    def check_password(cls,username,password):
        record = User.query.filter_by(username=username).first()

        if record and bcrypt.check_password_hash(record.password, password):
            return True
        else:
            return False


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username','email')
        