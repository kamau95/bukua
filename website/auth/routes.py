from flask import Blueprint, render_template, flash, request, redirect, url_for
from website.models import User
from ..import db 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password', category='danger')
        else:
            flash('email doesnot exist', category='danger')

    return render_template('login.html')


@auth.route('/logout')
@login_required #makes sure you can access this route when you are only logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('email already exists', category='danger')
        elif len(email) < 4:
            flash('email must be greater than 3 characters', category='danger')
        elif len(first_name) < 3:
            flash('first name should be more than two characters', category='danger')
        elif password1 != password2:
            flash('password not matching', category='danger')
        elif len(password1) < 7:
            flash('password should be more than six characters', category='danger')
        else:
            try:
                #hash password
                new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                    password1, method='pbkdf2:sha256'))
                ## Create new user object
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created', category='success')
                return redirect(url_for('views.home'))
            except IntegrityError:
                flash('Email exists, use new one', category='danger')


    return render_template('sign_up.html')
