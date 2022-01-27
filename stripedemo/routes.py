from tornado.web import url

from .auth import handlers as auth
from .home import handlers as home
from .subs import handlers as subs


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
            r'/logout',
            auth.Logout,
            kwargs,
            name='logout',
        ),
        url(
            r'/register',
            auth.Register,
            kwargs,
            name='register',
        ),
        url(
            r'/tokens',
            auth.Tokens,
            kwargs,
            name='tokens',
        ),

        # Stripe subscription demo
        url(
            r'/subs',
            subs.Index,
            kwargs,
            name='subs',
        ),
        url(
            r'/subscribe',
            subs.Subscribe,
            kwargs,
            name='subscribe',
        ),
    ]
