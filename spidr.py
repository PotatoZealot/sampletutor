import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import json


fhand = urllib.request.urlopen('') #url goes here

for line in fhand:
    print(line.decode().split())

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter link:')
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')