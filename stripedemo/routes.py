from tornado.web import url

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
    ]
