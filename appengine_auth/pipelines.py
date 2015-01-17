# -*- coding: utf-8 -*-
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from social_auth.models import UserSocialAuth
from social_auth.exceptions import AuthException


def associate_by_user_id(details, response, user=None, *args, **kwargs):
    """Return user entry with same Google user_id as returned in the response."""
    if user:
        return None

    if 'id' in response:
        # Try to associate accounts registered with the same Google user_id,
        # only if it's a single object from Google App Engine.
        # AuthException is raised if multiple objects are returned.
        try:
            user_id = response['id']
            queryset = UserSocialAuth.objects.filter(uid=user_id)
            queryset = queryset.filter(provider__startswith='google-appengine')
            return {'user': queryset.get().user}
        except MultipleObjectsReturned:
            raise AuthException(kwargs['backend'], 'Not unique Google user_id.')
        except ObjectDoesNotExist:
            pass
