#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
from xml.etree import ElementTree

BASEURL = "http://thegamesdb.net/api/"
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
USER_AGENT += '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

class Game():
	pass
		
class Platform():

	def __init__(self, platform_id, platform_name, platform_alias=None):
		self.platform_id = platform_id
		self.platform_name = platform_name
		self.platform_alias = platform_alias

class API():
	

	@staticmethod
	def call_api(base_url, query, query_args={}):
		url_values = urllib.urlencode(query_args)
		call_url = base_url + query + '.php?' + url_values
		print call_url
		request = urllib2.Request(call_url)
		request.add_unredirected_header('User-Agent', USER_AGENT)
		query_response = urllib2.urlopen(request).read()


		# Cache a copy of the XML response locally
		with open(query+'.xml', 'w') as output:
			output.write(query_response + '\n')

		return query_response

	def getGamesList(self, name, platform_name=None, genre=None):
		query = 'GetGamesList'
		query_args = {'name':name}
		if platform:
			query_args['platform'] = platform_name
		if genre:
			query_args['genre'] = genre

		response = self.call_api(BASEURL, query, query_args)
		return response


	def getPlatformsList(self):
		query = 'GetPlatformsList'

		response = self.call_api(BASEURL, query)
		
		return self.parsePlatformsList(response)
		
	def parsePlatformsList(self, response):
		root = ElementTree.fromstring(response)
		platforms = {}
		for element in root.findall('./Platforms/Platform'):
			platform_id = element.find('id').text
			platform_name = element.find('name').text
			platform_alias = element.find('alias').text if element.find('alias') else None
			platforms[platform_id] = platform_name, platform_alias

		return platforms

	def getPlatformGames(self, platform_id):
		query = 'GetPlatformGames'
		query_args = {'platform':platform_id}

		response = self.call_api(BASEURL, query, query_args)
		return response


	

if __name__ == "__main__":
	with open('output.txt', 'w') as out:
		#out.write(API().getGamesList('Super', platform = 'Super Nintendo (SNES)'))
		#out.write(API().getPlatformGames('0'))
		platforms = API().getPlatformsList()
		print platforms
		for platform in platforms:
			print platforms[platform]
