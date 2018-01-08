from flask import Flask, request, redirect, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:ZAl7jeFRnQTKvAVy@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route("/blog", methods=['POST', 'GET'])
def blog():
    blogs = Blog.query.all()
    title = "title"
    body = "body"
    if request.args:
        blog_id = request.args.get('id')
        for blog in blogs:
            if int(blog_id) == blog.id:
                title = blog.title
                body = blog.body
                return render_template('post.html', title=title, body=body)
    else:
        return render_template("blog.html", heading="What a time to be a blog", blogs=blogs)

@app.route("/newpost", methods=['POST', 'GET'])
def newpost():
    title = ""
    body = ""
    if request.method == 'GET':
        return render_template("newpost.html", heading="New Blog Entry")
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if not title and not body:
            flash("Please enter a title for your blog")
            flash("Please enter a body for your blog")
            return render_template("newpost.html", heading="New Blog Entry")
        elif not title:
            flash("Please enter a title for your blog")
            return render_template("newpost.html", heading="New Blog Entry", body=body)
        elif not body:
            flash("Please enter content for your blog")
            return render_template("newpost.html", heading="New Blog Entry", title=title)
        else:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            blogs = Blog.query.all()
            post = blogs[-1]
            post_id = post.id
            return redirect(url_for('blog' , id=post_id))

if __name__ == '__main__':
    app.run()
