import datetime

import pytest

import kiloblog


def setup_module():
    kiloblog.app.testing = True
    kiloblog.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    kiloblog.db.create_all()


@pytest.fixture
def client():
    return kiloblog.app.test_client()


class TestIndex:
    def test_get(self, client):
        assert client.get('/').status == '200 OK'


class TestCreatePost:
    post = kiloblog.Post(title='new blog title', content='content goes here', pub_date=datetime.date(2000, 1, 1))

    def test_new_post(self):

        actions = kiloblog.make_post({'title': 'new blog title', 'content': 'content goes here',
                                      'pub_date': datetime.date(2000, 1, 1)})
        assert actions == [kiloblog.Save(self.post), kiloblog.RedirectToPost(self.post)]

    def test_save(self):
        post = kiloblog.Post(title="new blog title", content="content goes here", pub_date=datetime.date(2000, 1, 1))
        save = kiloblog.Save(post)
        save.do()
        post_from_db = kiloblog.PostModel.query.get(1)
        assert kiloblog.PostModel.query.count() == 1
        assert post_from_db.title == post.title
        assert post_from_db.content == post.content
        assert post_from_db.pub_date == datetime.date(2000, 1, 1)

    def test_redirect_to_post(self):
        with kiloblog.app.test_request_context():
            redirect = kiloblog.RedirectToPost(self.post).do()
            assert redirect.headers['Location'] == '/2000/1/1/new-blog-title'
