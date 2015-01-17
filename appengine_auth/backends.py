# -*- coding: utf-8 -*-
from urllib2 import Request, urlopen

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from social_auth.utils import setting
from social_auth.backends.google import GoogleOAuth, GoogleOAuth2
from social_auth.backends.google import GoogleOAuthBackend, GoogleOAuth2Backend


# Google OAuth base configuration
GOOGLE_OAUTH_SERVER = setting('GOOGLE_APPENGINE_OAUTH_SERVER', 'oauth-profile.appspot.com')
AUTHORIZATION_URL = 'https://%s/_ah/OAuthAuthorizeToken' % GOOGLE_OAUTH_SERVER
REQUEST_TOKEN_URL = 'https://%s/_ah/OAuthGetRequestToken' % GOOGLE_OAUTH_SERVER
ACCESS_TOKEN_URL = 'https://%s/_ah/OAuthGetAccessToken' % GOOGLE_OAUTH_SERVER

GOOGLE_APPENGINE_PROFILE_V1 = 'https://%s/oauth/v1/userinfo' % GOOGLE_OAUTH_SERVER
GOOGLE_APPENGINE_PROFILE_V2 = 'https://%s/oauth/v2/userinfo' % GOOGLE_OAUTH_SERVER


# Backends
class BaseAppEngineAuthProfile(object):
    def get_user_details(self, response):
        """Return the information retrieved from the API endpoint"""
        email = response['email']
        return {'username': response.get('nickname', email).split('@', 1)[0],
                'email': email,
                'fullname': '',
                'first_name': '',
                'last_name': ''}


class GoogleAppEngineOAuthBackend(BaseAppEngineAuthProfile, GoogleOAuthBackend):
    """Google App Engine OAuth authentication backend"""
    name = 'google-appengine-oauth'

    def get_user_id(self, details, response):
        """Use google email or appengine user_id as unique id"""
        user_id = super(GoogleAppEngineOAuthBackend, self).get_user_id(details, response)
        if setting('GOOGLE_APPENGINE_OAUTH_USE_UNIQUE_USER_ID', False):
            return response['id']
        return user_id


class GoogleAppEngineOAuth2Backend(BaseAppEngineAuthProfile, GoogleOAuth2Backend):
    """Google App Engine OAuth2 authentication backend"""
    name = 'google-appengine-oauth2'

    def get_user_id(self, details, response):
        """Use google email or appengine user_id as unique id"""
        user_id = super(GoogleAppEngineOAuth2Backend, self).get_user_id(details, response)
        if setting('GOOGLE_APPENGINE_OAUTH_USE_UNIQUE_USER_ID', False):
            return response['id']
        return user_id


# Auth classes
class GoogleAppEngineOAuth(GoogleOAuth):
    """Google App Engine OAuth authorization mechanism"""
    AUTHORIZATION_URL = AUTHORIZATION_URL
    REQUEST_TOKEN_URL = REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = ACCESS_TOKEN_URL
    SERVER_URL = GOOGLE_OAUTH_SERVER
    AUTH_BACKEND = GoogleAppEngineOAuthBackend
    SETTINGS_KEY_NAME = 'GOOGLE_APPENGINE_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'GOOGLE_APPENGINE_CONSUMER_SECRET'

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Google API"""
        request = self.oauth_request(access_token, GOOGLE_APPENGINE_PROFILE_V1)
        url, params = request.to_url().split('?', 1)
        return google_appengine_userinfo_v1(url, params)

    def oauth_request(self, token, url, extra_params=None):
        """Add OAuth parameters to the request"""
        extra_params = extra_params or {}
        # Skip direct super class since scope and other parameters are not supported
        return super(GoogleOAuth, self).oauth_request(token, url, extra_params)

    @classmethod
    def get_key_and_secret(cls):
        """Return key and secret and fix anonymous settings"""
        key_and_secret = super(GoogleAppEngineOAuth, cls).get_key_and_secret()
        if key_and_secret == (None, None):
            return 'anonymous', 'anonymous'
        return key_and_secret


class GoogleAppEngineOAuth2(GoogleOAuth2):
    """Google App Engine OAuth2 authentication backend"""
    AUTH_BACKEND = GoogleAppEngineOAuth2Backend
    SETTINGS_KEY_NAME = 'GOOGLE_APPENGINE_CLIENT_ID'
    SETTINGS_SECRET_NAME = 'GOOGLE_APPENGINE_CLIENT_SECRET'

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Google API"""
        return google_appengine_userinfo_v2(GOOGLE_APPENGINE_PROFILE_V2, access_token)


def google_appengine_userinfo_v1(url, params):
    """Loads user data from OAuth Profile Google App Engine App.

    Parameters must be passed in queryset and Authorization header as described
    on Google OAuth documentation at:
    http://groups.google.com/group/oauth/browse_thread/thread/d15add9beb418ebc
    and: http://code.google.com/apis/accounts/docs/OAuth2.html#CallingAnAPI
    """
    request = Request(url + '?' + params, headers={'Authorization': params})
    try:
        return json.loads(urlopen(request).read())
    except (ValueError, KeyError, IOError):
        return None


def google_appengine_userinfo_v2(url, access_token):
    """Loads user data from OAuth Profile Google App Engine App.

    The access_token parameter is passed as a Bearer authorization.
    """
    request = Request(url, headers={'Authorization': 'Bearer ' + access_token})
    try:
        return json.loads(urlopen(request).read())
    except (ValueError, KeyError, IOError):
        return None


# Backend definition
BACKENDS = {
    'google-appengine-oauth': GoogleAppEngineOAuth,
    'google-appengine-oauth2': GoogleAppEngineOAuth2,
}
