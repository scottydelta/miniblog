from flask import Flask, request, render_template,Markup,redirect
import json, time, threading, random
import MySQLdb as mdb
import random, datetime,markdown
from flask.ext.sqlalchemy import SQLAlchemy
from models import db,Posts,Authors,Users,app
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
import config
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(id):
  return Users.query.get(int(id))

@app.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')
  print request.args
  username = request.form['username']
  password = request.form['password']
  print username, password
  registered_user = Users.query.filter_by(username=username,password=password).first()
  if not registered_user:
   # flash('Username or Password is invalid' , 'error')
    return "Not logged In"
  login_user(registered_user)
  #flask('Logged in successfully')
  if request.args.get('next'):
    return redirect(request.args.get('next'))
  return "Logged in"
@app.route('/logout', methods=['GET'])
def logout():
  logout_user()
  return "logged out"



@app.route('/blog/<author>/create', methods=['GET','POST'])
@login_required
def createPost(author):
  if request.method=='GET':
    if current_user.username==author:
      return render_template('create.html')
    return "Are you not " + current_user.username+", Login with different user?"
  else:
    if current_user.username==author:
      postid = random.randint(100000000000,999999999999)
      title = request.form['title']
      desp = request.form['description']
      body = request.form['body']
      link = title.split(" ")
      link = "-".join(link[0:6])
      timestamp = datetime.datetime.now()
      add = Posts(id=postid,title=title,link=link,post=body,pubDate=timestamp,author=author,desp=desp)
      db.session.add(add)
      db.session.commit()  
      return redirect('/blog/' + author + '/' + link)
    return "Are you not " + current_user.username+", Login with different user?"
@app.route('/blog/<author>/<link>')
def getpost(author, link):
  article = Posts.query.filter_by(author=author, link=link).first()
  if article:
    author_data = Authors.query.filter_by(username = author).first()
    print markdown.markdown(article.post,['fenced_code'])
    post = {
            'title':article.title,
            'date': article.pubDate.strftime('%b %d, %Y'),
            'body': Markup(markdown.markdown(article.post,['fenced_code']))
          }
    author = {
              'name' : author_data.name,
              'bio' : author_data.bio,
              'pic' : "authors/" + author_data.pic
            }
    return render_template('post.html', title=author_data.title,post=post,author=author)
  return "hakuna matata"   
@app.route('/blog/<author>/page/<pagenumber>')
@app.route('/blog/<author>/')
def blogindex(author,pagenumber=1):
  relative_path = "../../" if isinstance(pagenumber, unicode) else "../"
  pagenumber = int(pagenumber)
  start = (pagenumber-1) *2
  end = pagenumber * 2
  articles = Posts.query.filter_by(author=author).order_by('pubDate desc').all()
  totalpages = len([articles[x:x+2] for x in xrange(0, len(articles), 2)])
  articles = articles[start:end]
  previouspage = (pagenumber-1) if (pagenumber>1) else "pointer-events:none;color:grey"
  nextpage = (pagenumber + 1) if (pagenumber<totalpages) else "pointer-events:none;color:grey"
  posts = []
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
  app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
  app.run(host="0.0.0.0", port=8000,debug=True)
  
