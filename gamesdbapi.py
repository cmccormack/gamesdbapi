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
	def __init__(self, platform_id, platform_name, platform_alias=None):
		self.platform_id = platform_id
		self.platform_name = platform_name
		self.platform_alias = platform_alias

def call_api(base_url, query, query_args={}):
	local_xml = query + '.xml'

	# Check if cached xml exists, retrieved within the last hour
	time_diff = time.time() - os.path.getmtime(local_xml)
	if os.path.isfile(local_xml) and time_diff < 3600:
		print "Found cached copy of {}, skipping API call.".format(query)
		with open(local_xml) as inxml:
			return inxml.read()

	url_values = urllib.urlencode(query_args)
	call_url = base_url + query + '.php?' + url_values
	print call_url
	request = urllib2.Request(call_url)
	request.add_unredirected_header('User-Agent', USER_AGENT)
	query_response = urllib2.urlopen(request).read()

	# Cache a copy of the XML response locally
	with open(local_xml, 'w') as output:
		output.write(query_response + '\n')

	return query_response

def getGamesList(name, platform_name=None, genre=None):
	query = 'GetGamesList'
	query_args = {'name':name}
	if platform:
		query_args['platform'] = platform_name
	if genre:
		query_args['genre'] = genre

	response = self.call_api(API_URL, query, query_args)
	return response


def getPlatformsList():
	query = 'GetPlatformsList'

	response = call_api(API_URL, query)
	
	return parsePlatformsList(response)
	
def parsePlatformsList(response):
	root = ElementTree.fromstring(response)
	platforms = {}
	for element in root.findall('./Platforms/Platform'):
		platform_id = element.find('id').text
		platform_name = element.find('name')
		if platform_name is not None:
			platform_name = platform_name.text
		platform_alias = element.find('alias')
		if platform_alias is not None:
			platform_alias = platform_alias.text

		platforms[platform_id] = platform_name, platform_alias

	return platforms

def getPlatformGames(platform_id):
	query = 'GetPlatformGames'
	query_args = {'platform':platform_id}

	response = call_api(API_URL, query, query_args)
	return response


	

if __name__ == "__main__":
	with open('output.txt', 'w') as out:
		#out.write(API().getGamesList('Super', platform = 'Super Nintendo (SNES)'))
		#out.write(API().getPlatformGames('0'))
		platforms = getPlatformsList()
		#print platforms
		for platform in platforms:
			print platforms[platform]
