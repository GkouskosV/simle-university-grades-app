import os
from flask import render_template, url_for, flash, redirect,request, abort
from courses import app, db, bcrypt
from courses.forms import RegistrationForm, LoginForm
from courses.models import User, Course, Enrolments, Professor
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')   

@app.route("/my_courses")
# Require login to view the specific page
@login_required
def my_courses():
        user = User.query.filter_by(name=current_user.name).first()
        grades = Enrolments.query.filter_by(user=user)
        return render_template('my_courses.html', title='Profile', user=user, grades=grades)

@app.route("/my_course")
@login_required
def my_course():
    user = Professor.query.filter_by(name=current_user.name).first()
    grades = Enrolments.query.filter_by(professor=user)
    return render_template('my_course.html', user=user, grades=grades)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit(): 
        # If the credentials are valid
        # Generate hash password for the user
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        my_role = form.role.data
        # Store in the database the hashed password and not the plain text
        user = User(name=form.name.data, email=form.email.data, password=hashed_pass, role_id=my_role)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Check if the user exists and the password is the same with the one in the database
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Log the user in from the flask extension to handle the session
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if user.role_id == 0:
                return redirect(next_page) if next_page else redirect(url_for('my_courses'))
            else:
                return redirect(next_page) if next_page else redirect(url_for('my_course'))
        else:
            flash('Login Unsuccessful. Check your credentials!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('home'))


