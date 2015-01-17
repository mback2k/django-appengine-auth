Remote Google App Engine OAuth backend for Django
=================================================

[Django-AppEngine-Auth](https://github.com/mback2k/django-appengine-auth) is an
extension to [Django-Social-Auth](https://github.com/omab/django-social-auth)
which adds a OAuth backend for Google App Engine based Google Accounts.

This application makes use of the
[Google App Engine OAuth Profile endpoint application](https://github.com/mback2k/appengine-oauth-profile)
which is by default hosted at https://oauth-profile.appspot.com/

Dependencies
------------
- django-social-auth [https://github.com/omab/django-social-auth]
- oauth2             [https://github.com/simplegeo/python-oauth2]

Installation
------------
Install the latest version from pypi.python.org:

    pip install django-appengine-auth

Install the development version by cloning the source from github.com:

    pip install git+https://github.com/mback2k/django-appengine-auth.git

Configuration
-------------
Add the package to your `INSTALLED_APPS`:

    INSTALLED_APPS += (
        'social_auth',
        'appengine_auth',
    )

Add the desired backends to your `AUTHENTICATION BACKENDS`:

    AUTHENTICATION_BACKENDS += (
        'appengine_auth.backends.GoogleAppEngineOAuthBackend',
        'appengine_auth.backends.GoogleAppEngineOAuth2Backend',
    )

Add the pipeline to your `SOCIAL_AUTH_PIPELINE`:

    SOCIAL_AUTH_PIPELINE = (
        'social_auth.backends.pipeline.social.social_auth_user',
        'appengine_auth.pipelines.associate_by_user_id',
        # Removed by default since it can be a dangerouse behavior that
        # could lead to accounts take over.
        #'social_auth.backends.pipeline.associate.associate_by_email',
        'social_auth.backends.pipeline.user.get_username',
        'social_auth.backends.pipeline.user.create_user',
        'social_auth.backends.pipeline.social.associate_user',
        'social_auth.backends.pipeline.social.load_extra_data',
        'social_auth.backends.pipeline.user.update_user_details',
    )

Additional Settings
-------------------
Add some or all of the following settings to your `settings.py`:

    # Hostname of the OAuth and Web Service endpoint
    GOOGLE_APPENGINE_OAUTH_SERVER = 'oauth-profile.appspot.com'

    # Use static and unique Google App Engine user's user_id as identifier
    # Defaults to False which makes it use the user's email address
    GOOGLE_APPENGINE_OAUTH_USE_UNIQUE_USER_ID = True

    # Setup Google OAuth 1.0 consumer key and secret
    GOOGLE_APPENGINE_CONSUMER_KEY = ''
    GOOGLE_APPENGINE_CONSUMER_SECRET = ''

    # or Setup Google OAuth 2.0 client id and secret
    GOOGLE_APPENGINE_CLIENT_ID = ''
    GOOGLE_APPENGINE_CLIENT_SECRET = ''

Please refer to the [Django-Social-Auth](http://django-social-auth.readthedocs.org/)
documentation for additional information.

License
-------
* Released under MIT License
* Copyright (c) 2012-2015 Marc Hoersken <info@marc-hoersken.de>
