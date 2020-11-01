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
            {"id": 1067094924124872705},
            {"id": 1067094924124872706},
            {"id": 1067094924124872707}]

    @staticmethod
    def status_code():
        return 200


@pytest.fixture
def mock_response_fav_list(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponseGetLikesByScreenname()

    monkeypatch.setattr(requests, "get", mock_get)


def test_get_json(mock_response_fav_list):
    result = tweet_fav.get_like_lists(3, "ryopenguin")
    assert result == [1067094924124872705,
                      1067094924124872706, 1067094924124872707]


class MockResponseGetTweetByID:
    """
    mock of GET /2/tweets/:id
    References:
    https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets-id
    """
    @staticmethod
    def json():
        return {
            "data": {
                "id": "1067094924124872705",
                "text": "mock_response"
            }
        }

    @staticmethod
    def status_code():
        return 200


@pytest.fixture
def mock_response_get_tweet(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponseGetTweetByID()

    monkeypatch.setattr(requests, "get", mock_get)


def test_get_tweet_from_id(mock_response_get_tweet):
    id = 1128358947772145672
    result = tweet_fav.get_tweet_from_id(id)
    assert result == "mock_response"


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
