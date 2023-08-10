from flask import Blueprint,render_template,redirect,url_for,request,flash
from . import db 
from .models import User,Post,Comment
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from os import path,mkdir

ctrl = Blueprint('controllers',__name__)
auth = Blueprint('auth',__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png','jpg','jpeg']

@ctrl.route("/create/<int:uid>",methods=["GET","POST"])
def add_post(uid):
    if request.method=="POST":
        post=request.files["img"]
        caption=request.form.get("caption")
        if not allowed_file(post.filename):
            flash("File Type Not Allowed", category='error')
        else: 
            new_post = Post(content=caption,media=post.filename,user_id=uid)
            db.session.add(new_post)
            db.session.commit()
            cur_dir = path.abspath(path.dirname(__file__))
            location = cur_dir+path.join(f'/static/img/{uid}',new_post.media)
            post.save(location)
            return redirect(url_for('views.home',uid=uid))
    return redirect(f"/create/{uid}")


@ctrl.route("/edit/<int:uid>",methods=["GET","POST"])
def edit_post(uid):
    if request.method=="POST":
        name=request.form.get("name")
        username=request.form.get("username")
        caption=request.form.get('caption')
        profile_pic = request.files['img']

        if len(username) < 2:
            flash('Username is too short.', category='error')
        elif not allowed_file(profile_pic.filename) and profile_pic.filename !='':
            flash("File Type Not Allowed", category='error')
        else:
            user = User.query.filter_by(uid=uid).first()
            user.name=name
            user.caption=caption
            user.username=username
            if profile_pic.filename!='':
                user.image_file=profile_pic.filename
                cur_dir = path.abspath(path.dirname(__file__))
                location = cur_dir+path.join(f'/static/img/{uid}',profile_pic.filename)
                profile_pic.save(location)            
            db.session.commit()
            return redirect(url_for('views.profile',uid=uid))
    return redirect(f"/edit/{uid}")
    
@ctrl.route("/view_post/<int:uid>")
def view_post(uid):
    pid = request.args['pid']
    user= User.query.filter_by(uid=uid).first()
    post=Post.query.filter_by(pid=pid).first()
    return render_template("explore/view_post.html",user=user,post=post)

@ctrl.route("/follow")
def follows():
    fid = request.args['fid']
    uid = request.args['uid']
    user= User.query.filter_by(uid=uid).first()
    follower= User.query.filter_by(uid=fid).first()
    user.follow(follower)
    db.session.commit()
    return redirect(request.referrer)


@ctrl.route("/unfollow")
def unfollows():
    fid = request.args['fid']
    uid = request.args['uid']
    user= User.query.filter_by(uid=uid).first()
    follower= User.query.filter_by(uid=fid).first()
    user.unfollow(follower)
    db.session.commit()
    return redirect(request.referrer)

@ctrl.route("/like")
def like():
    pid = request.args['pid']
    uid = request.args['uid']
    user= User.query.filter_by(uid=uid).first()
    post= Post.query.filter_by(pid=pid).first()
    post.like_post(user)
    db.session.commit()
    return redirect(request.referrer)

@ctrl.route("/unlike")
def unlike():
    pid = request.args['pid']
    uid = request.args['uid']
    user= User.query.filter_by(uid=uid).first()
    post= Post.query.filter_by(pid=pid).first()
    post.unlike_post(user)
    db.session.commit()
    return redirect(request.referrer)


@ctrl.route("/comment",methods=["POST"])
def comment():
    if request.method=="POST":
        pid = request.args['pid']
        uid = request.args['uid']
        comment = request.form.get('comment')
        c = Comment(content=comment, user_id=uid, post_id=pid)
        db.session.add(c)
        db.session.commit()
        return redirect(request.referrer)

@ctrl.route("/delete-post")
def delete_post():
    pid = request.args['pid']
    uid = request.args['uid']
    Post.query.filter_by(pid=pid).delete()
    db.session.commit()
    flash("Post Deleted", category='success')
    return redirect(url_for('views.profile',uid=uid))

@ctrl.route("/delete-account")
def delete_account():
    uid = request.args['uid']
    User.query.filter_by(uid=uid).delete()
    db.session.commit()
    logout_user()
    flash("Account Deleted", category='success')
    return redirect(url_for('views.login'))
