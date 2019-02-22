import logging

from ..core.handlers import BaseRequestHandler
from ..settings import AUTH_LOGIN_URL
from .forms import LoginForm


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
            redirect=self.get_argument('redirect', ''),
            messages=messages,
        )


class Login(FormMixin, BaseRequestHandler):

    async def get(self):
        self.login_form()


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
