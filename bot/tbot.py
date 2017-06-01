"""
This module handles messaging between the bot and the telegram API
"""
import os
import requests
import collections
import http
import operator

import bot.actions as actions


class BotException(Exception):
    pass


Message = collections.namedtuple('Message', ['sender', 'text', 'chat_id', 'update_id'])


def get_base_url():
    return 'https://api.telegram.org/bot'


def get_api_key():
    # get this from env
    key = os.getenv('TELEGRAM_BOT_AUTH_TOKEN')
    if key is None:
        raise RuntimeError('TELEGRAM_BOT_AUTH_TOKEN environment variable not set')
    return key


def method_url(method_name):
    return '{}{}/{}'.format(get_base_url(), get_api_key(), method_name)


def get_updates(message_offset=None, timeout=100):
    """
    Get  messages from the  telegram server
    :param message_offset:
    :param timeout:
    :return:
    """
    updates = requests.post(
        method_url('getUpdates'),
        json={
            'timeout': timeout,
            'offset': message_offset
        }
    )

    def get_from(message):
        return message['message']['from']['first_name'] + ' ' + message['message']['from']['last_name']

    def get_text(message):
        return message['message']['text']

    def get_chat_id(message):
        return message['message']['chat']['id']

    def get_update_id(message):
        return message['update_id']

    return [Message(get_from(m), get_text(m), get_chat_id(m), get_update_id(m)) for m in updates.json()['result']]


def send_message(text, chat_id):
    response = requests.post(
        method_url('sendMessage'),
        json={
            'chat_id': chat_id,
            'text': text,
        }
    )
    if not response.status_code == http.HTTPStatus.OK:
        raise BotException()


def main():
    max_update_id = None
    while True:
        m = get_updates(max_update_id + 1 if max_update_id else None)
        max_update_id = max(m, key=operator.itemgetter(3)).update_id
        if not actions.ACTION_FUNCS:
            send_message('Syed, you dont have any actions configured. So I have no idea what to do', m[0].chat_id)


if __name__ == '__main__':
    main()
