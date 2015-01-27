
class Notifier(object):

    def __init__(self, config):
        self.config = config

    def notify(self, message, *args, **kwargs):
        print message, ('({kwargs[open]})'.format(kwargs=kwargs)
                        if 'open' in kwargs
                        else '')
