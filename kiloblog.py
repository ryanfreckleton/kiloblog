import datetime

import bcrypt
import flask
import flask_login
import flask_sqlalchemy
import flask_wtf
import wtforms
import flask_misaka

from slugify import slugify

app = flask.Flask(__name__)
app.config.from_envvar('KILOBLOG_SETTINGS')
flask_misaka.Misaka(app)
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


@app.route('/<int:year>/<int:month>/<int:day>/<slug>/edit', methods=['GET', 'POST'])
@flask_login.login_required
def edit_post(year, month, day, slug):
    """
    Edit an existing blog post.
    """
    post = Post.query.filter_by(slug=slug, pub_date=datetime.date(year, month, day)).first()
    form = PostForm(title=post.title, content=post.content)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        return flask.redirect(flask.url_for(
            'view_post',
            year=post.pub_date.year,
            month=post.pub_date.month,
            day=post.pub_date.day,
            slug=post.slug
        ))
    return flask.render_template('edit.html', post=post, form=form)


@app.route('/')
def index():
    """
    Display all blog posts on front page.
    """
    return flask.render_template('index.html', posts=Post.query.all())


@app.route('/new', methods=['GET', 'POST'])
@flask_login.login_required
def new_post():
    """
    Display and handle form for creating a new blog post.
    """
    form = PostForm()
    if form.validate_on_submit():
        post = Post(pub_date=datetime.date.today())
        post.slug = slugify(post.title)
        post.title = form.title.data
        post.content = form.content.data
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log user in, flash if bad login and redirect to index page.
    """
    form = LoginForm()
    if form.validate_on_submit():
        if bcrypt.checkpw(form.password.data.encode('UTF-8'), app.config['PASSWORD']):
            flask_login.login_user(user_loader(form.username.data))
        else:
            flask.flash('Bad login')
            return flask.redirect(flask.url_for('login'))
        return flask.redirect(flask.session['next'])
    return flask.render_template('login.html', form=form)


class LoginForm(flask_wtf.FlaskForm):
    """
    Form for creating or editing a blog post.
    """
    username = wtforms.StringField()
    password = wtforms.PasswordField()


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
    if user_id != app.config['ADMIN_USERNAME']:
        return None
    user = User()
    user.id = user_id
    return user
