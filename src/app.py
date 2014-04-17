from flask import Flask, request, render_template,Markup
import json, time, threading, random
import MySQLdb as mdb
import random, datetime,markdown
from flask.ext.sqlalchemy import SQLAlchemy
from models import db,Posts,app
import config
#app = Flask(__name__, static_folder='static', static_url_path='')
#db.init_app(app)
#SQLALCHEMY_DATABASE_URI =  "mysql://root:wjlbti@localhost/miniblog?charset=utf8&use_unicode=0"
a = Posts(798798,'bajaj',datetime.datetime.now(),'sfsfsdf','sdfsdf','sdfsdf')
db.session.add(a)
db.session.commit()
cnx = mdb.connect('localhost', 'root', 'wjlbti','miniblog')
cur = cnx.cursor()
@app.route('/create')
def createPost():
  return render_template('create.html')
@app.route('/<author>/save',methods= ['POST'])
def savePost(author):
  postid = random.randint(100000000000,999999999999)
  title = str(request.form['title'])
  link = title.split(" ")
  link = "-".join(link)
  content = str(request.form['content'])
  timestamp = datetime.datetime.now()
  try:
    cur.execute(
       """insert into bloglist(id,link, title,content,timestamp,author)
       VALUES (%s, %s, %s, %s, %s,%s);""",
       (postid,link,title,content,timestamp,author))
    cnx.commit()
    return "Transaction Stored"
  except Exception as e:
    print e
    return "Promlem: " + str(e)
@app.route('/')
def index():
  text = Markup(markdown.markdown("`Bold is a good buy`"))
  posts = [
    {
      'title' : 'Cats are assholes',
      'body' : 'It is widely known fact. Some cats are grumpy aswell' + text,
      'date' : '15 Nov 2013',
      'link' : 'check/fsfsdf'
    },
    {
      'title' : 'Dogs are good',
      'body' : 'Dogs are most friendly creatures',
      'date' : '16 Nov 2013',
      'link' : 'check/fsdfsdfsfsdf'
    },
    {
      'title' : 'Song from Frozen is awesome',
      'body' : 'Do you want to build a snowman, we could go out and play!!',
      'date' : '17 Nov 2013',
      'link' : 'chefsdfck/fsfsdf'
    },
    {
      'title' : 'Song from Frozen is awesome',
      'body' : 'Do you want to build a snowman, we could go out and play!!',
      'date' : '17 Nov 2013',
      'link' : 'chefsdfck/fsfsdf'
    }
  ]
  return render_template('index.html',title='First MiniBlog',description='This is a miniblog in Python, checkout the source at https://github.com/scottydelta/miniblog',posts=posts)
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000)
  
