#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
API Call Status:
==========================

Complete:
----------------

Almost complete:
----------------
GetPlatformsList
GetPlatform
GetGamesList

Current:
----------------
GetGame

Incomplete:
----------------
GetGame
GetArt
GetPlatformGames
PlatformGames
Updates
UserRating
UserFavorites
===========================
"""
import os
import time
import urllib
import urllib2
from xml.etree import ElementTree

API_URL = "http://thegamesdb.net/api/"
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
USER_AGENT += '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'


class Game(object):
    """ To be completed
    """

    def __init__(self, identifier, name=''):

        self.identifier = identifier
        self.gametitle = name

        self.platform = ''
        self.releasedate = ''
        self.overview = ''
        self.esrb = ''
        self.genres = []
        self.players = ''
        self.coop = ''
        self.youtube = ''
        self.publisher = ''
        self.developer = ''
        self.rating = ''
        self.images = []

    def __str__(self):
        return str(self.__dict__)


class Platform(object):
    """ Platform object to hold id and name information, as well
        as additional optional attributes.
    """

    def __init__(self, identifier, name, alias=''):

        self.identifier = identifier
        self.name = name
        self.alias = alias

        self.platform = ''
        self.overview = ''
        self.developer = ''
        self.manufacturer = ''
        self.cpu = ''
        self.memory = ''
        self.graphics = ''
        self.sound = ''
        self.display = ''
        self.media = ''
        self.maxcontrollers = ''
        self.youtube = ''
        self.rating = ''
        self.images = []

    def __str__(self):
        return str(self.__dict__)


class Image(object):
    """ Image object to hold URL and dimension information for platform
        and game images.
    """

    def __init__(self, img_type, img_url, img_thumb=None):

        self.type = img_type
        self.url = img_url
        self.thumb = img_thumb
        self.width = ''
        self.height = ''
        self.side = ''

    def __str__(self):
        return str(self.__dict__)


def call_api(query, query_args=None):
    """ To be completed
    """

    call_url = API_URL + query + '.php?'
    if query_args:
        call_url += urllib.urlencode(query_args)
    print call_url
    query_comment_xml = '<!--' + call_url + '-->'

    # Check if cached xml exists, retrieved within the last hour
    local_xml = query + '.xml'
    if os.path.isfile(local_xml):
        with open(local_xml) as input_xml:
            if input_xml.readline().strip() == query_comment_xml:
                time_diff = time.time() - os.path.getmtime(local_xml)
                if time_diff < 3600:
                    print "Found cached copy of {},".format(query),
                    print "skipping API call."
                    print "Last call {} minutes {} seconds ago.".format(
                        int(time_diff/60), int(time_diff % 60))
                    return input_xml.read()
    # End cache check snippet ----------------------------------

    request = urllib2.Request(call_url)
    request.add_unredirected_header('User-Agent', USER_AGENT)

    try:
        query_response = urllib2.urlopen(request).read()
    except urllib2.URLError:
        print "Unable to connect to {}".format(request)

    # Cache a copy of the XML response locally
    with open(local_xml, 'w') as output:
        output.write(query_comment_xml + '\n')
        output.write(query_response + '\n')
        return query_response
    # End cache write snippet ----------------------------------


def get_platforms_list():
    """ Returns a listing of all platforms available on the site,
        sorted by alphabetical order by name.

        Parameters:
            None

        Returns:
            A list of Platform objects
    """

    # API Call
    query = 'GetPlatformsList'
    response = call_api(query)
    root = ElementTree.fromstring(response)

    # Parse API response
    platforms = []
    for element in root.findall('./Platforms/Platform'):
        p_id = element.find('id').text
        p_name = element.find('name').text
        platform = Platform(p_id, p_name)

        for elem in element:
            setattr(platform, elem.tag.lower(), elem.text)

        platforms.append(platform)

    return platforms


def get_platform(platform_id):
    """ Returns a set of metadata and artwork data for a specified Platform ID.

        Parameters:
            platform_id (str):
                Platform identifier, str representation of integer value

        Returns:
            Platform object with metadata attributes

        To Do:
            Additional testing
            Cleanup unicode and HTML text
    """

    # API Call
    query = 'GetPlatform'
    query_args = {'id': platform_id}
    response = call_api(query, query_args)
    root = ElementTree.fromstring(response)

    if root.tag == 'Error':
        return None

    # Gather platform attributes from API response
    p_id = root.find('.//Platform/id').text
    p_name = root.find('.//Platform/Platform').text
    platform = Platform(p_id, p_name)

    for element in root.find('Platform'):
        setattr(platform, element.tag.lower(), element.text)

    # Gather platform image details from API response
    #  Iterate over each image type and store Image object in list
    base_img_url = root.find('baseImgUrl').text
    platform_images = []
    for element in root.find('.//Platform/Images'):
        thumb = element.find('thumb')
        if thumb is not None:
            thumb = thumb.text
        if element.tag == 'fanart':
            element = element.find('original')
        platform_image = Image(element.tag, base_img_url + element.text, thumb)
        for elem in element.attrib:
            setattr(platform_image, elem.lower(), element.attrib[elem])
        platform_images.append(platform_image)

    platform.images = platform_images

    return platform


def get_platform_games(platform_id):
    """ To be completed
    """

    query = 'GetPlatformGames'
    query_args = {'platform': platform_id}

    response = call_api(query, query_args)
    return response


def get_games_list(name, platform_name=None, genre=None):
    """ Returns a listing of games matched up with loose search terms.

        Parameters:
            name (str):
                name of game or other detail in game description
            platform (str) (optional):
                filters results by platform
            genre (str) (optional):
                filters results by genre

        Returns:
            list containing Game objects

    """

    # API Call
    query = 'GetGamesList'
    query_args = {'name': name}
    if platform_name:
        query_args['platform'] = platform_name
    if genre:
        query_args['genre'] = genre
    response = call_api(query, query_args)
    root = ElementTree.fromstring(response)
    if root.tag == 'Error':
        return None

    # Parse API Response
    games = []
    for element in root.findall('Game'):
        g_id = element.find('id').text
        g_name = element.find('GameTitle').text
        game_obj = Game(g_id, g_name)

        for elem in element:
            setattr(game_obj, elem.tag.lower(), elem.text)

        games.append(game_obj)

    return games


def get_game(name=None, platform=None, game_id=None):
    """ To be completed
    """

    query = 'GetGame'
    query_args = {'name': name, 'platform': platform, 'id': game_id}

    response = call_api(query, query_args)
    return response


if __name__ == "__main__":
    for game in get_games_list('luna'):
        print game
