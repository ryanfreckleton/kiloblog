from datetime import date

from attr import attrs, attrib
from slugify import slugify

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['BLOG_TITLE'] = "A Byte Sized Blog"
db = SQLAlchemy(app)


@attrs(frozen=True)
class Save:
    post = attrib()

    def do(self):
        pm = PostModel(title=self.post.title, content=self.post.content, pub_date=self.post.pub_date)
        db.session.add(pm)
        db.session.commit()


@attrs(frozen=True)
class RedirectToPost:
    post = attrib()

    def do(self):
        return redirect(
            url_for('view_post',
                    year=self.post.pub_date.year,
                    month=self.post.pub_date.month,
                    day=self.post.pub_date.day,
                    slug=self.post.slug)
        )


@attrs(frozen=True)
class Post:
    title = attrib()
    content = attrib()
    pub_date = attrib()

    @property
    def slug(self):
        return slugify(self.title)


class PostModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    pub_date = db.Column(db.Date(), nullable=False)


def make_post(data):
    post = Post(**data)
    return [Save(post), RedirectToPost(post)]


@app.route('/')
def index():
    return render_template('index.html', blog_title=app.config['BLOG_TITLE'])


@app.route('/<year>/<month>/<day>/<slug>')
def view_post(year, month, day, slug):
    return "TBD"
