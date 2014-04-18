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
class Users(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(30),unique=True)

