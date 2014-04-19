from flask import Flask, request, render_template,Markup,redirect
import json, time, threading, random
import MySQLdb as mdb
import random, datetime,markdown
from flask.ext.sqlalchemy import SQLAlchemy
from models import db,Posts,Authors,app
import config
@app.route('/blog/<author>/create')
def createPost(author):
  return render_template('create.html')
@app.route('/blog/<author>/<link>')
def getpost(author, link):
  article = Posts.query.filter_by(author=author, link=link).first()
  author_data = Authors.query.filter_by(username = author).first()
  post = {
          'title':article.title,
          'date': article.pubDate.strftime('%b %d, %Y'),
          'body': Markup(markdown.markdown(article.post))
        }
  author = {
            'name' : author_data.name,
            'bio' : author_data.bio,
            'pic' : "authors/" + author_data.pic
          }
  return render_template('post.html', title=author_data.title,post=post,author=author)   
@app.route('/blog/<author>/save',methods= ['POST'])
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
    return redirect("/blog/" + author + "/" + link)
  except Exception as e:
    print e
    return "Promlem: " + str(e)
@app.route('/blog/<author>/page/<pagenumber>')
@app.route('/blog/<author>/')
def blogindex(author,pagenumber=1):
  pgnumber  = pagenumber
  pagenumber = int(pagenumber)
  start = (pagenumber-1) *2
  end = pagenumber * 2
  articles = Posts.query.filter_by(author=author).order_by('pubDate desc').all()
  totalpages = len([articles[x:x+2] for x in xrange(0, len(articles), 2)])
  articles = articles[start:end]
  previouspage = (pagenumber-1) if (pagenumber>1) else "pointer-events:none;color:grey"
  nextpage = (pagenumber + 1) if (pagenumber<totalpages) else "pointer-events:none;color:grey"
  posts = []
  relative_path = "../../" if isinstance(pgnumber, unicode) else "../"
  print relative_path
  for article in articles:
    post = {
            'title' : article.title,
            'body' : Markup(markdown.markdown(article.description)),
            'date' : article.pubDate.strftime('%b %d, %Y'),
            'link' : relative_path + author + "/" + article.link
          }
    posts.append(post)
  return render_template('index.html',title='First MiniBlog',description='This is a miniblog in Python, checkout the source at https://github.com/scottydelta/miniblog',posts=posts, page=pagenumber, totalpages=totalpages,author=author,previouspage = previouspage,nextpage=nextpage)
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000,debug=True)
  
