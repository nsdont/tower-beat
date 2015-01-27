# Notifier on Mac OS X Notification Center.
import sys

if sys.platform != 'darwin':
    raise RuntimeError('Mac OS X system required.')

from pync import Notifier as PyncNotifier


class Notifier(object):

    def __init__(self, config):
        self.config = config

    def notify(self, message, *args, **kwargs):
        PyncNotifier.notify(message, *args, **kwargs)
