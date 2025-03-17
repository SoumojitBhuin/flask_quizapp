from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
current_utc_time = datetime.utcnow()
from sqlalchemy.sql import text
db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(40), unique=True, nullable=False)
    Password = db.Column(db.String(120), nullable=False)  
    FullName = db.Column(db.String(100), nullable=False)
    Qualification = db.Column(db.String(100), nullable=False)
    DOB = db.Column(db.Date, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)


    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.Password = generate_password_hash(password)  

    def check_password(self, password):
        return check_password_hash(self.Password, password)  


class Subject(db.Model):
    __tablename__ = 'Subject'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(200), nullable=False)
    chaps = db.relationship('Chapter', backref='Subject', foreign_keys="[Chapter.sub_id]")
    quizzes_in_sub = db.relationship('Quiz', backref='Subject', foreign_keys="[Quiz.sub_id]")
    question = db.relationship('Question', backref='Subject', foreign_keys="[Question.sub_id]")
    score=db.relationship('Score', backref='Subject',foreign_keys="[Score.sub_id]")

class Chapter(db.Model):
    __tablename__ = 'Chapter'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(200), nullable=False)
    
    sub_id=db.Column(db.Integer, db.ForeignKey('Subject.id'))
    
    Quizzes = db.relationship('Quiz', backref='Chapter', foreign_keys="[Quiz.chap_id]")
    question=db.relationship('Question', backref='Chapter', foreign_keys="[Question.chap_id]")
    score=db.relationship('Score', backref='Chapter',foreign_keys="[Score.chap_id]")


class Quiz(db.Model):
    __tablename__ = 'Quiz'
    id = db.Column(db.Integer, primary_key=True)
    quiz_no = db.Column(db.String(100), nullable=False)
    date_of_quiz = db.Column(db.Date, nullable=False)
    time_duration = db.Column(db.Integer, nullable=False)
    sub_id=db.Column(db.Integer, db.ForeignKey('Subject.id'))
    chap_id=db.Column(db.Integer, db.ForeignKey('Chapter.id'))
    
    Questions = db.relationship('Question', backref='Quiz', foreign_keys="[Question.quiz_id]")
    score=db.relationship('Score', backref='Quiz',foreign_keys="[Score.quiz_id]")

    

class Question(db.Model):
    __tablename__ = 'Question'
    id = db.Column(db.Integer, primary_key=True)
    
    Question_Statement = db.Column(db.String(200), nullable=False)
    Option1 = db.Column(db.String(100), nullable=False)
    Option2 = db.Column(db.String(100), nullable=False)
    Option3 = db.Column(db.String(100), nullable=False)
    Option4 = db.Column(db.String(100), nullable=False)
    correct_option = db.Column(db.String(100), nullable=False, default=1)
    
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'))
    chap_id=db.Column(db.Integer, db.ForeignKey('Chapter.id'))
    sub_id=db.Column(db.Integer, db.ForeignKey('Subject.id'))
    
    
    


class Score(db.Model):
    __tablename__ = 'Score'
    id = db.Column(db.Integer, primary_key=True)
    Total_Scored = db.Column(db.Integer, nullable=False)


    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'), nullable=False)
    chap_id=db.Column(db.Integer, db.ForeignKey('Chapter.id'))
    sub_id=db.Column(db.Integer, db.ForeignKey('Subject.id'))

    Time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    quiz = db.relationship('Quiz', backref='scores', lazy=True)