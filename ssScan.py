  
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ssScan.py
#  
#  Copyright 2019 laet4x <https://github.com/laet4>x
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
# 
import argparse, urllib3
import sys
import urlparse
from pyfiglet import Figlet
from Wappalyzer import Wappalyzer, WebPage

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # disable Python SSL warnings !

green = "\033[32m"
blue = "\033[34m"
red = "\033[31m"
bold = "\033[1m"
end = "\033[0m"

wappalyzer = Wappalyzer.latest()

custom_fig = Figlet(font='graffiti')

banner = '''                                  
By laet4x  
'''
print custom_fig.renderText('ssScan')
print banner


def parseurl(url):
	p = urlparse.urlparse(url, 'http')
	netloc = p.netloc or p.path
	path = p.path if p.netloc else ''
	if not netloc.startswith('www.'):
		netloc = 'www.' + netloc

	p = urlparse.ParseResult('http', netloc, path, *p[3:])
	return p.geturl()


def detect(domain,ig,out):
	try:
		webpage = WebPage.new_from_url(domain)
		services = wappalyzer.analyze(webpage)
		print("[+] " + str(domain) + " | " + green + bold + " - ".join(services) + end)
		if out != 'None':
			with open(out, 'a') as f:
				f.write(domain + " | " + " - ".join(services) + "\n")
				f.close()
	
	except Exception as e:
		if ig == 'True':
			pass
		else:
			print(red+"Error: " + end + "[ " + bold + str(domain) + end + " ] > " + str(e))

parser = argparse.ArgumentParser(description = 'Get website services')
parser.add_argument('domain', metavar='domain', type=str,
                    help='domain name')
parser.add_argument("-i", "--ignore", help="To Ignore The Errors", action='store_true')
parser.add_argument("-o", "--output", help="Save The Results To a File", type=str)
parser.add_argument("-w", "--domainlist", help="Domains List File", type=str)
parser.add_argument("-t", "--thread", help="Theads Number - (Default: 10)", type=int)

#parse arguments
args = parser.parse_args()

links = str(args.domainlist)
threads = str(args.thread)
ig = str(args.ignore)
out = str(args.output)

#parse domain
domain = parseurl(args.domain)
detect(domain,ig, out)

