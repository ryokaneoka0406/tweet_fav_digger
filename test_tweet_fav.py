import requests
import pytest

import tweet_like_digger


class MockResponseGetLikeIDByScreenname:
    """
    mock of GET favorites/list API
    References:
    https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/get-favorites-list
    """

    def __init__(self):
        self.status_code = 200

    @staticmethod
    def json():
        return [
            {"id": 11111},
            {"id": 22222}]


@pytest.fixture
def mock_response_like_list(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponseGetLikeIDByScreenname()

    monkeypatch.setattr(requests, "get", mock_get)


def test_get_like_id(mock_response_like_list):
    result1 = tweet_like_digger.get_like_id_list("ryopenguin")
    result2 = tweet_like_digger.get_like_id_list(
        "ryopenguin", top_id=1323781753203421184)
    assert result1 == 11111
    assert result2 == 22222


class MockResponseGetLikeIDError:
    """
    mock of GET favorites/list API Error
    References:
    https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/get-favorites-list
    """

    def __init__(self):
        self.status_code = 404
        self.text = "Not found"


@pytest.fixture
def mock_response_like_list_error(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponseGetLikeIDError()

    monkeypatch.setattr(requests, "get", mock_get)


def test_get_like_id_err(mock_response_like_list_error):
    result = tweet_like_digger.get_like_id_list("ryopenguin")
    assert result == 'Getting Data Failed...(error : Not found )'


class MockResponseGetTweetByID:
    """
    mock of GET /2/tweets/:id
    References:
    https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets-id
    """

    def __init__(self):
        self.status_code = 200

    @staticmethod
    def json():
        return {
            "data": {
                "id": "1067094924124872705",
                "text": "mock_response"
            }
        }


@pytest.fixture
def mock_response_get_tweet(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponseGetTweetByID()

    monkeypatch.setattr(requests, "get", mock_get)


class MockResponseGetTweetByIDError:
    """
    mock of GET /2/tweets/:id Error
    References:
    https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets-id
    """

    def __init__(self):
        self.status_code = 404
        self.text = 'Not found'


@pytest.fixture
def mock_response_get_tweet_error(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponseGetTweetByIDError()

    monkeypatch.setattr(requests, "get", mock_get)


def test_get_tweet_from_id(mock_response_get_tweet_error):
    id = 11111
    result = tweet_like_digger.get_tweet_from_id(id)
    assert result == 'Getting Data Failed...(error : Not found )'


def test_get_url_list_from_text():
    text = """
    URL1はこちらです。https://qiita.com/です。
    URL2はこちらですね。https://ja.wikipedia.org/wiki/Python
    改行からURL3を抽出します。
    URL4はこちらです。https://www.google.com/おいらはかねおかです。
    """
    result = tweet_like_digger.get_url_list_from_text(text)
    assert result == ["https://qiita.com/",
                      "https://ja.wikipedia.org/wiki/Python",
                      "https://www.google.com/"]


def test_remove_twitter_url():
    url1 = "https://example.com"
    url2 = "https://twitter.com/i/web/status/1323781753203421184"
    url3 = None
    assert tweet_like_digger.remove_twitter_url(url1) == "https://example.com"
    assert tweet_like_digger.remove_twitter_url(url2) is None
    assert tweet_like_digger.remove_twitter_url(url3) is None
