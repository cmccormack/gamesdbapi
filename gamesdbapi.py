#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

import urllib
import urllib2
from xml.etree import ElementTree

API_URL = "http://thegamesdb.net/api/"
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
USER_AGENT += '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'


class Game(object):
    """ test
    """

    def __init__(self):
        pass

    def __str__(self):
        pass


class Platform(object):
    """ test
    """

    def __init__(self, platform_id, platform_name, platform_alias=None):
        self.p_id = platform_id
        self.p_name = platform_name
        self.p_alias = platform_alias

    def __str__(self):
        return "id:{0};name:{1};alias:{2}".format(
            self.p_id, self.p_name, self.p_alias)


def call_api(query, query_args=None):
    """
    """

    call_url = API_URL + query + '.php?'
    call_url += urllib.urlencode(query_args) if query_args else ''
    print call_url
    request = urllib2.Request(call_url)
    request.add_unredirected_header('User-Agent', USER_AGENT)
    query_response = urllib2.urlopen(request).read()

    return query_response


def get_platforms_list():
    """
    """

    query = 'GetPlatformsList'

    response = call_api(query)
    root = ElementTree.fromstring(response)
    
    platforms = []
    platform = {}
    for element in root.findall('./Platforms/Platform'):
        platform['alias'] = ''

        for elem in element:
            platform[elem.tag] = elem.text

        platforms.append(
            Platform(platform['id'], platform['name'], platform['alias']))

    return platforms


def get_platform(platform_id):
    """ Returns a set of metadata and artwork data for a specified Platform ID.

        Parameters:
            platform_id (str):
                Platform identifier, str representation of integer value

        Returns:
            Platform object with metadata attributes
    """

    query = 'GetPlatform'
    query_args = {'id': platform_id}

    response = call_api(query, query_args)
    root = ElementTree.fromstring(response)
    platform = {}
    for element in root.findall('./Platforms/Platform'):
        platform['alias'] = ''

        for elem in element:
            platform[elem.tag] = elem.text

    return response


def get_platform_games(platform_id):
    """
    """

    query = 'GetPlatformGames'
    query_args = {'platform': platform_id}

    response = call_api(query, query_args)
    return response


def get_games_list(name, platform_name=None, genre=None):
    """
    """

    query = 'GetGamesList'
    query_args = {'name': name}
    if platform_name:
        query_args['platform'] = platform_name
    if genre:
        query_args['genre'] = genre

    response = call_api(query, query_args)
    return response


def get_game(name=None, platform=None, game_id=None):
    """
    """

    query = 'GetGame'
    query_args = {'name': name, 'platform': platform, 'id': game_id}

    response = call_api(query, query_args)
    return response


if __name__ == "__main__":
    print get_platform(1)
        