import pyotp
import base64
import hashlib
import logging
import secrets

from datetime import datetime
from collections import namedtuple

from tornado.escape import json_encode, json_decode
from tornado.httpclient import AsyncHTTPClient, HTTPError

from ..core.models import database
from ..settings import (
    HASH_FUNC,
    HASH_ITER,
    SALT_BITS,
    AUTH_BASE_URL,
    AUTH_LOGIN_URL,
    AUTH_PEOPLE_URL,
)
from .models import User, Token


logger = logging.getLogger(__name__)


_HTTPResult = namedtuple('_HTTPResult', [
    'success',
    'payload',
])

_User = namedtuple('_User', [
    'id',
    'uri',
    'email',
    'qrcode',
])

_Contact = namedtuple('_Contact', [
    'email',
    'qrcode',
])

_AuthInfo = namedtuple('_AuthInfo', [
    'token',
    'user',
])


class AuthProvider:

    def __init__(self, main):
        self.main = main

    @property
    def session(self):
        return self.main.session

    async def login(self, username, password):
        user = await self.authenticate(username, password)
        if user is None:
            return None
        return await self.create_session(user)
    
    async def logout(self, token):
        return await self.delete_session(token)
    
    async def register(self, username, password):
        return User.new(username, password_hash(password))

    async def save_token(self, user, token):
        # Run blocking call on a separate thread.
        return await self.main.execute(save_token, user, token)

    async def authenticate(self, username, password):
        query = (
            User
            .select()
            .where(User.username == username)
        )

        user = query.first()

        if user is None:
            logger.info('User not found.')
            return None
        
        if not password_check(password, user.password):
            logger.info('Incorrect password.')
            return None

        logger.info('Got user: {}'.format(user))

        return user
    
    async def otp_verify(self, user_id, value):
        query = (
            User
            .select()
            .where(User.id == user_id)
        )

        user = query.first()

        if user is None:
            logger.info('User not found.')
            return False
        
        totp = pyotp.TOTP(user.secret.encode())

        logger.debug('Verifying the OTP: %s', value)

        if totp.verify(value):
            logger.debug('The OTP is valid: %s', value)
            return True

        logger.debug('The OTP is invalid: %s', value)

        return False

    async def fetch_user_profile(self, access_token):
        headers = {
            'Authorization': access_token
        }
        http = AsyncHTTPClient()
        try:
            response = await http.fetch(AUTH_PEOPLE_URL, headers=headers)
        except HTTPError as error:
            logger.exception('Failed to fetch user info.')
            return None

        user = json_decode(response.body)

        logger.info('Got user info: {}'.format(user))

        return user

    async def fetch_user_contact(self, access_token, user):
        headers = {
            'Authorization': access_token
        }
        http = AsyncHTTPClient()
        url = '{}{}'.format(AUTH_BASE_URL, user['contactInfo'][0])
        try:
            response = await http.fetch(url, headers=headers)
        except HTTPError as error:
            logger.exception('Failed to fetch user contact info.')
            return None

        contact = json_decode(response.body)

        logger.info('Got user contact info: {}'.format(contact))

        return _Contact(
            contact['email_1'],
            contact['qrcode_1'],
        )

    async def fetch_user_info(self, access_token):
        profile = await self.fetch_user_profile(access_token)
        if profile is None:
            return None

        contact = await self.fetch_user_contact(access_token, profile)
        if contact is None:
            return None

        return _User(
            profile['personID'],
            profile['refs']['self'],
            contact.email,
            contact.qrcode,
        )

    async def create_session(self, user):
        # Require the user to enter an OTP if there's a secret key.
        otp_required = True if user.secret is not None else False

        data = dict(
            id=user.id,
            name='',
            email=user.username,
            otp_required=otp_required,
            otp_verified=False,
        )
        token = create_session_token(user)

        logger.debug('Saving session: token={} data={}'.format(
            token,
            data,
        ))

        saved = await self.session.set(token, data)
        if not saved:
            logger.debug('Session not saved.')
            return None
        logger.debug('Session saved.')
        return token
    
    async def delete_session(self, token):
        return await self.session.delete(token)


def save_token(user, token):
    logger.debug('Saving access token: {}'.format(token))

    refresh, expires = token.get('refresh_token'), token.get('expires_in')
    with database:
        token = Token.new(
            user,
            token['access_token'],
            token_expire=expires,
            token_refresh=refresh,
        )
        if token is None:
            return False
    logger.debug('Access token saved: {}'.format(token))
    return True


def password_hash(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(SALT_BITS)
    hash = hashlib.pbkdf2_hmac(
        HASH_FUNC, password.encode(), salt.encode(), HASH_ITER
    )
    b16 = base64.b16encode(hash).decode()
    return '{}${}'.format(salt, b16)


def password_check(password, hashed_password):
    salt, hash = hashed_password.split('$')
    pass_hash = hashlib.pbkdf2_hmac(
        HASH_FUNC, password.encode(), salt.encode(), HASH_ITER
    )
    pass_b16 = base64.b16encode(pass_hash).decode()
    return pass_b16 == hash


def create_session_token(user):
    tkn, now = secrets.token_hex(16), datetime.utcnow()
    # Generate a random value which will
    # be used to create the session token.
    #
    # Example:
    # 123456$61ac314a682e7fa2c958fb1daa4ecb64$1655796867.389337
    value = '{}${}${}'.format(
        user.id, tkn, now.timestamp()
    )

    # The session token is a SHA256 hash of the above.
    return hashlib.sha256(value.encode()).hexdigest()
