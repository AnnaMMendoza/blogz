from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:b@b272AzB@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'itsasecret'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET']) # direct to the newpost page
def blogs(): 
    return redirect('/newpost')


@app.route('/newpost', methods=['POST', 'GET'])
def index(): # adds the post to the database and displays below the entry form

    new_post = None
    title = ""
    body = ""
    title_error = ""
    post_error = ""

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if title == "":
            title_error = "Please enter a title for your post"
        if len(title) > 120:
            title_error = "Blog title is limited to 120 characters"
        if body == "":
            post_error = "Please enter your blog post here"
        if len(body) > 500:
            post_error = "Blog post is limited to 500 characters"
        if title_error != "" and post_error != "":
            return render_template('newpost.html', title_error=title_error, post_error=post_error)
        
        if not title_error and not post_error:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
        
    return render_template('newpost.html', new_post=new_post, title_error=title_error, post_error=post_error)
   
# display all blog posts on a new main page
# @app.route('/blog', methods=['POST'])
# def blogposts():

#     new_post = request.form['new_post']
#     new_post = Blog.query.filter_by(title=title, body=body).all()

#     return render_template('blog.html', title="Just Say It!")


if __name__=='__main__':
    app.run()