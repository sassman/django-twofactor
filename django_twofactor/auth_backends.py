import logging
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django_twofactor.models import UserAuthToken

log = logging.getLogger(__name__)


class TwoFactorAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, token=None):
        """
        authenticate a username with a password against the ModelBackend first,
        on success it authenticates the user against the TwoFactor Algorithm
        if a token is given and the given user has configured TwoFactor Auth

        One speciality is available for BasicAuth compatibility:
            token can be pushed into username like this "12345\myusername"
            therefore the NT known notation of domain and user is still
            possible like this: "12345\mydomain\username"

        :param username: username that ModelBackend knows as this
        :param password: password that ModelBackend can auth against
        :param token: token that can be checked if user has configured TwoFactor
        :return: User or None
        """
        if token is None and '\\' in username:
            # here some specials, allow the left site of \ in username to be a token
            (token, username) = username.split('\\', 1)

        # Validate username and password first
        user_or_none = super(TwoFactorAuthBackend, self).authenticate(username, password)

        if user_or_none and isinstance(user_or_none, User):
            log.debug('user found')
            # Got a valid login. Now check token.
            try:
                user_token = UserAuthToken.objects.get(user=user_or_none)
            except UserAuthToken.DoesNotExist:
                # User doesn't have two-factor authentication enabled, so
                # just return the User object.
                return user_or_none

            log.debug('check the auth token..')
            validate = user_token.check_auth_code(token)
            if not validate:
                log.debug('bad auth token given..')
                user_or_none = None
        return user_or_none