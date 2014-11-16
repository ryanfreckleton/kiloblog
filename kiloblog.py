from flask import (Flask, Response, render_template, request, redirect,
                   url_for, abort)
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.widgets import TextArea

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config.from_object('default_settings')
db = SQLAlchemy(app)

chapters = db.Table('chapters',
           db.Column('prequel_id', db.Integer, db.ForeignKey('post.id')),
           db.Column('sequel_id', db.Integer, db.ForeignKey('post.id')))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.String(1024), unique=True)
    sequels = db.relationship('Post', 
                              secondary=chapters,
                              primaryjoin=id==chapters.c.prequel_id,
                              secondaryjoin=id==chapters.c.sequel_id,
                              backref=db.backref('prequels'))

PostForm = model_form(Post, base_class=Form,
                      field_args={'content':{'widget':TextArea()}},
                      only=['title', 'content'])

@app.route('/', methods=('GET', 'POST'))
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post()
        form.populate_obj(post)
        db.session.add(post)
        db.session.commit()
    return render_template("index.html", listing=Post.query.all(), form=form)

@app.route('/<int:post_id>')
def show(post_id):
    post = Post.query.get(post_id)
    return render_template("post.html", post_id=post_id, post=post)

@app.route('/<int:post_id>/edit', methods=('GET', 'POST'))
def edit(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    form = PostForm(request.form, post)
    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('show', post_id=post_id))
    return render_template('edit.html', post_id=post_id, form=form)
