from flask import Blueprint, render_template, flash, request, redirect, url_for, session, abort
from .model import User, Profileform
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import qrcode, io, base64


auth=Blueprint('auth',__name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        session['email']=email

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password1):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                if current_user.is_admin:
                     profiles = Profileform.query.all()
                     print (profiles)
                     return render_template("admin.html", profiles=profiles)
                return redirect(url_for('views.profileform'))
              
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category= 'error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method =='POST':
        email=request.form.get('email')
        session['email']=email
        fullname=request.form.get('fullname')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        user = User.query.filter_by(email=email).first()

        

 
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash ('Email must be greater than 3 characters.', category='error')
        elif len(fullname) < 2:
            flash ('Full name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash ('Password do not match.', category='error')
        elif len(password1) < 5:
            flash ('Password is too short. It must be greater than 4 characters.', category='error')
        else:
            new_user = User(email=email, fullname=fullname, password=generate_password_hash(password1, method='sha256'))
            if email== 'admin@gmail.com':
                new_user.is_admin = True
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account is created', category='success')
            return redirect(url_for('views.profileform'))
        

    return render_template("signup.html", user=current_user)