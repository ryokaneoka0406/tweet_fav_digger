import re
import time

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


def get_like_id_list(screen_name, top_id=None):
    """
    Args:
        screen_name(string): target user screen name,
        top_id: Get Tweets before this ID
    return:
        the newest like id(integer)
    """
    url = "https://api.twitter.com/1.1/favorites/list.json?"
    params = {
        "count": 2,
        "screen_name": screen_name,
        "max_id": top_id
    }
    response = requests.get(url, auth=OAUTH, params=params, timeout=10)

    if response.status_code != 200:
        return f'Getting Data Failed...(error : {response.text} )'

    if top_id:
        return response.json()[1]['id']
    else:
        return response.json()[0]['id']


def get_tweet_from_id(tweet_id):
    """
    Args:
        tweet_id(integer): target tweet's id
    Returns:
        string: the tweet text
    """

    url = f"https://api.twitter.com/2/tweets/{tweet_id}"
    response = requests.get(url, headers={
        "Authorization": f"Bearer {settings.bearer_token}"
    })

    if response.status_code != 200:
        return f'Getting Data Failed...(error : {response.text} )'
    response_json = response.json()
    return response_json["data"]["text"]


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


def expand_url(url):
    """"
    Args:
        url(string): url
    return:
        url(string):expanded url
    """
    try:
        req = urllib.request.Request(url, method='HEAD')
        response = urllib.request.urlopen(req)
        return response.url
    except Exception as e:
        print(e)


def remove_twitter_url(url):
    """"
    Args:
        url(string): url
    return:
        (Boolean): url | twitter url
    """
    try:
        if "https://twitter.com/" not in url:
            return url
    except TypeError:
        pass


if __name__ == "__main__":
    all_url_list = []
    target_id = get_like_id_list("ryopenguin")
    text = get_tweet_from_id(target_id)
    url_list = get_url_list_from_text(text)
    for url in url_list:
        url_wo_twitter = remove_twitter_url(expand_url(url))
        if url_wo_twitter:
            all_url_list.append(url_wo_twitter)

    while len(all_url_list):
        target_id = get_like_id_list("ryopenguin", top_id=target_id)
        text = get_tweet_from_id(target_id)
        url_list = get_url_list_from_text(text)
        for url in url_list:
            url_wo_twitter = remove_twitter_url(expand_url(url))
            if url_wo_twitter:
                all_url_list.append(url_wo_twitter)

        print(all_url_list)
        time.sleep(10)
        if len(all_url_list) == 20:
            break
