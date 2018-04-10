from hypothesis import given, strategies as st


class TestGeneralBehavior:
    """
    Test general properties of the application.
    """
    @given(st.text())
    def test_get(self, client, text):
        """
        When an arbitrary URL is tried with GET, it doesn't return a 500 error.
        """
        assert client.get('/'+text).status_code != 500

    @given(st.text())
    def test_post(self, client, text):
        """
        When an arbitrary URL is tried with POST, it doesn't return a 500 error.
        """
        assert client.post('/'+text).status_code != 500


class TestLogin:
    @given(st.text(), st.text())
    def test_username_password(self, client, username, password):
        """
        The login prompt should return a 200 OK status no matter what.
        """
        assert client.post('/login',
                           data=dict(username=username, password=password, follow_redirects=True)).status_code == 200

# Invariants
# - Don't ever throw a 500 exception
# - All URLs respond with something that isn't a 404
# - Don't ever lose data

# Coverage
# /login
# - username
# - password
# /logout
# - state change
# /
# - state of articles
# /new
# - title
# - logged in?
# - content
