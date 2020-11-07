import urllib.request

import requests
import pytest

import tweet_fav


class MockResponseGetLikesByScreenname:
    """
    mock of GET favorites/list API
    References:
    https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/get-favorites-list
    """
    @staticmethod
    def json():
        return [
            {"text": """日本国民は、正当に選挙された国会における代表者を通じて行動し、
            われらとわれらの子孫のために、諸国民との協和による成果と、わが国全土にわたつて
            自由のもたらす恵沢を確保し、政府の行為によつて再び戦争の惨禍"""},
            {"text": """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            Etiam tempor laoreet velit ut feugiat. 
            Phasellus lobortis nisi."""}]

    @staticmethod
    def status_code():
        return 200


@pytest.fixture
def mock_response_fav_list(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponseGetLikesByScreenname()

    monkeypatch.setattr(requests, "get", mock_get)


def test_get_json(mock_response_fav_list):
    result = tweet_fav.get_like_text_list(2, "ryopenguin")
    assert result == ["""日本国民は、正当に選挙された国会における代表者を通じて行動し、
            われらとわれらの子孫のために、諸国民との協和による成果と、わが国全土にわたつて
            自由のもたらす恵沢を確保し、政府の行為によつて再び戦争の惨禍""",
                      """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            Etiam tempor laoreet velit ut feugiat. 
            Phasellus lobortis nisi."""
                      ]


def test_get_url_list_from_text():
    text = """
    URL1はこちらです。https://qiita.com/です。
    URL2はこちらですね。https://ja.wikipedia.org/wiki/Python
    改行からURL3を抽出します。
    URL4はこちらです。https://www.google.com/おいらはかねおかです。
    """
    result = tweet_fav.get_url_list_from_text(text)
    assert result == ["https://qiita.com/",
                      "https://ja.wikipedia.org/wiki/Python",
                      "https://www.google.com/"]


def test_remove_twitter_url():
    url1 = "https://example.com"
    url2 = "https://twitter.com/i/web/status/1323781753203421184"
    assert tweet_fav.remove_twitter_url(url1) == "https://example.com"
    assert tweet_fav.remove_twitter_url(url2) is None
