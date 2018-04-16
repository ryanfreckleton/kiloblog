import datetime
import pytest

from slugify import slugify

from hypothesis import assume, given, strategies as st
from hypothesis.stateful import Bundle, RuleBasedStateMachine, precondition, rule

import kiloblog


class KiloblogStateMachine(RuleBasedStateMachine):
    """
    Describe rules for state transition of doing elaborate testing of kiloblog.
    """

    def __init__(self):
        super().__init__()
        self.logged_in = False
        kiloblog.app.testing = True
        kiloblog.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        kiloblog.app.config['WTF_CSRF_ENABLED'] = False
        kiloblog.db.drop_all()
        kiloblog.db.create_all()
        self.client = kiloblog.app.test_client()

    titles = Bundle('titles')
    contents = Bundle('contents')

    @rule(target=titles, title=st.from_regex(r'\A[a-zA-Z0-9]+[ a-zA-Z0-9.,*?!]+\Z'))
    def title(self, title):
        return title

    @rule(target=contents, content=st.text())
    def content(self, content):
        return content

    @precondition(lambda self: self.logged_in)
    @rule(title=titles, content=contents)
    def create_post(self, title, content):
        resp = self.client.post('/new', data=dict(title=title, content=content))
        assert resp.status_code == 302
        assert resp.headers['Location'] == 'http://localhost/{d.year}/{d.month}/{d.day}/{slug}'.format(
                                                    d=datetime.date.today(), slug=slugify(title))

    @rule()
    def login(self):
        self.client.post('/login', data=dict(username='admin', password='password'))
        self.logged_in = True

    @rule()
    def logout(self):
        self.client.get('/logout')
        self.logged_in = False


TestStatefully = KiloblogStateMachine.TestCase


class TestGeneralBsehavior:
    """
    Test general properties of the application.
    """

    @pytest.mark.parametrize("url", ['/', '/login'])
    def test_public_urls(self, url, client):
        """
        Confirm that public urls of front page and login are displayed
        """
        assert client.get(url).status_code == 200

    @pytest.mark.parametrize("url", ['/new', '/logout'])
    def test_protected_urls(self, url, client):
        """
        Confirm that public urls of front page and login are displayed
        """
        assert client.get(url).status_code == 302
        assert client.get(url).headers['Location'] == 'http://localhost/login'

    @given(st.text())
    def test_get(self, client, path):
        """
        When an arbitrary URL is tried with GET, it doesn't return a 500 error.

        Carriage return ('\\n' or '\\r') in the URL will cause Flask to raise a
        500 due to potential security issues.
        """
        assume('\n' not in path)
        assume('\r' not in path)
        assert client.get('/'+path).status_code != 500

    @given(st.text(), st.dictionaries(st.text(), st.text()))
    def test_post(self, client, path, data):
        """
        When an arbitrary URL is tried with POST, it doesn't return a 500 error.
        """
        assert client.post('/'+path, data=data).status_code != 500


class TestAuthentication:
    def test_successful_login(self, client):
        """
        When login is successful, the logout link is displayed to the user.
        """

        assert 'Login' in client.get('/login').data.decode('UTF-8')
        assert 'Logout' in client.post('/login', data=dict(username='admin', password='password'),
                                       follow_redirects=True).data.decode('UTF-8')

    def test_unsuccessful_login(self, client):
        """
        When the login isn't successful, the login page is shown again.
        """
        assert 'Login' in client.get('/login').data.decode('UTF-8')
        result = client.post('/login', data=dict(username='admin', password='wrong_password'),
                             follow_redirects=True).data.decode('UTF-8')
        assert 'Username' in result
        assert 'Bad login' in result

    def test_logout(self, client):
        """
        After logging in and clicking the the logout link, the user is logged out.
        """
        client.post('/login', data=dict(username='admin', password='password'), follow_redirects=True)
        assert 'Logged out' in client.get('/logout', follow_redirects=True).data.decode('UTF-8')


class TestCreatePost:
    def test_new_shows_up_for_logged_in(self, client):
        """
        User logs in
        User goes to /new
        Page with form shows up
        """
        client.post('/login', data=dict(username='admin', password='password'), follow_redirects=True)
        html = client.get('/new').data.decode('UTF-8')
        assert 'form' in html
        assert 'Title' in html
        assert 'Content' in html

    def test_create_post(self, client):
        """
        User logs in
        User creates post
        User is redirected to new post
        Post shows up on index
        """
        client.post('/login', data=dict(username='admin', password='password'), follow_redirects=True)
        resp = client.post('/new', data=dict(title="A Title", content="The Content"), follow_redirects=True)
        assert "A Title" in resp.data.decode('UTF-8')
        assert "The Content" in resp.data.decode('UTF-8')

        resp = client.get('/')
        assert "A Title" in resp.data.decode('UTF-8')
        assert "The Content" in resp.data.decode('UTF-8')

    def test_create_two_posts(self, client):
        """
        Create two posts
        Both posts should show up on the index
        """
        client.post('/login', data=dict(username='admin', password='password'), follow_redirects=True)
        resp = client.post('/new', data=dict(title="A Title", content="The Content"), follow_redirects=True)
        resp = client.post('/new', data=dict(title="B Title", content="The B Content"), follow_redirects=True)

        resp = client.get('/')
        assert "A Title" in resp.data.decode('UTF-8')
        assert "The Content" in resp.data.decode('UTF-8')
        assert "B Title" in resp.data.decode('UTF-8')
        assert "The B Content" in resp.data.decode('UTF-8')


class TestEditPost:
    def test_can_edit_post_when_logged_in(self, client):
        """
        When the user is logged in, the user can edit existing blog posts.
        """
        client.post('/login', data=dict(username='admin', password='password'), follow_redirects=True)
        resp = client.post('/new', data=dict(title="A Title", content="The Content"))
        article_url = resp.headers['Location']
        html = client.get(article_url + '/edit').data.decode('UTF-8')
        assert 'form' in html
        assert 'A Title' in html
        assert 'The Content' in html

    def test_edit_post_updates_content(self, client):
        """
        When a page is edited, it should show the changes on the post page.
        """
        client.post('/login', data=dict(username='admin', password='password'), follow_redirects=True)
        resp = client.post('/new', data=dict(title="A Title", content="The Content"))
        article_url = resp.headers['Location']
        resp = client.post(article_url + '/edit', data=dict(title="B Title", content="The Other Content"),
                           follow_redirects=True)
        assert 'B Title' in resp.data.decode('UTF-8')
        assert 'The Other Content' in resp.data.decode('UTF-8')


def test_user_loader():
    """
    Make sure that the user_loader returns None if the user isn't found.
    """
    assert kiloblog.user_loader('not a real name') is None
