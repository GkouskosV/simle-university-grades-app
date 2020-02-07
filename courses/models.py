from courses import db, login_manager
# Import the UserMixin module to add 
# all of the required methods and attributes to manage the sessions for us
from flask_login import UserMixin

# Return the current user, handled by the Flask extension
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    enrolments = db.relationship('Enrolments', backref='user', lazy=True)
    role_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

class Enrolments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Float, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)

    def __repr__(self):
        return f"Student: {self.student_id}, Professor: {self.professor_id}, Course: {self.course_id}, Grade: {self.grade})"


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    professor = db.relationship('Professor', backref='course', uselist=False)
    enrolments = db.relationship('Enrolments', backref='course', lazy=True)

    def __repr__(self):
        return f"Course('{self.title}', '{self.semester}')"

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    enrolments = db.relationship('Enrolments', backref='professor', lazy=True)

    def __repr__(self):
        return f"Professor('{self.name}')"
