import bot.tbot as tbot


def test_method_url_returns_the_correct_urlf_for_given_method():
    method = 'getUpdates'
    expected = 'https://api.telegram.org/bot{}/{}'.format(tbot.get_api_key(), method)
    got = tbot.method_url(method)
    assert got == expected
