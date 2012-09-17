import oauth2
from .base import AbstractSharer


class OAuthSharer(AbstractSharer):
    def __init__(self, consumer_key=None, consumer_secret=None,
                 access_token=None, access_token_secret=None):
        super(OAuthSharer, self).__init__()
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    @property
    def client(self):
        return oauth2.Client(self.consumer, self.token)

    @property
    def consumer(self):
        return oauth2.Consumer(
            key=self.consumer_key,
            secret=self.consumer_secret
        )

    @property
    def token(self):
        return oauth2.Token(
            key=self.access_token,
            secret=self.access_token_secret
        )
