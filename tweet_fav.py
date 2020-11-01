import re

import requests
from requests_oauthlib import OAuth1

import settings

OAUTH = OAuth1(
    settings.consumer_key,
    settings.consumer_secret,
    settings.access_token,
    settings.access_token_secret
)


def get_like_lists(count, screen_name):
    """"
    Args:
        count(integer): tweet list length,
        screen_name(string): target user screen name
    return:
        list of id(integer)
    """
    url = "https://api.twitter.com/1.1/favorites/list.json?"
    params = {
        "count": count,
        "screen_name": screen_name
    }
    response = requests.get(url, auth=OAUTH, params=params)

    if response.status_code != 200:
        print(f'Getting Data Failed...(error code : {response.status_code} )')
    return [record["id"] for record in response.json()]


def get_tweet_from_id(tweet_id):
    """
    Args:
        tweet_id(integer): target tweet's id
    Returns:
        string: the tweet text
    """
    url = f"https://api.twitter.com/2/tweets/{tweet_id}"
    response = requests.get(url, headers={
        "Authorization": "Bearer {}".format(settings.bearer_token)
    })

    if response.status_code != 200:
        print(f'Getting Data Failed...(error code : {response.status_code} )')
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


if __name__ == "__main__":
    likeIdlists = get_like_lists(7, "ryopenguin_beer")
    idUrlList = []
    for likeId in likeIdlists:
        text = get_tweet_from_id(likeId)
        urlList = get_url_list_from_text(text)
        idUrlList.append({"tweetId": likeId, "urlList": urlList})
    print(idUrlList)
