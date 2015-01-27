import os

BASE_DIR = os.path.dirname(__file__)

SESSION_COOKIES_LOCATION = os.path.expanduser(r'~/Library/Application Support/'
                                              r'Google/Chrome/Default/Cookies')
SESSION_COOKIE_NAME = '_tower2_session'

QUERY_STATEMENT = (r'SELECT * FROM `cookies` WHERE '
                   r'host_key=".tower.im" AND name="_tower2_session";')

DECRYPT_COOKIE_VALUE_SALT = b'saltysalt'
DECRYPT_COOKIE_VALUE_IV = b' ' * 16
DECRYPT_COOKIE_VALUE_LENGTH = 16
DECRYPT_COOKIE_VALUE_ITERATIONS = 1003

NOTIFICATION_NOT_LOGIN = 'Please login at webbrowser first!'
NOTIFICATION_TASK_FOUND = 'Found a task that need to beat it.'

KEYRING_SERVICE = 'Chrome Safe Storage'
KEYRING_USERNAME = 'Chrome'

NOTIFIER_TITLE = 'BEAT IT'

DUE_XPATH = '//span[@class="due"]'

LOGIN_URL = 'https://tower.im/users/sign_in'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'beatit': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        }
    },
    'handlers': {
        'beatit': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'beatit.log'),
            'maxBytes': 1024 * 1024,
            'backupCount': 1,
            'formatter': 'beatit'
        }
    },
    'loggers': {
        'beatit': {
            'handlers': ['beatit'],
            'level': 'INFO',
            'progagate': True
        }
    }
}
