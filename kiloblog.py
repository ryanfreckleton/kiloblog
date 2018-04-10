import datetime

import attr
import flask
import flask_sqlalchemy
import flask_wtf
import wtforms

from slugify import slugify

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['BLOG_TITLE'] = "A Byte Sized Blog"
app.config['SECRET_KEY'] = b"T\xe6\xe2|8\xe4\x052\xda\x14\xe2',Oa\xeaO\x07\xac\x1b\xbbu\xcas\xd8\x1a\x93\xc0\xc9\xc4zV"
db = flask_sqlalchemy.SQLAlchemy(app)


@attr.s(frozen=True)
class Save:
    post = attr.ib()

    def do(self):
        pm = PostModel(title=self.post.title, content=self.post.content, pub_date=self.post.pub_date)
        db.session.add(pm)
        db.session.commit()


@attr.s(frozen=True)
class RedirectToPost:
    post = attr.ib()

    def do(self):
        return flask.redirect(flask.url_for(
            'view_post',
            year=self.post.pub_date.year,
            month=self.post.pub_date.month,
            day=self.post.pub_date.day,
            slug=self.post.slug
        ))


@attr.s(frozen=True)
class Post:
    title = attr.ib()
    content = attr.ib()
    pub_date = attr.ib()

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
    return flask.render_template('index.html', blog_title=app.config['BLOG_TITLE'])


@app.route('/<year>/<month>/<day>/<slug>')
def view_post(year, month, day, slug):
    return "TBD"


class NewForm(flask_wtf.FlaskForm):
    title = wtforms.StringField()
    content = wtforms.TextAreaField()


@app.route('/new', methods=['GET', 'POST'])
def new():
    form = NewForm()
    if form.validate_on_submit():
        data = form.data.copy()
        del data['csrf_token']
        data['pub_date'] = datetime.date.today()
        for action in make_post(data):
            done = action.do()
            if done:
                return done
    return flask.render_template('new.html', blog_title=app.config['BLOG_TITLE'], form=form)
