import logging

from ..core.decorators import otp_required
from ..core.handlers import BaseRequestHandler
from ..settings import AUTH_LOGIN_URL
from .forms import OTPForm, LoginForm, RegistrationForm


logger = logging.getLogger(__name__)


class FormMixin:

    def get_template_namespace(self):
        """
        Pass additional variables to the templates.
        """
        data = super().get_template_namespace()

        data['tokens_url'] = self.reverse_url('tokens')

        return data

    def login_form(self, messages=None):
        self.render(
            'auth/login.html',
            username=self.get_argument('username', ''),
            password=self.get_argument('password', ''),
            redirect=self.get_argument('redirect', self.reverse_url('home')),
            messages=messages,
        )


class SubmitMixin:

    async def post(self):
        form = LoginForm(
            username=self.get_argument('username', ''),
            password=self.get_argument('password', ''),
        )
        if form.validate():
            await self.form_valid(form)
        else:
            self.form_error(form)

    async def form_valid(self, form):
        token = await self.auth.login(
            form.username.data,
            form.password.data,
        )
        if token is None:
            # 400 Bad Request
            self.set_status(400)

            messages = dict(
                login='Incorrect username or password.',
            )
            self.login_form(messages)
        else:
            self.login_done(token)

    def form_error(self, form):
        # 400 Bad Request
        self.set_status(400)

        messages = dict()
        for field_name, field_errors in form.errors.items():
            for field_error in field_errors:
                messages[field_name] = field_error

        self.write(messages)

    def login_done(self, token):
        # Return the session token as a cookie.
        self.set_secure_cookie('session', token.encode())

        # Redirect back to the authorization page.
        redirect = self.get_argument('redirect', None)
        if redirect is None:
            redirect = self.reverse_url('home')
        self.redirect(redirect)


class Login(FormMixin, SubmitMixin, BaseRequestHandler):

    async def get(self):
        self.login_form()


class Logout(BaseRequestHandler):

    async def post(self):
        session_token = self.get_secure_cookie('session')

        if session_token:
            done = await self.auth.logout(session_token.decode())

            if done:
                self.redirect(self.reverse_url('login'))
                return

        self.redirect(self.reverse_url('home'))


class Register(BaseRequestHandler):

    async def get(self):
        self.registration_form()
    
    async def post(self):
        form = RegistrationForm(
            username=self.get_argument('username', ''),
            password=self.get_argument('password', ''),
        )
        if form.validate():
            await self.form_valid(form)
        else:
            self.form_error(form)

    async def form_valid(self, form):
        user = await self.auth.register(
            form.username.data,
            form.password.data,
        )
        if user is None:
            # 400 Bad Request
            self.set_status(400)

            messages = dict(
                register='Failed to create a new account.',
            )
            self.registration_form(messages)
        else:
            self.registration_done()

    def form_error(self, form):
        # 400 Bad Request
        self.set_status(400)

        messages = dict()
        for field_name, field_errors in form.errors.items():
            for field_error in field_errors:
                messages[field_name] = field_error

        self.write(messages)
    
    def registration_form(self, messages=None):
        self.render(
            'auth/register.html',
            username=self.get_argument('username', ''),
            password=self.get_argument('password', ''),
            redirect=self.get_argument('redirect', self.reverse_url('login')),
            messages=messages,
        )

    def registration_done(self):
        # Redirect back to the authorization page.
        redirect = self.get_argument('redirect', None)
        if redirect is None:
            redirect = self.reverse_url('login')
        logger.info('Redirecting to: {}'.format(redirect))
        self.redirect(redirect)


class OTP(BaseRequestHandler):

    @otp_required
    async def get(self):
        await self.otp_form()
    
    @otp_required
    async def post(self):
        form = OTPForm(otpvalue=self.get_argument('otpvalue', ''))

        if form.validate():
            await self.form_valid(form)
        else:
            await self.form_error(form)

    async def form_valid(self, form):
        verified = await self.auth.otp_verify(self.current_user['id'], form.otpvalue.data)

        if not verified:
            messages = dict(
                otp='Invalid OTP.',
            )
            await self.otp_form(messages)
        else:
            await self.otp_done()

    async def form_error(self, form):
        messages = dict()
        for field_name, field_errors in form.errors.items():
            for field_error in field_errors:
                messages[field_name] = field_error

        self.write(messages)
    
    async def otp_form(self, messages=None):
        self.render(
            'auth/otp.html',
            otpvalue=self.get_argument('otpvalue', ''),
            redirect=self.get_argument('redirect', self.reverse_url('login')),
            messages=messages,
        )

    async def otp_done(self):
        token = self.get_secure_cookie('session')

        if token is not None:
            self.current_user['otp_verified'] = True

            saved = await self.session.set(token.decode(), self.current_user)

            if saved:
                logger.debug('The session has been updated.')
            else:
                logger.debug('The session was not updated.')

        redirect = self.get_argument('redirect', None)
        if redirect is None:
            redirect = self.reverse_url('home')
        logger.info('Redirecting to: {}'.format(redirect))
        self.redirect(redirect)


class Tokens(FormMixin, BaseRequestHandler):

    async def post(self):
        form = LoginForm(
            username=self.get_argument('username', ''),
            password=self.get_argument('password', ''),
        )
        if form.validate():
            await self.form_valid(form)
        else:
            self.form_error(form)

    async def form_valid(self, form):
        token = await self.auth.login(
            form.username.data,
            form.password.data,
        )
        if token is None:
            # 400 Bad Request
            self.set_status(400)

            messages = dict(
                login='Incorrect username or password.',
            )
            self.login_form(messages)
        else:
            self.login_done(token)

    def form_error(self, form):
        # 400 Bad Request
        self.set_status(400)

        messages = dict()
        for field_name, field_errors in form.errors.items():
            for field_error in field_errors:
                messages[field_name] = field_error

        self.write(messages)

    def login_done(self, token):
        # Return the session token as a cookie.
        self.set_secure_cookie('session', token.encode())

        # Redirect back to the authorization page.
        redirect = self.get_argument('redirect', None)
        if redirect is None:
            redirect = self.reverse_url('home')
        self.redirect(redirect)
