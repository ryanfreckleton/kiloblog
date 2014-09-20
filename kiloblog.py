from flask import Flask, Response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kiloblog.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(1024), unique=True)

PostForm = model_form(Post, Form)

def get_listing():
    return '\n'.join(' - %s' % post.title for post in Post.query.all())

@app.route('/')
def index():
    content = get_listing() + 
    return Response(content, mimetype="text/plain")

if __name__ == '__main__':
    app.run(debug=True)
