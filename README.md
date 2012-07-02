Remote Google App Engine OAuth backend for Django
=================================================

[Django-AppEngine-Auth](https://github.com/mback2k/django-appengine-auth) is an
extension to [Django-Social-Auth](https://github.com/omab/django-social-auth)
which adds a OAuth backend for Google App Engine based Google Accounts.

Installation
------------
You can install the latest version from GitHub manually:

    git clone https://github.com/mback2k/django-appengine-auth.git
    cd django-appengine-auth
    python setup.py install

or via pip:

    pip install https://github.com/mback2k/django-appengine-auth/zipball/master

Configuration
-------------
Add the package to your `INSTALLED_APPS`:

    INSTALLED_APPS += (
        'social_auth',
        'appengine_auth',
    )

Add the backend to your `AUTHENTICATION BACKENDS`:

    AUTHENTICATION_BACKENDS += (
        'appengine_auth.backends.GoogleAppEngineOAuthBackend',
    )

Additional Settings
-------------------
Add some or all of the following settings to your `settings.py`:

    # Hostname of the OAuth and Web Service endpoint
    GOOGLE_APPENGINE_OAUTH_SERVER = 'oauth-profile.appspot.com'

    # Use static and unique Google App Engine user's user_id as identifier
    # Defaults to False which makes it use the user's email address
    GOOGLE_APPENGINE_OAUTH_USE_UNIQUE_USER_ID = True

    # Setup Google OAuth cunsumer key and secret
    GOOGLE_APPENGINE_CONSUMER_KEY = ''
    GOOGLE_APPENGINE_CONSUMER_SECRET = ''

Please refer to the [Django-Social-Auth](http://django-social-auth.readthedocs.org/)
documentation for additional information.

License
-------
* Released under MIT License
* Copyright (c) 2012 Marc Hoersken <info@marc-hoersken.de>
