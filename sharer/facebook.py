import requests
from .base import AbstractSharer


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
