import os


# stripedemo/
ROOT = os.path.dirname(os.path.abspath(__file__))


ENV = 'default'
PORT = 9000
DEBUG = True
SECRET = (
    'sWArxfCwlgtf6YCKfxs0'
    'Zfs1ILq3gUYnqnAIYIfS'
)
DATABASE = os.path.join(os.path.dirname(ROOT), 'stripedemo.db')

HASH_FUNC = 'sha256'
HASH_ITER = 100000
SALT_BITS = 4

# stripedemo/static
STATIC_PATH = os.path.join(ROOT, 'static')

# stripedemo/templates
TEMPLATE_PATH = os.path.join(ROOT, 'templates')

#
# Stripe settings.
#
STRIPE_PUBLIC_KEY = os.getenv(
    'STRIPEDEMO_STRIPE_PUBLIC_KEY',
    'pk_test_5KsdSiMNj3',
)

STRIPE_SECRET_KEY = os.getenv(
    'STRIPEDEMO_STRIPE_SECRET_KEY',
    'sk_test_X7kxkNPFcQ',
)
