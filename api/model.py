from exam_portal_end_to_end.api.config import db


class Questions(db.Model):
    id = db.Column('ques_id', db.Integer(), primary_key=True)
    question = db.Column('question', db.String(255))
    option1 = db.Column('opt1', db.String(255))
    option2 = db.Column('opt2', db.String(255))
    option3 = db.Column('opt3', db.String(255))
    option4 = db.Column('opt4', db.String(255))
    answer = db.Column('ans', db.String(255))
    clientid = db.Column("client_id", db.ForeignKey("client.client_id"), unique=False, nullable=True)
    active = db.Column('active', db.String(10), default='Y')



class Client(db.Model):
    id = db.Column('client_id', db.Integer(), primary_key=True)
    fullname = db.Column('cname', db.String(60))
    email = db.Column('cemail', db.String(255))
    username = db.Column('username', db.String(30),unique=True)
    password = db.Column('password', db.String(255))
    token = db.Column('token', db.String(255), nullable=True)
    active = db.Column('active', db.String(10), default='Y')
    studref = db.relationship('Student', uselist=True, lazy=True, backref="clref")
    questions = db.relationship('Questions', uselist=True, lazy=True, backref="clref")

    @staticmethod
    def get_dummy():
        return Client(id=0, fullname='', email='', username='', password='')



class Student(db.Model):
    id = db.Column('stud_id', db.Integer(), primary_key=True)
    fullname = db.Column('stud_name', db.String(60))
    email = db.Column('stud_email', db.String(255))
    username = db.Column('username', db.String(30),unique=True)
    password = db.Column('password', db.String(255))
    active = db.Column('active', db.String(10), default='Y')
    clientid = db.Column('cl_id', db.ForeignKey("client.client_id"), unique=False, nullable=True)


    @staticmethod
    def get_dummy():
        return Student(id=0, fullname='',email='',username='',password='')


if __name__ == '__main__':
    db.create_all()
