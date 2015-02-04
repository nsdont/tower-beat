import requests


class Notifier(object):

    def __init__(self, config):
        if 'smscn' not in config:
            raise EnvironmentError('Smscn config don"t exist')
        self.config = config['smscn']

    def notify(self, message, *args, **kwargs):
        content = "{} {}".format(self.config['PREFIX'], message)
        self.send_sms(content)

    def send_sms(self, content):
        params = {
            'uid': self.config['USERNAME'],
            'pwd': self.config['PASSWORD'],
            'mobile': self.config['MOBILE'],
            'content': content.encode('gbk')
        }
        response = requests.get(self.config['URL'], params=params)
        data = response.content.decode('gbk').split("&")
        status = data[1].split("=")[1]

        if status == '100':
            print('Notification Sms Send Success')
        else:
            print('Notification Sms Send Faild')
