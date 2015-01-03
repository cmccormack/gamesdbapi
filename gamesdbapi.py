#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import urllib
import urllib2
from xml.etree import ElementTree

API_URL = "http://thegamesdb.net/api/"
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
USER_AGENT += '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

class Game():
	pass
		
class Platform():

	def __init__(self, p_id, name=None, alias=None):
		self.id = p_id
		self.name = name
		self.alias = alias

	def __str__(self):
		return "Platform id:{0} name:{1} alias:{2}".format(self.id, self.name, self.alias)


def call_api(query, query_args={}):
	local_xml = query + '.xml'

	# Check if cached xml exists, retrieved within the last hour
	
	if os.path.isfile(local_xml):
		time_diff = time.time() - os.path.getmtime(local_xml)
		if time_diff < 3600:
			print "Found cached copy of {}, skipping API call. ".format(query),
			print "Last call {} minutes {} seconds ago.".format(
				int(time_diff/60), int(time_diff % 60))

		with open(local_xml) as input_xml:
			return input_xml.read()

	url_values = urllib.urlencode(query_args)
	call_url = API_URL + query + '.php?' + url_values
	print call_url
	request = urllib2.Request(call_url)
	request.add_unredirected_header('User-Agent', USER_AGENT)
	query_response = urllib2.urlopen(request).read()

	# Cache a copy of the XML response locally
	with open(local_xml, 'w') as output:
		output.write(query_response + '\n')

	return query_response


def getPlatformsList():

	query = 'GetPlatformsList'

	response = call_api(API_URL, query)
	root = ElementTree.fromstring(response)
	
	platforms = []
	for element in root.findall('./Platforms/Platform'):
		platform = Platform(element.find('id').text)
		name = element.find('name')
		if name is not None:
			platform.name = name.text
		alias = element.find('alias')
		if alias is not None:
			platform.alias = alias.text

		platforms.append(platform)

	return platforms


def getPlatformGames(platform_id):
	query = 'GetPlatformGames'
	query_args = {'platform':platform_id}

	response = call_api(query, query_args)
	return response


def getGamesList(name, platform_name=None, genre=None):

	query = 'GetGamesList'
	query_args = {'name':name}
	if platform:
		query_args['platform'] = platform_name
	if genre:
		query_args['genre'] = genre

	response = call_api(query, query_args)
	return response


def getGame(name=None, platform=None, game_id=None):

	query = 'GetGame'
	query_args = {'name': name, 'platform':platform, 'id':game_id}

	response = call_api(query, query_args)
	return response



	

if __name__ == "__main__":
	#with open('output.txt', 'w') as out:
	#	pass
	print getGame(game_id='1')
		