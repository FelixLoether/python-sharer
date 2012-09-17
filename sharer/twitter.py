import urllib
from .oauth import OAuthSharer


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
