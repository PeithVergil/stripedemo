from tornado.web import url

from .auth import handlers as auth
from .home import handlers as home


def build_routes(main):
    kwargs = {
        'main': main,
    }
    return [
        url(
            r'/',
            home.Index,
            kwargs,
            name='home',
        ),
        url(
            r'/order',
            home.Order,
            kwargs,
            name='order',
        ),
        url(
            r'/login',
            auth.Login,
            kwargs,
            name='login',
        ),
        url(
            r'/tokens',
            auth.Tokens,
            kwargs,
            name='tokens',
        ),
    ]
