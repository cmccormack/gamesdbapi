#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
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

    def __init__(self):
        pass

    def __str__(self):
        pass


class Platform(object):
    """ To be completed
    """

    def __init__(self, platform_id, platform_name, platform_values=None):

        self.p_values = platform_values
        self.p_id = platform_id
        self.p_name = platform_name
        if platform_values and platform_values['alias']:
            self.p_alias = platform_values['alias']

        if self.p_values:
            self.p_alias = self.p_values['alias']
            self.p_platform = self.p_values['Platform']
            self.p_overview = self.p_values['overview']
            self.p_developer = self.p_values['developer']
            self.p_manufacturer = self.p_values['manufacturer']
            self.p_cpu = self.p_values['cpu']
            self.p_memory = self.p_values['memory']
            self.p_graphics = self.p_values['graphics']
            self.p_sound = self.p_values['sound']
            self.p_display = self.p_values['display']
            self.p_media = self.p_values['media']
            self.p_maxcontrollers = self.p_values['maxcontrollers']
            self.p_youtube = self.p_values['Youtube']
            self.p_rating = self.p_values['Rating']
            self.p_images = self.p_values['images']

    def __str__(self):
        return '\n'.join(
            [k+':'+self.p_values[k]for k in self.p_values if self.p_values[k]]
        )


class Image(object):
    """ Image object to hold URL and dimension information for platform
        and game images
    """

    def __init__(self, img_type, img_url, thumb=None, img_attribs=None):
        
        self.type = img_type
        self.url = img_url
        self.thumb = thumb

        # Parse image attributes
        self.attribs = {'side': '',
                        'width': '',
                        'height': ''
                        }
        if img_attribs:
            for attrib in img_attribs:
                self.attribs[attrib] = img_attribs[attrib]
        self.side = self.attribs['side']
        self.width = self.attribs['width']
        self.height = self.attribs['height']
            
    def __str__(self):
        return "TYPE:{}, URL:{}, THUMB_URL:{}, ATTRIBS:{})".format(
            self.type, self.url, self.thumb, self.attribs)


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
    # End cache check snippet -----------------------

    request = urllib2.Request(call_url)
    request.add_unredirected_header('User-Agent', USER_AGENT)

    try:
        query_response = urllib2.urlopen(request).read()
    except:
        print "Unable to connect to {}".format(request)

    # Cache a copy of the XML response locally
    with open(local_xml, 'w') as output:
        output.write(query_comment_xml + '\n')
        output.write(query_response + '\n')
        return query_response
    # End cache write snippet -----------------------


def get_platforms_list():
    """ To be completed
    """

    query = 'GetPlatformsList'

    response = call_api(query)
    root = ElementTree.fromstring(response)

    platforms = []
    p_values = {
        'id': None,
        'name': None,
        'alias': None
    }
    for element in root.findall('./Platforms/Platform'):

        for elem in element:
            p_values[elem.tag] = elem.text

        platforms.append(
            Platform(p_values['id'], p_values['name'], p_values['alias']))

    return platforms


def get_platform(platform_id):
    """ Returns a set of metadata and artwork data for a specified Platform ID.

        Parameters:
            platform_id (str):
                Platform identifier, str representation of integer value

        Returns:
            Platform object with metadata attributes
    """

    platform_img_types = ['fanart', 'boxart', 'banner',
                          'consoleart', 'controllerart']
    query = 'GetPlatform'
    query_args = {'id': platform_id}

    response = call_api(query, query_args)
    root = ElementTree.fromstring(response)

    p_values = {
        'id': '',
        'Platform': '',
        'alias': '',
        'overview': '',
        'developer': '',
        'manufacturer': '',
        'cpu': '',
        'memory': '',
        'graphics': '',
        'sound': '',
        'display': '',
        'media': '',
        'maxcontrollers': '',
        'Youtube': '',
        'Rating': '',
        'images': ''
    }

    # Gather platform attributes from API response
    for element in root.findall('Platform'):
        for elem in element:
            p_values[elem.tag] = elem.text

    # Gather platform image details from API response
    base_img_url = root.find('baseImgUrl').text

    # Combine all image types into a single list for iteration
    all_imgs = []
    for img_type in platform_img_types:
        all_imgs += root.findall('.//' + img_type)

    # Iterate over each image type and store Image object in list
    images = []
    for element in all_imgs:
        thumb = ''
        if element.tag == 'fanart':
            thumb = element.find('.//thumb').text
            element = element.find('.//original')
        images.append(Image(element.tag, base_img_url + element.text,
                            thumb, element.attrib))
    p_values['images'] = images

    return Platform(p_values['id'], p_values['Platform'], p_values)


def get_platform_games(platform_id):
    """ To be completed
    """

    query = 'GetPlatformGames'
    query_args = {'platform': platform_id}

    response = call_api(query, query_args)
    return response


def get_games_list(name, platform_name=None, genre=None):
    """ To be completed
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
    """ To be completed
    """

    query = 'GetGame'
    query_args = {'name': name, 'platform': platform, 'id': game_id}

    response = call_api(query, query_args)
    return response


if __name__ == "__main__":
    platform = get_platform('18')
    print '\n'.join([image.url for image in platform.p_images if image.url])
        