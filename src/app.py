from flask import Flask, request, render_template,Markup
import json, time, threading, random
import MySQLdb as mdb
import random, datetime,markdown
from flask.ext.sqlalchemy import SQLAlchemy
from models import db,Posts,app
import config
blog="/post/"
@app.route('/create')
def createPost():
  return render_template('create.html')
@app.route('/<author>/save',methods= ['POST'])
def savePost(author):
  postid = random.randint(100000000000,999999999999)
  title = str(request.form['title'])
  link = title.split(" ")
  link = "-".join(link[0:6])
  content = str(request.form['content'])
  timestamp = datetime.datetime.now()
  try:
    add = Posts(id=postid,title=title,link=link,post=content,pubDate=timestamp,author=author)
    db.session.add(add)
    db.session.commit()  
    return redirect blog+link
  except Exception as e:
    print e
    return "Promlem: " + str(e)
@app.route('/blog/<author>')
def index():
  posts = models.Posts.query.filter_by(author=author).order_by('pubDate desc').all()
  text = Markup(markdown.markdown("`Bold is a good buy`"))
  return render_template('index.html',title='First MiniBlog',description='This is a miniblog in Python, checkout the source at https://github.com/scottydelta/miniblog',posts=posts)
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000)
  
