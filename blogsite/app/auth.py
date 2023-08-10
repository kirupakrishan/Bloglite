from flask import Blueprint,render_template,redirect,url_for,request,flash
from . import db 
from .models import User
from os import path,mkdir
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth',__name__)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png','jpg','jpeg']

@auth.route("/",methods=["GET","POST"])
@auth.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        try:
            user= User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password,password):
                    login_user(user,remember=True)
                    return redirect(url_for('views.home',uid=user.uid))
                else:
                    flash('Incorrect Password',category='error')
            else:
                    flash('Invalid Email',category='error')
        except:
            flash('No such account',category='error')
    return render_template("auth/signup.html")

@auth.route("/sign-up",methods=["GET","POST"])
def sign_up():
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("email")
        username=request.form.get("username")
        password1=request.form.get("password1")
        password2=request.form.get("password2")
        profile_pic = request.files['img']
        email_exists= User.query.filter_by(email=email).first()
        username_exists= User.query.filter_by(username=username).first()

        if email_exists :
            flash('Email in Use',category='error')
        elif username_exists:
            flash('Username Already Taken')
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        elif not allowed_file(profile_pic.filename):
            flash("File Type Not Allowed", category='error')
        else:
            new_user = User(name=name,email=email, username=username, password=generate_password_hash(password1, method='sha256'),image_file=profile_pic.filename)
            db.session.add(new_user)
            db.session.commit()
            cur_dir = path.abspath(path.dirname(__file__))
            mkdir(cur_dir+path.join(f'/static/img/{new_user.uid}'))
            location = cur_dir+path.join(f'/static/img/{new_user.uid}',profile_pic.filename)
            profile_pic.save(location)
            login_user(new_user, remember=True)
            return redirect(url_for('views.home',uid=new_user.uid))

    return redirect(url_for('views.signup'))
        

@auth.route("/logout")
@login_required
def logout():
    return redirect(url_for('views.login'))
        