from sharer import OAuthSharer, AbstractSharer


class TestSharer(OAuthSharer):
    # Implement the abstract methods so we can instanciate
    def send(self, message, **kw):
        pass


class TestOAuthSharer(object):
    def setup_method(self, method):
        self.consumer_key = object()
        self.consumer_secret = object()
        self.access_token = object()
        self.access_token_secret = object()
        self.sharer = TestSharer(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
        )

    def test_init_sets_keys_and_secrets(self):
        assert self.consumer_key is self.sharer.consumer_key
        assert self.consumer_secret is self.sharer.consumer_secret
        assert self.access_token is self.sharer.access_token
        assert self.access_token_secret is self.sharer.access_token_secret

    def test_extends_abstract_sharer(self):
        assert isinstance(self.sharer, AbstractSharer)

    def test_client_returns_valid_client(self):
        client = self.sharer.client
        assert client.consumer.key is self.consumer_key
        assert client.consumer.secret is self.consumer_secret
        assert client.token.key is self.access_token
        assert client.token.secret is self.access_token_secret

    def test_consumer_returns_valid_consumer(self):
        consumer = self.sharer.consumer
        assert consumer.key is self.consumer_key
        assert consumer.secret is self.consumer_secret

    def test_token_returns_valid_token(self):
        token = self.sharer.token
        assert token.key is self.access_token
        assert token.secret is self.access_token_secret
