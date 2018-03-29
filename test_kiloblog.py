import kiloblog


class TestDatabase(object):
    def setup_class(cls):
        kiloblog.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        kiloblog.db.create_all()
        cls.post1 = kiloblog.Post(title="Post 1", content="Content 1")
        kiloblog.db.session.add(cls.post1)
        kiloblog.db.session.commit()

    def test_post1_exists(self):
        assert kiloblog.Post.query.get(1) is not None

    def test_sequels(self):
        new_post = kiloblog.Post(title='Post 2', content='Content 2')
        self.post1.sequels.append(new_post)
        kiloblog.db.session.add(new_post)
        kiloblog.db.session.commit()
        assert self.post1.sequels == [new_post]

    def teardown_class(cls):
        kiloblog.db.drop_all()
