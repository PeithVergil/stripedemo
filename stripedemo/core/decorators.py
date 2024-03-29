import logging
import functools

from tornado.httputil import url_concat


logger = logging.getLogger(__name__)


def login_required(func):
    """
    Check if the user is logged in.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.current_user is None:
            # Redirect the user back to the current page after logging in.
            args = [
                ('redirect', self.request.uri),
            ]
            return self.redirect(url_concat(self.reverse_url('login'), args))
        
        if self.current_user['otp_required'] and not self.current_user['otp_verified']:
            # Redirect the user back to the current page after logging in.
            args = [
                ('redirect', self.request.uri),
            ]
            return self.redirect(url_concat(self.reverse_url('otp'), args))

        return func(self, *args, **kwargs)
    return wrapper


def otp_required(func):
    """
    Check if the "otp required" flag is set.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.current_user is None:
            args = [
                ('redirect', self.reverse_url('home')),
            ]
            return self.redirect(url_concat(self.reverse_url('login'), args))

        if not self.current_user['otp_required'] or self.current_user['otp_verified']:
            return self.redirect(self.reverse_url('home'))

        return func(self, *args, **kwargs)
    return wrapper
