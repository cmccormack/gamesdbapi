#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from xml.etree import ElementTree
from StringIO import StringIO


def run():
	filename = '\\MACK-RETROPIE\\snes\\gameslist.xml' 	# default filename
	for arg in sys.argv:
		if arg[-3:].lower() == 'xml':
			print arg
			filename = arg
	print filename
	doc = ElementTree.parse(filename)
	root = doc.getroot()
	

	names = []
	paths = []
	longestpath = ''
	for elem in root.findall('game'):
		name = elem.find('name').text
		names.append(name)
		path = elem.find('path').text
		paths.append(path)
		if len(path) > len(longestpath):
			longestpath = path

	pathN = len(longestpath)
	
	for i,name in enumerate(names):
		print "[{num:03}] {0} {dash} [{num:03}] {1}".format(paths[i].encode('utf-8'),name.encode('utf-8'), dash='-'*(pathN-len(paths[i])), num=i)

def printxml(xmldata):
	print xmldata
	


if __name__ == "__main__":
	run()
