from requests import HTTPError

from social.p3 import urlencode
from social.exceptions import AuthCanceled

from social.tests.backends.oauth import OAuth1Test


class EvernoteOAuth1Test(OAuth1Test):
    backend_path = 'social.backends.evernote.EvernoteOAuth'
    expected_username = '101010'
    access_token_body = urlencode({
        'edam_webApiUrlPrefix': 'https://sandbox.evernote.com/shard/s1/',
        'edam_shard': 's1',
        'oauth_token': 'foobar',
        'edam_expires': '1395118279645',
        'edam_userId': '101010',
        'edam_noteStoreUrl': 'https://sandbox.evernote.com/shard/s1/notestore'
    })
    request_token_body = urlencode({
        'oauth_token_secret': 'foobar-secret',
        'oauth_token': 'foobar',
        'oauth_callback_confirmed': 'true'
    })

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()


class EvernoteOAuth1CanceledTest(EvernoteOAuth1Test):
    access_token_status = 401

    def test_login(self):
        with self.assertRaises(AuthCanceled):
            self.do_login()

    def test_partial_pipeline(self):
        with self.assertRaises(AuthCanceled):
            self.do_partial_pipeline()


class EvernoteOAuth1ErrorTest(EvernoteOAuth1Test):
    access_token_status = 500

    def test_login(self):
        with self.assertRaises(HTTPError):
            self.do_login()

    def test_partial_pipeline(self):
        with self.assertRaises(HTTPError):
            self.do_partial_pipeline()
