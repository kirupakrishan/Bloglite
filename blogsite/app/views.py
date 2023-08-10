from flask import Blueprint,render_template,request
from .models import User,Post
views = Blueprint('views',__name__)


@views.route("/home/<int:uid>",methods=["GET","POST"])
def home(uid):
    user= User.query.filter_by(uid=uid).first()
    return render_template("home/feed.html",user=user)

@views.route("/")
@views.route("/login")
def login():
    return render_template("auth/login.html")

@views.route("/sign-up")
def signup():
    return render_template("auth/signup.html")

@views.route("/profile/<int:uid>")
def profile(uid):
    user= User.query.filter_by(uid=uid).first()
    posts = Post.query.filter_by(user_id=uid).all()
    return render_template("profile/profile.html",user=user,posts=posts)

@views.route("/check-profile/<int:uid>")
def check_profile(uid):
    vid = request.args['vid']
    user= User.query.filter_by(uid=uid).first()
    visitor=User.query.filter_by(uid=vid).first()
    posts=Post.query.filter_by(user_id=vid).all()
    return render_template("explore/check-profile.html",user=user,visitor=visitor,posts=posts)

@views.route("/explore/<int:uid>")
def explore(uid):
    user= User.query.filter_by(uid=uid).first()
    users=User.query.all()
    return render_template("explore/explore.html",user=user,users=users)

@views.route("/create/<int:uid>")
def add_post(uid):
    user= User.query.filter_by(uid=uid).first()
    return render_template("create_post/new_post.html",user=user)
@views.route("/edit/<int:uid>")
def edit(uid):
    user= User.query.filter_by(uid=uid).first()
    return render_template("profile/edit_profile.html",user=user)
