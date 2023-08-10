from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
import timeago 

# Followers Table
followers = db.Table('followers',
    db.Column('user_id', db.Integer, db.ForeignKey('users.uid')),
    db.Column('follows_id', db.Integer, db.ForeignKey('users.uid'))
)


# Likes Table datetime.utc
likes = db.Table('likes',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.pid')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.uid'))
)


class User(db.Model,UserMixin):
    __tablename__ = 'users'

    uid=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email=db.Column(db.String(150),unique=True)
    username=db.Column(db.String(150),unique=True)
    name=db.Column(db.String(150))
    caption=db.Column(db.String(150),default="Caption")
    password=db.Column(db.String(150))
    date_created=db.Column(db.DateTime(timezone=True),default=func.now())
    image_file = db.Column(db.String(50),nullable=False,default='default.jpg')

    posts = db.relationship('Post',backref ='user',lazy = 'dynamic')
    comments = db.relationship('Comment',backref ='user',lazy = 'dynamic')

    follows = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.user_id == uid),
        secondaryjoin=(followers.c.follows_id == uid),backref='follower')


    def post_count(self,user):
        l = user.posts.count() 
        return l

    def get_id(self):
        return self.uid

    def is_following(self, user):
        return user in self.follows

    def follow(self, user):
        if self.uid != user.uid:
            if not self.is_following(user):
                self.follows.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.follows.remove(user)

    def get_following_count(self, user):
        return len(self.follows)

    def get_followed_posts(self):
        fw_users = [user.uid for user in self.follows]
        fw_users.append(self.uid)       # to include my own posts
        fw_posts = Post.query.order_by(Post.date_posted.desc()).filter(Post.user_id.in_(fw_users))
        return fw_posts 

class Post(db.Model):
    __tablename__ = 'posts'
    pid = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=True)
    media = db.Column(db.String(32), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)

    liked = db.relationship("User", secondary=likes)
    comments = db.relationship('Comment', backref='post', lazy=True)

    def get_likes_count(self):
        return len(self.liked)


    def user_liked(self, user):
        return user in self.liked


    def like_post(self, user):
        self.liked.append(user)

    def unlike_post(self, user):
        self.liked.remove(user)


    def comments_count(self):
        return len(self.comments)


    def get_comments(self, limit=0):
        if limit > 0:
            return self.comments[-limit:] 


    def get_timeago(self):
        now = func.now()
        return timeago.format(self.date_posted, now)

class Comment(db.Model):
    __tablename__ = 'comments'
    cid = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.pid'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=func.now())
