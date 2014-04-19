from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import config,datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  config.DB_URI
db = SQLAlchemy(app)
class Posts(db.Model):
  __tablename__ = 'posts'
  id = db.Column(db.Integer, primary_key=True)
  author = db.Column(db.String(30))
  pubDate = db.Column(db.DateTime)
  description = db.Column(db.String(300))
  post = db.Column(db.Text)
  title = db.Column(db.String(200))
  link = db.Column(db.String(200),unique=True)
  def __init__(self,id,author,pubDate,desp,post,title,link):
    self.id = id
    self.author = author
    self.pubDate = pubDate
    self.post = post
    self.title = title
    self.link = link
    self.description = desp
class Authors(db.Model):
  __tablename__ = 'authors'
  username = db.Column(db.String(30),primary_key=True)
  name = db.Column(db.String(40))
  bio = db.Column(db.String(300))
  title = db.Column(db.String(20))
  fb = db.Column(db.String(30))
  github = db.Column(db.String(30))
  twitter = db.Column(db.String(30))
  pic = db.Column(db.String(100))
  def __init__(self,username,name,bio,title,fb,github,twitter,pic):
    self.username = username
    self.name= name
    self.bio = bio
    self.title = title
    self.fb = fb
    self.github = github
    self.twitter = twitter
    self.pic = pic

