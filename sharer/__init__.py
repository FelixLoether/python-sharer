import abc
import oauth2
import requests
import urllib


class AbstractSharer(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def send(self, message, **kw):
        pass


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


class TwitterSharer(OAuthSharer):
    def send(self, message, hashtag='', **kw):
        if hashtag:
            message += ' ' + hashtag

        request = self.client.request(
            'https://api.twitter.com/1.1/statuses/update.json',
            method='POST',
            body='status=%s' % urllib.quote_plus(message)
        )[0]
        return request.status == 200


class FacebookFeedSharer(AbstractSharer):
    def __init__(self, feed_id=None, access_token=None):
        super(FacebookFeedSharer, self).__init__()
        self.feed_id = feed_id
        self.access_token = access_token

    def send(self, message, **kw):
        request = requests.post(
            'https://graph.facebook.com/%s/feed' % self.feed_id,
            data={
                'message': message,
                'access_token': self.access_token
            }
        )
        return request.status_code == 200


class MultiSharer(AbstractSharer):
    def __init__(self, **kw):
        super(MultiSharer, self).__init__()
        self.sharers = {}
        self.add_sharers(**kw)

    def add_sharers(self, **kw):
        for key, val in kw.iteritems():
            self.sharers[key] = val

    def send(self, *args, **kw):
        for name, sharer in self.sharers.iteritems():
            sharer.send(*args, **kw)
