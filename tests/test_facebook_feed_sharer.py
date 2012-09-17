from flexmock import flexmock
import requests
from sharer import FacebookFeedSharer, AbstractSharer


class TestFacebookFeedSharer(object):
    def setup_method(self, method):
        self.feed_id = 'feedio-idioto'
        self.access_token = 'accessio-tokenio'
        self.sharer = FacebookFeedSharer(
            self.feed_id, self.access_token
        )

    def test_init_sets_attributes(self):
        assert self.sharer.feed_id is self.feed_id
        assert self.sharer.access_token is self.access_token

    def test_inherits_abstract_sharer(self):
        assert isinstance(self.sharer, AbstractSharer)

    def test_send(self):
        got_request = (
            flexmock(requests)
            .should_receive('post')
            .once()
            .with_args(
                'https://graph.facebook.com/feedio-idioto/feed',
                data={
                    'message': 'test message',
                    'access_token': self.access_token,
                }
            )
            .and_return(flexmock(status_code=200))
        )
        assert self.sharer.send('test message') is True
        got_request.verify()

    def test_send_fail(self):
        (flexmock(requests)
            .should_receive('post')
            .and_return(flexmock(status_code=500)))
        assert self.sharer.send('test message') is False
