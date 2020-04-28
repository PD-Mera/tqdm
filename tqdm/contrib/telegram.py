"""
Send updates to a Telegram bot.

Usage:
    from tqdm.contrib.telegram import tqdm, trange
    for i in trange(10, token='1234567890:THIS1SSOMETOKEN0BTAINeDfrOmTELEGrAM',
                    chat_id='0246813579'):
        ...
"""
from __future__ import absolute_import
from html import escape

from requests import Session

from tqdm.auto import tqdm as tqdm_auto
from tqdm.utils import _range
__author__ = {"github.com/": ["casperdcl"]}
__all__ = ['TelegramIO', 'tqdm_telegram', 'ttgrange', 'tqdm', 'trange']


class TelegramIO():
    API = 'https://api.telegram.org/bot'

    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.session = session = Session()
        self.text = self.__class__.__name__
        try:
            res = session.post(
                self.API + '%s/sendMessage' % self.token,
                data=dict(text=escape(self.text), chat_id=self.chat_id,
                          parse_mode='HTML'))
        except Exception as e:
            print(e)
        else:
            self.message_id = res.json()['result']['message_id']

    def write(self, s):
        if not s:
            return
        s = s.strip().replace('\r', '')
        if s == self.text:
            return  # avoid duplicate message Bot error
        self.text = s
        try:
            return self.session.post(
                self.API + '%s/editMessageText' % self.token,
                data=dict(text=escape(s), chat_id=self.chat_id,
                          message_id=self.message_id, parse_mode='HTML'))
        except Exception as e:
            print(e)


class tqdm_telegram(tqdm_auto):
    def __init__(self, *args, **kwargs):
        """
        Parameters
        ----------
        token  : str, required. Telegram token.
        chat_id  : str, required. Telegram chat ID.


        See `tqdm.auto.tqdm.__init__` for other parameters.
        """
        self.tgio = TelegramIO(kwargs.pop('token'), kwargs.pop('chat_id'))
        super().__init__(*args, **kwargs)

    def display(self, msg=None, **kwargs):
        super().display(msg=msg, **kwargs)
        fmt = self.format_dict
        if 'bar_format' in fmt and fmt['bar_format']:
            fmt['bar_format'] = fmt['bar_format'].replace('<bar/>', '{bar}')
        self.tgio.write(self.format_meter(**fmt))


def ttgrange(*args, **kwargs):
    """
    A shortcut for `tqdm.contrib.telegram.tqdm(xrange(*args), **kwargs)`.
    On Python3+, `range` is used instead of `xrange`.
    """
    return tqdm_telegram(_range(*args), **kwargs)


# Aliases
tqdm = tqdm_telegram
trange = ttgrange
