class TestIndex:
    def test_get(self, client):
        assert client.get('/').status == '200 OK'

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
