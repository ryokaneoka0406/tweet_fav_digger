import re

import requests
import urllib.request

from requests.models import Response
from requests_oauthlib import OAuth1
from bs4 import BeautifulSoup

import settings

OAUTH = OAuth1(
    settings.consumer_key,
    settings.consumer_secret,
    settings.access_token,
    settings.access_token_secret
)


def get_like_text_list(count, screen_name):
    """"
    Args:
        count(integer): tweet list length,
        screen_name(string): target user screen name
    return:
        list of text(string)
    """
    url = "https://api.twitter.com/1.1/favorites/list.json?"
    params = {
        "count": count,
        "screen_name": screen_name
    }
    response = requests.get(url, auth=OAUTH, params=params, timeout=10)

    if response.status_code != 200:
        print(f'Getting Data Failed...(error code : {response.status_code} )')
    return [record["text"] for record in response.json()]


def get_url_list_from_text(tweet_text):
    """
    Args:
        tweet_text(string): target tweet's text
    Returns:
        list of string: URLs list in tweet of arg
    """
    pattern = r"https?://[\w/:%#&~=_,\$\?\(\)\.\+\-\*][^ぁ-んァ-ン一-龥ｦ-ﾟＡ-Ｚａ-ｚ\n\s]+"
    url_list = re.findall(pattern, tweet_text)
    return url_list


def unrap_url(url):
    """"
    Args:
        url(string): url
    return:
        url(string):unwrapped url
    """
    req = urllib.request.Request(url, method='HEAD')
    response = urllib.request.urlopen(req)
    return response.url


def remove_twitter_url(url):
    """"
    Args:
        url(string): url
    return:
        (Boolean): url | twitter url
    """
    if "https://twitter.com/" not in url:
        return url


if __name__ == "__main__":
    text_list = get_like_text_list(10, "ryopenguin")
    url_list_include_tweet = []
    url_list_without_tweet = []
    for text in text_list:
        urls = get_url_list_from_text(text)
        url_list_include_tweet += urls

    for url in url_list_include_tweet:
        unrapped_url = unrap_url(url)
        unrapped_url_wo_twitter = remove_twitter_url(unrapped_url)
        if unrapped_url_wo_twitter:
            url_list_without_tweet.append(unrapped_url_wo_twitter)
    print(url_list_without_tweet)
