import datetime

import attr
import flask
import flask_login
import flask_sqlalchemy
import flask_wtf
import wtforms

from slugify import slugify

app = flask.Flask(__name__)
app.config.from_envvar('KILOBLOG_SETTINGS')
db = flask_sqlalchemy.SQLAlchemy(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = ['admin']


@app.context_processor
def context_processor():
    return dict(blog_title=app.config['BLOG_TITLE'])


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(user_id):
    if user_id not in users:
        return None
    user = User()
    user.id = user_id
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    email = flask.request.form['email']
    if flask.request.form['password'] == app.config['PASSWORD']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('index'))

    return 'Bad login'


@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return 'Logged out'


@attr.s(frozen=True)
class Save:
    post = attr.ib()

    def do(self):
        self.post.slug = slugify(self.post.title)
        db.session.add(self.post)
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


class Post(db.Model):
    title = db.Column(db.String(80), primary_key=True)
    slug = db.Column(db.String(80), primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    pub_date = db.Column(db.Date(), nullable=False)


def make_post(data):
    post = Post(**data)
    return [Save(post), RedirectToPost(post)]


@app.route('/')
def index():
    return flask.render_template('index.html', posts=Post.query.all())


@app.route('/<int:year>/<int:month>/<int:day>/<slug>')
def view_post(year, month, day, slug):
    post = Post.query.filter_by(slug=slug, pub_date=datetime.date(year, month, day)).first()
    return flask.render_template('post.html', post=post)


class PostForm(flask_wtf.FlaskForm):
    title = wtforms.StringField()
    content = wtforms.TextAreaField()


@app.route('/new', methods=['GET', 'POST'])
@flask_login.login_required
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
    return flask.render_template('new.html', form=form)
