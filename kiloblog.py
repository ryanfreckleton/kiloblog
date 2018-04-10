import datetime

import attr
import flask
import flask_sqlalchemy
import flask_wtf
import wtforms

from slugify import slugify

app = flask.Flask(__name__)
app.config.from_envvar('KILOBLOG_SETTINGS')
db = flask_sqlalchemy.SQLAlchemy(app)


@attr.s(frozen=True)
class Save:
    post = attr.ib()

    def do(self):
        pm = PostModel(title=self.post.title, content=self.post.content, pub_date=self.post.pub_date, slug=self.post.slug)
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

    @classmethod
    def from_model(cls, model):
        return cls(title=model.title, content=model.content, pub_date=model.pub_date)


class PostModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    pub_date = db.Column(db.Date(), nullable=False)
    slug = db.Column(db.String(80), nullable=False)


def make_post(data):
    post = Post(**data)
    return [Save(post), RedirectToPost(post)]


@app.route('/')
def index():
    return flask.render_template('index.html', blog_title=app.config['BLOG_TITLE'])


@app.route('/<int:year>/<int:month>/<int:day>/<slug>')
def view_post(year, month, day, slug):
    model = PostModel.query.filter_by(slug=slug, pub_date=datetime.date(year, month, day)).first()
    return flask.render_template('post.html', post=Post.from_model(model))


class PostForm(flask_wtf.FlaskForm):
    title = wtforms.StringField()
    content = wtforms.TextAreaField()


@app.route('/new', methods=['GET', 'POST'])
def new():
    form = PostForm()
    if form.validate_on_submit():
        data = form.data.copy()
        del data['csrf_token']
        data['pub_date'] = datetime.date.today()
        for action in make_post(data):
            done = action.do()
            if done:
                return done
    return flask.render_template('new.html', blog_title=app.config['BLOG_TITLE'], form=form)
