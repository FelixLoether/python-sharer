import oauth2
import urllib
from flexmock import flexmock
from sharer import TwitterSharer, OAuthSharer


class TestTwitterSharer(object):
    def setup_method(self, method):
        self.sharer = TwitterSharer(
            consumer_key='',
            consumer_secret='',
            access_token='',
            access_token_secret='',
        )

    def test_inherits_oauth_sharer(self):
        assert isinstance(self.sharer, OAuthSharer)

    def test_send(self):
        got_request = (
            flexmock(oauth2.Client)
            .should_receive('request')
            .once()
            .with_args(
                'https://api.twitter.com/1.1/statuses/update.json',
                method='POST',
                body='status=test'
            )
            .and_return([flexmock(status=200)])
        )
        assert self.sharer.send('test') is True
        got_request.verify()

    def test_send_hashtag(self):
        got_request = (
            flexmock(oauth2.Client)
            .should_receive('request')
            .once()
            .with_args(
                'https://api.twitter.com/1.1/statuses/update.json',
                method='POST',
                body='status=%s' % urllib.quote_plus('test #hash')
            )
            .and_return([flexmock(status=200)])
        )
        assert self.sharer.send('test', hashtag='#hash') is True
        got_request.verify()

    def test_send_fail_returns_false(self):
        (flexmock(oauth2.Client)
            .should_receive('request')
            .and_return([flexmock(status=500)]))
        assert self.sharer.send('test') is False
