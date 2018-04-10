import datetime

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


class Post(db.Model):
    """
    Args:
        title (str): Title of the blog post for display at the top of the page.
        slug (str): Unchanging url slug based on title.
        content (str): Blog post content (eventually this will be in markdown).
        pub_date (datetime.date): Date that this blog was initially published.

    Returns:
        New post model object.
    """
    title = db.Column(db.String(80), primary_key=True)
    slug = db.Column(db.String(80), primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    pub_date = db.Column(db.Date(), nullable=False)


@app.route('/<int:year>/<int:month>/<int:day>/<slug>')
def view_post(year, month, day, slug):
    """
    Display a single blog post based on day and slug.
    """
    post = Post.query.filter_by(slug=slug, pub_date=datetime.date(year, month, day)).first()
    return flask.render_template('post.html', post=post)


@app.route('/')
def index():
    """
    Display all blog posts on front page.
    """
    return flask.render_template('index.html', posts=Post.query.all())


@app.route('/new', methods=['GET', 'POST'])
@flask_login.login_required
def new():
    """
    Display and handle form for creating a new blog post.
    """
    form = PostForm()
    if form.validate_on_submit():
        data = form.data.copy()
        del data['csrf_token']
        data['pub_date'] = datetime.date.today()
        post = Post(**data)
        post.slug = slugify(post.title)
        db.session.add(post)
        db.session.commit()
        return flask.redirect(flask.url_for(
            'view_post',
            year=post.pub_date.year,
            month=post.pub_date.month,
            day=post.pub_date.day,
            slug=post.slug
        ))
    return flask.render_template('new.html', form=form)


class PostForm(flask_wtf.FlaskForm):
    """
    Form for creating or editing a blog post.
    """
    title = wtforms.StringField()
    content = wtforms.TextAreaField()


@app.context_processor
def context_processor():
    """
    Make global configuration and variables available to all templates.
    """
    return dict(blog_title=app.config['BLOG_TITLE'])


class User(flask_login.UserMixin):
    """
    Simplistic user class, since we only have the administrator.
    """
    pass


@login_manager.user_loader
def user_loader(user_id):
    """
    Only handle one user_id, that of the administrator.
    """
    if user_id != 'admin':
        return None
    user = User()
    user.id = user_id
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log user in, flash if bad login and redirect to index page.
    """
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    user_id = flask.request.form['user_id']
    if flask.request.form['password'] == app.config['PASSWORD']:
        user = User()
        user.id = user_id
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('index'))

    flask.flash('Bad login')
    return flask.redirect('login')


@app.route('/logout')
@flask_login.login_required
def logout():
    """
    Log out user when they request /logout with a GET.

    Flash status that the user has logged out.
    """
    flask_login.logout_user()
    flask.flash('Logged out')
    return flask.redirect(flask.url_for('index'))
