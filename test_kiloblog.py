class TestIndex:
    def test_get(self, client):
        assert client.get('/').status == '200 OK'

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
