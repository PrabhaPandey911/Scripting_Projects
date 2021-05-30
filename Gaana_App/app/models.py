from datetime import datetime
from app import db

class User(db.Model):
    uid = db.Column(db.Integer, db.Sequence('uid',start=1,increment=1), primary_key=True)
    uname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.Numeric(10), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # favourite = db.relationship('Favourite')
    # follower = db.relationship('Follower')

class Follower(db.Model):
    uid = db.Column(db.String(50), db.ForeignKey('user.uid'), primary_key=True) 
    follower_id = db.Column(db.String(50), db.ForeignKey('user.uid'), primary_key=True)

class Category(db.Model):
    cat_id = db.Column(db.Integer,db.Sequence('sid',start=1,increment=1), primary_key=True)
    cat_name = db.Column(db.String(50), nullable=False)
    cat_thumbnail=db.Column(db.String(1000),default="https://t3.ftcdn.net/jpg/01/41/65/48/500_F_141654838_zclm59IeX5ws6E7UCqHzkfP4YDVea1QP.jpg")

class Subcategory(db.Model):
    scat_id = db.Column(db.Integer,db.Sequence('sid',start=1,increment=1), primary_key=True)
    scat_name = db.Column(db.String(50), nullable=False)
    cat_subcat = db.relationship('Cat_subcat')
    songs = db.relationship('Songs')


class Cat_subcat(db.Model):
    cat_id = db.Column(db.Integer, db.ForeignKey('category.cat_id') , primary_key=True)
    scat_id = db.Column(db.Integer, db.ForeignKey('subcategory.scat_id') , primary_key=True)

class Songs(db.Model):
    sid = db.Column(db.Integer, db.Sequence('sid',start=1,increment=1), primary_key=True)
    sname = db.Column(db.String(50), nullable=False)
    category=db.Column(db.Integer,db.ForeignKey('category.cat_id'),nullable=False)
    genre = db.Column(db.Integer,db.ForeignKey('subcategory.scat_id') , nullable=False)
    artist = db.Column(db.String(50), nullable=True)
    album = db.Column(db.String(60), nullable=True)
    year = db.Column(db.Numeric(4),nullable=False)
    path = db.Column(db.String(1000), nullable=False)
    count = db.Column(db.Integer,default=0)
    thumbnail = db.Column(db.String(1000),default="https://image.freepik.com/free-vector/circle-made-of-music-instruments_23-2147509304.jpg")
    duration = db.Column(db.Numeric, nullable=False,default=0)

    # favourite = db.relationship('Favourite')
    # playlist_song = db.relationship('Playlist_song')

class Uploaded_songs(db.Model):
    uid = db.Column(db.String(50), db.ForeignKey('user.uid'), nullable=False) 
    sid = db.Column(db.Integer, db.ForeignKey('songs.sid'), primary_key=True)
    sname = db.Column(db.String(50),  db.ForeignKey('songs.sname'),nullable=False)
    path = db.Column(db.String(1000), nullable=False)
    isPublic = db.Column(db.Boolean, default=True)

class Playlist(db.Model):
    pid = db.Column(db.Integer, db.Sequence('sid',start=1,increment=1), primary_key=True)
    pname = db.Column(db.String(50), nullable=False)
    uid = db.Column(db.String(50), db.ForeignKey('user.uid')) 
    # playlist_song = db.relationship('Playlist_song')

class Playlist_song(db.Model):
    pid = db.Column(db.Integer, db.ForeignKey('playlist.pid'), primary_key=True)
    sid = db.Column(db.Integer, db.ForeignKey('songs.sid'), primary_key=True)

class Favourite(db.Model):
    uid = db.Column(db.Integer, db.ForeignKey('user.uid') ,primary_key=True)
    sid = db.Column(db.Integer, db.ForeignKey('songs.sid'), primary_key=True)


db.create_all()


