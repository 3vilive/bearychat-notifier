# coding: utf-8

import requests


class Color(object):
    Red = '#db4c5d'
    Purple = '#ca4cdb'
    Pink = '#db4ca4'
    Blue = '#66ccff'
    Black = '#000000'
    White = '#ffffff'
    Green = '#66ff99'
    Yellow = '#ffff00'


class NotifyLevel(object):
    Normal = 'normal'
    Warning = 'warning'
    Success = 'success'
    Error = 'error'


notify_level2color = {
    NotifyLevel.Normal: Color.Blue,
    NotifyLevel.Warning: Color.Yellow,
    NotifyLevel.Success: Color.Green,
    NotifyLevel.Error: Color.Red,
}


class BearyChatNotifier(object):
    def __init__(self, web_hook_url):
        self.web_hook_url = web_hook_url
        self.session = requests.session()

    def base_notify(self, text, notification=None, markdown=True, channel=None, user=None, attachments=None, timeout=5):
        payload = {
            'text': text,
            'notification': notification,
            'markdown': markdown,
            'channel': channel,
            'user': user,
            'attachments': attachments,
        }

        resp = self.session.post(self.web_hook_url, json=payload, timeout=timeout)
        resp_json = resp.json()
        return resp_json

    @staticmethod
    def make_attachment(title=None, url=None, text=None, color=None, images=None):
        attachment = {
            'title': title,
            'url': url,
            'text': text,
            'color': color,
            'images': images,
        }

        return attachment

    def notify(self, title, sub_title=None, text=None, url=None, images=None, level=NotifyLevel.Normal,
               notification=None, markdown=True, channel=None, user=None, timeout=5):
        color = notify_level2color[level]
        attachment = self.make_attachment(title=sub_title, url=url, text=text, color=color, images=images)
        return self.base_notify(title, notification=notification, markdown=markdown,
                                channel=channel, user=user, attachments=[attachment], timeout=timeout)


def test():
    web_hook_url = 'place your web hook here'
    notifier = BearyChatNotifier(web_hook_url)

    notifier.notify(
        title='Analysis completed',
        text='check out on https://url.to.somewhere.com',
        level=NotifyLevel.Success,
    )

    notifier.notify(
        title='Hey! 普通的通知',
        text='↓',
        images=['https://wx2.sinaimg.cn/large/c0788b86ly1fx3bieu1gyj20ir0p0jxw.jpg']
    )

    notifier.notify(
        title='Server Error Report',
        text='On Server_34\nError: disk space not enough\nInfo: Used 374G Avail 0G',
        level=NotifyLevel.Error
    )


if __name__ == '__main__':
    test()
