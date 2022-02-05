
from tabnanny import check
from flask import Blueprint, redirect, render_template, request, flash, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # query the user table in the database for the submitted email
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)   
                return redirect(url_for('views.home'))
            else:
                flash('inccorrect passwrd, try again', category='error')
        else:
            flash('email does not exist', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required   #can not access this route unless the user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')

        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 2 characters', category='error')
        elif password1 != password2:
            flash('Password confrimation must match the original password',
                  category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters', category='error')
        else:
            # add user to the database
            new_user = User(email=email, first_name=first_name,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account was successfully created', category='success')
            # or just ('/') incase the route name changes
            return redirect(url_for('views.home'))

    return render_template('sign-up.html', user=current_user)
